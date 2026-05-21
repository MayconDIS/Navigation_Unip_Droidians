// ============================================================
//  UDH1 — Motor + Odometria + Controle de Velocidade
//  UnipDroidians Robotics Team
//
//  Correções aplicadas:
//    1. METROS_POR_PULSO usa diâmetro correto (0.156 m)
//    2. MAX_PWM separado por roda (ESQ e DIR) para calibrar desequilíbrio
//    3. MAX_PWM_GIRO separado por roda para calibrar giro
//    4. Feed-forward na partida (evita desequilíbrio inicial)
//    5. Reset de integrador em mudança significativa de setpoint
//    6. Watchdog freia imediatamente
// ============================================================

#include <PinChangeInterrupt.h>

// --- PINOS MOTORES ---
#define PIN_L_DIR   4
#define PIN_L_PWM   5
#define PIN_L_BREAK 11
#define PIN_R_DIR   7
#define PIN_R_PWM   9
#define PIN_R_BREAK 13

// --- PINOS ODOMETRIA ---
#define ODO_L   10   // canal B esquerda (direção)
#define ODO_R   6    // canal B direita  (direção)
#define ODO_A_L 2    // canal A esquerda (contagem)
#define ODO_A_R 3    // canal A direita  (contagem)

// ============================================================
// PARÂMETROS FÍSICOS
// Diâmetro real da roda UDH1 = 0.156 m
// 12.95 pulsos mecânicos/rev; quadratura 4x → 51.8 pulsos efetivos
// ============================================================
const float METROS_POR_PULSO = 0.156 * 3.14159 / (12.95 * 4.0);

// ============================================================
// CALIBRAÇÃO DE PWM POR RODA
const int MIN_PWM_ESQ      = 13;   // ← aumente se roda ESQUERDA demorar a sair
const int MIN_PWM_DIR      = 13;   // ← aumente se roda DIREITA  demorar a sair

// -- Movimento reto / frente / trás --
// Se uma roda gira mais rápido em regime:
//   → Diminua o MAX_PWM dessa roda em passos de 2
const int MAX_PWM_ESQ      = 36;   // ← diminua se roda ESQUERDA for mais rápida
const int MAX_PWM_DIR      = 36;   // ← diminua se roda DIREITA  for mais rápida

// -- Giro no próprio eixo (comando J / L) --
const int MAX_PWM_GIRO_ESQ = 55;   // ← diminua se o giro puxar demais para esquerda
const int MAX_PWM_GIRO_DIR = 55;   // ← diminua se o giro puxar demais para direita

// ============================================================

// --- ODOMETRIA ---
volatile long pulsosEsq = 0;
volatile long pulsosDir = 0;
long pulsosEsqAnt       = 0;
long pulsosDirAnt       = 0;
unsigned long tempoAnterior = 0;

// --- CONTROLE DE VELOCIDADE (controlador I) ---
const float KP                       = 4.0;
const unsigned long CTRL_INTERVAL_MS = 200;

// Feed-forward: pré-aquece o integrador na partida para as duas rodas
// saírem juntas. Ajuste se o robô der tranco (diminua) ou não sair (aumente).
const float FF_GANHO = 28.0;

float velEsq = 0.0;
float velDir = 0.0;
float pwmEsq = 0.0;
float pwmDir = 0.0;

// --- COMANDOS ROS ---
float setPointEsq = 0.0;
float setPointDir = 0.0;
unsigned long lastCmdTime        = 0;
const unsigned long CMD_TIMEOUT_MS = 500;

// ============================================================
void setup() {
  Serial.begin(115200);

  pinMode(PIN_L_DIR,   OUTPUT);
  pinMode(PIN_R_DIR,   OUTPUT);
  pinMode(PIN_L_BREAK, OUTPUT);
  pinMode(PIN_R_BREAK, OUTPUT);

  pinMode(ODO_L,   INPUT_PULLUP);
  pinMode(ODO_R,   INPUT_PULLUP);
  pinMode(ODO_A_L, INPUT_PULLUP);
  pinMode(ODO_A_R, INPUT_PULLUP);

  // Quadratura 4x: CHANGE nos dois canais de cada encoder
  attachPinChangeInterrupt(digitalPinToPCINT(ODO_A_L), countEsqA, CHANGE);
  attachPinChangeInterrupt(digitalPinToPCINT(ODO_L),   countEsqB, CHANGE);
  attachPinChangeInterrupt(digitalPinToPCINT(ODO_A_R), countDirA, CHANGE);
  attachPinChangeInterrupt(digitalPinToPCINT(ODO_R),   countDirB, CHANGE);

  // Freia na partida
  digitalWrite(PIN_L_BREAK, HIGH);
  digitalWrite(PIN_R_BREAK, HIGH);
}

// ============================================================
void loop() {

  // ----------------------------------------------------------
  // LEITURA SERIAL (ROS → Arduino)
  // ----------------------------------------------------------
  while (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');

    if (input.startsWith("CMD:")) {
      int sep = input.indexOf(';', 4);
      if (sep != -1) {
        float novoEsq = input.substring(4, sep).toFloat();
        float novoDir = input.substring(sep + 1).toFloat();
        lastCmdTime   = millis();

        // Parada imediata
        if (abs(novoEsq) < 0.001 && abs(novoDir) < 0.001) {
          setPointEsq = 0.0;
          setPointDir = 0.0;
          pwmEsq      = 0.0;
          pwmDir      = 0.0;
          moveMotor(0, 0);

        } else {
          // Reset de integrador em mudança significativa de setpoint
          // com feed-forward para partida simétrica
          if (abs(novoEsq - setPointEsq) > 0.05) {
            pwmEsq = (novoEsq >= 0 ? 1 : -1) * max(abs(novoEsq) * FF_GANHO, 6.0f);
          }
          if (abs(novoDir - setPointDir) > 0.05) {
            pwmDir = (novoDir >= 0 ? 1 : -1) * max(abs(novoDir) * FF_GANHO, 6.0f);
          }

          setPointEsq = novoEsq;
          setPointDir = novoDir;
        }
      }
    }
  }

  // ----------------------------------------------------------
  // WATCHDOG: para se ROS parar de enviar
  // ----------------------------------------------------------
  if (millis() - lastCmdTime >= CMD_TIMEOUT_MS) {
    setPointEsq = 0.0;
    setPointDir = 0.0;
    pwmEsq      = 0.0;
    pwmDir      = 0.0;
    moveMotor(0, 0);  // freia imediatamente
  }

  // ----------------------------------------------------------
  // CICLO DE CONTROLE + ODOMETRIA (a cada 200 ms)
  // ----------------------------------------------------------
  unsigned long agora = millis();
  unsigned long dt_ms = agora - tempoAnterior;

  if (dt_ms >= CTRL_INTERVAL_MS) {
    float dt_s = dt_ms * 0.001f;

    noInterrupts();
    long pEsq = pulsosEsq;
    long pDir = pulsosDir;
    interrupts();

    long dEsq = pEsq - pulsosEsqAnt;
    long dDir = pDir - pulsosDirAnt;
    pulsosEsqAnt = pEsq;
    pulsosDirAnt = pDir;

    // Velocidade medida (esquerda negada: encoder montado invertido)
    velEsq = -(dEsq * METROS_POR_PULSO) / dt_s;
    velDir =  (dDir * METROS_POR_PULSO) / dt_s;

    // --- CONTROLADOR I ---
    if (abs(setPointEsq) < 0.001) {
      pwmEsq = 0.0;
    } else {
      pwmEsq += (setPointEsq - velEsq) * KP;
      pwmEsq  = constrain(pwmEsq, -100.0, 100.0);
    }

    if (abs(setPointDir) < 0.001) {
      pwmDir = 0.0;
    } else {
      pwmDir += (setPointDir - velDir) * KP;
      pwmDir  = constrain(pwmDir, -100.0, 100.0);
    }

    // Publica odometria para o ROS
    Serial.print("ODO:");
    Serial.print(pEsq);  Serial.print(";");
    Serial.print(pDir);  Serial.print(";");
    Serial.println(dt_ms);

    moveMotor((int)pwmDir, (int)pwmEsq);
    tempoAnterior = agora;
  }
}

// ============================================================
// ACIONAMENTO DOS MOTORES
// velD / velE: −100 a +100
// Usa MAX_PWM separado por roda — permite calibrar desequilíbrio
// ============================================================
void moveMotor(int velD, int velE) {

  // Zona morta
  if (abs(velE) < 5) velE = 0;
  if (abs(velD) < 5) velD = 0;

  // Detecta giro no próprio eixo: rodas em sentidos opostos
  bool girando = (velE != 0 && velD != 0) && ((velE > 0) != (velD > 0));

  // Seleciona limite de PWM correto para cada roda e modo
  int limE = girando ? MAX_PWM_GIRO_ESQ : MAX_PWM_ESQ;
  int limD = girando ? MAX_PWM_GIRO_DIR : MAX_PWM_DIR;

  // Motor ESQUERDO
  if (velE != 0) {
    int pwmE = map(abs(velE), 5, 100, MIN_PWM_ESQ, limE);
    digitalWrite(PIN_L_BREAK, LOW);
    digitalWrite(PIN_L_DIR,   velE > 0);
    analogWrite(PIN_L_PWM, pwmE);
  } else {
    digitalWrite(PIN_L_BREAK, HIGH);
    analogWrite(PIN_L_PWM, 0);
  }

  // Motor DIREITO
  if (velD != 0) {
    int pwmD = map(abs(velD), 5, 100, MIN_PWM_DIR, limD);
    digitalWrite(PIN_R_BREAK, LOW);
    digitalWrite(PIN_R_DIR,   velD < 0);
    analogWrite(PIN_R_PWM, pwmD);
  } else {
    digitalWrite(PIN_R_BREAK, HIGH);
    analogWrite(PIN_R_PWM, 0);
  }
}

// ============================================================
// QUADRATURA 4x — ISRs
// ============================================================

void countEsqA() {
  bool a = digitalRead(ODO_A_L);
  bool b = digitalRead(ODO_L);
  if (a ^ b) pulsosEsq++; else pulsosEsq--;
}

void countEsqB() {
  bool a = digitalRead(ODO_A_L);
  bool b = digitalRead(ODO_L);
  if (a == b) pulsosEsq++; else pulsosEsq--;
}

void countDirA() {
  bool a = digitalRead(ODO_A_R);
  bool b = digitalRead(ODO_R);
  if (a ^ b) pulsosDir++; else pulsosDir--;
}

void countDirB() {
  bool a = digitalRead(ODO_A_R);
  bool b = digitalRead(ODO_R);
  if (a == b) pulsosDir++; else pulsosDir--;
}
