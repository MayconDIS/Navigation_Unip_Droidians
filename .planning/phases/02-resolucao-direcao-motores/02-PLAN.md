# Plano da Fase 2: Resolução do Problema de Direção e Controle de Motores

Este plano descreve as modificações necessárias no firmware do Arduino e no driver ROS 2 para implementar um controle em malha fechada estável, de alta frequência, e resolver os problemas de alinhamento físico que fazem o robô desviar de rota ou derrapar.

## Goals

1.  **Aumento de Frequência (50Hz)**: Reduzir o intervalo da malha de controle no Arduino de 100ms para 20ms.
2.  **Uso de Interrupções de Hardware Nativas**: Evitar perda de ticks usando `attachInterrupt` em vez de `PinChangeInterrupt` nos pinos 2 e 3.
3.  **Controle PI com Feedforward**: Substituir a lógica integral pura por uma malha de controle PI robusta com Feedforward. O controlador PI deve compensar dinamicamente a assimetria física dos motores (um roda a **192 RPM** e outro a **216 RPM** sob mesma potência) sem a dependência do TRIM estático.
4.  **Remoção de TRIM Estático**: Desativar fatores estáticos para deixar a malha corrigir as velocidades dinamicamente.
5.  **Foco em Trajetória Retilínea e Teleoperação (Prioridade)**: O objetivo principal desta fase é eliminar a derrapagem (*skidding*) e fazer o robô andar reto fisicamente.
6.  **Postergamento de Bugs de Nav2 / Gazebo**: Questões de quebra de mapa no Nav2 (autônomo) e teletransporte no simulador Gazebo foram adiadas para depois do dia 13.

---

## Proposed Changes

### 1. Arduino (`Arduino/odometrypulse-malha/odometrypulse-malha.ino`)
*   Substituir as interrupções de biblioteca por nativas.
*   Implementar a lógica PI e limitar o acúmulo de erro (anti-windup).
*   Zerar integradores em caso de setpoint de parada (evita acúmulo ao parar).

### 2. ROS 2 (`serial_com_py/`)
*   Calibração de odometria e verificação dos eixos em [base_driver_pulse.py](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/base_driver_pulse.py).
*   Criação de nó de teleoperação WASD customizado [wasd_teleop.py](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/wasd_teleop.py) para controle do robô pelo terminal.

---

## Verification Plan

### Testes Estáticos e de Pista
*   **Rodas Suspensas**: Validar se as rodas respondem na mesma velocidade ao comando `cmd_vel`.
*   **Deslocamento Linear**: Medir o desvio físico ao andar 1 metro em linha reta. O limite máximo aceitável de desvio lateral é de 5 cm.
