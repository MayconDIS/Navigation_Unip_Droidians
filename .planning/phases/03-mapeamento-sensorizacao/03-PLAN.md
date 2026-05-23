# Plano da Fase 3: Mapeamento e Sensorização

Este plano descreve as etapas para configurar, executar e validar a sensorização do sensor LIDAR (RPLidar) e a geração de mapas de ocupação 2D (SLAM) tanto em ambiente simulado (Gazebo Classic) quanto no robô físico real.

## Goals

1.  **Validação dos Sensores (LIDAR)**: Garantir que as leituras do laser sejam transmitidas e filtradas corretamente no tópico `/scan`.
2.  **Mapeamento 2D (SLAM)**: Gerar um mapa estático de ocupação 2D representativo do ambiente utilizando o `slam_toolbox`.

---

## Proposed Changes

### 1. Launch Files (`my_robot_bringup/launch/` e `udh1_gazebo/launch/`)
*   Executar o launch de simulação e mapeamento online.
*   Executar o SLAM Toolbox para mapeamento online assíncrono.

---

## Verification Plan

### Testes de Sensorização
*   Verificar se as leituras do LIDAR em `/scan` possuem cobertura correta (360 graus na simulação, filtrado na realidade).
*   Garantir que os arquivos `mapa_udh1.yaml` e `mapa_udh1.pgm` sejam salvos de forma íntegra.
