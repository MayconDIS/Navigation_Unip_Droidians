# Resumo da Fase 2: Resolução do Problema de Direção e Controle de Motores

Este documento resume as modificações efetuadas e validadas para corrigir o controle de velocidade das rodas e alinhar a odometria física com o RViz no robô UD-H1.

## Ações Realizadas

### 1. Refatoração do Firmware do Arduino
*   **Arquivo**: [odometrypulse-malha.ino](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/Arduino/odometrypulse-malha/odometrypulse-malha.ino)
*   **Frequência do Loop**: Aumentada de 10 Hz para **50 Hz** (20ms).
*   **Controlador**: Implementado controle **PI (Proporcional-Integral) real com Feedforward** e proteção de estouro integral (anti-windup).
*   **Interrupções**: Modificado de `PinChangeInterrupt` para `attachInterrupt` nativo nos pinos de hardware 2 e 3 (`INT0` e `INT1`) para evitar perda de ticks.
*   **TRIM Estático**: Removido da lógica para evitar competição com a malha fechada.

### 2. Calibração e Rampa no Driver Python
*   **Arquivo**: [base_driver_pulse.py](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/base_driver_pulse.py)
*   **Rampas de Aceleração**: Implementado limites de aceleração linear ($0.8\text{ m/s}^2$) e angular ($1.5\text{ rad/s}^2$) no callback de comando. Isso suaviza partidas e paradas rápidas enviadas pelo Nav2, evitando que as rodas de hoverboard patinem ou percam tração.
*   **Remoção de Negações**: Removida a negação global de odometria linear/angular que gerava inconsistência matemática no filtro de localização e costmaps.

---

## Próximos Passos de Verificação Prática
*   Realizar o teste estático com as rodas suspensas para confirmar que os sentidos e rotações estão sintonizados.
*   Executar o teste dinâmico no chão em linha reta por 2 metros.
