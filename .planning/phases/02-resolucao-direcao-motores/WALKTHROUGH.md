# Walkthrough: Resolução do Problema de Direção e Controle de Motores

Este walkthrough documenta as alterações realizadas para resolver o problema físico do robô UD-H1 de desviar de rota ou derrapar.

## Changes Made

### 1. Firmware do Arduino (`Arduino/odometrypulse-malha/`)
*   **Frequência da Malha Fechada**: Aumentada para **50 Hz** (período de 20ms) para reduzir o tempo de reação de correção das rodas.
*   **Controlador PI + Feedforward**: Implementada a fórmula completa de PI e Feedforward com proteção contra estouro da parcela integral (anti-windup).
*   **Interrupções de Hardware**: Alterado o código para usar a função `attachInterrupt` direta de hardware do Arduino Uno/Mega nos pinos 2 e 3 (`INT0` e `INT1`) em vez da biblioteca `PinChangeInterrupt`, eliminando a perda de pulsos em velocidades mais altas.
*   **Remoção de TRIM**: Desativado o TRIM estático para evitar disputas com a malha fechada.

### 2. Driver de Odometria ROS 2 (`serial_com_py/`)
*   **Rampas de Aceleração Suaves**: Adicionadas rampas de limite de aceleração linear ($0.8\text{ m/s}^2$) e angular ($1.5\text{ rad/s}^2$) para suavizar comandos bruscos e evitar derrapagens.
*   **Remoção de Negações de Eixo**: Removida a negação global redundante das velocidades calculadas no script Python, restaurando a consistência cinemática do TF com o AMCL e os costmaps.

### 3. Utilidade de Teleoperação WASD
*   **WASD Teleop**: Criado o nó [wasd_teleop.py](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/wasd_teleop.py) e adicionada sua entrada no [setup.py](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/src/serial_com_py/setup.py) para permitir controle direcional direto.

### 4. Reestruturação do Planejamento GSD
*   Inserção da **Fase 2: Resolução do Problema de Direção e Controle de Motores** como a fase ativa e deslocamento de "Mapeamento e Sensorização" para a **Fase 3**.

---

## Verification Plan & Steps for the Team

Como o robô necessita de validação física no laboratório, a equipe deve seguir estes passos de teste (com foco principal em teleoperação e retilineidade física antes do dia 13):

1.  **Validação com Rodas Suspensas (Estático)**:
    *   Suspender o robô para evitar contato com o chão.
    *   Iniciar a teleoperação WASD customizada da equipe:
        ```bash
        ros2 run serial_com_py wasd_teleop
        ```
    *   Pressionar **W** e verificar se as duas rodas giram na mesma velocidade para a frente.
2.  **Validação de Coordenadas de Odometria**:
    *   Comandar o robô para frente: verificar se a pose X no tópico `/odom` aumenta positivamente (correto no RViz2, conforme observado pela equipe).
    *   Comandar rotação para a esquerda: verificar se a pose angular yaw (orientação Z) aumenta positivamente (regra da mão direita).
3.  **Teste de Direção Retilínea no Piso (Foco Prioritário)**:
    *   Colocar o robô em uma marcação retilínea no chão e enviar comando linear constante.
    *   Verificar se o desvio lateral na distância de 1 metro é inferior a **5 cm**.

*Nota: Testes de navegação autônoma pelo Nav2 (onde ocorria a instabilidade no mapa) e comportamento de simulação no Gazebo (teletransporte) foram postergados para a próxima fase (pós-dia 13).*
