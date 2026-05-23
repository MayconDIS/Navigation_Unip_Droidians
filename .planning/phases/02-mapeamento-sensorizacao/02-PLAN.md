# Plano da Fase 2: Mapeamento e Sensorização (UD-H1 Navigation Stack)

Este plano descreve as etapas para configurar, executar e validar a sensorização do sensor LIDAR (RPLidar) e a geração de mapas de ocupação 2D (SLAM) tanto em ambiente simulado (Gazebo Classic) quanto no robô físico real.

## Goals

1.  **Validação dos Sensores (LIDAR)**: Garantir que as leituras do laser sejam transmitidas e filtradas corretamente no tópico `/scan`.
2.  **Mapeamento 2D (SLAM)**: Gerar um mapa estático de ocupação 2D representativo do ambiente utilizando o `slam_toolbox`.
3.  **Configuração de Launch Files**: Assegurar que os arquivos de inicialização do robô físico e de simulação estejam parametrizados e estáveis.

---

## Plan 2.1: Sensorização e Mapeamento em Simulação (Gazebo)

### Goal
Validar a cinemática, o sensor LIDAR e o pipeline de SLAM dentro do ambiente simulado do Gazebo Classic antes de passar para o hardware físico.

### Requirements Covered
*   **SLAM-01**: Leitura de laser publicada em `/scan`.
*   **SLAM-03**: Geração e persistência do mapa estático do ambiente.

### Proposed Execution Steps
1.  **Iniciar a Simulação com SLAM**:
    *   Executar o launch de simulação e mapeamento online:
        ```bash
        ros2 launch udh1_gazebo gazebo.launch.py
        ```
        (Isso deve abrir o Gazebo com o robô posicionado no mundo de teste `udh1_world.world` e o `robot_state_publisher` ativo).
    *   Executar o nó do SLAM Toolbox para mapeamento online assíncrono:
        ```bash
        ros2 launch udh1_mapping launch.py
        ```
2.  **Teleoperação e Geração do Mapa**:
    *   Iniciar o nó de teleoperação por teclado em um terminal separado:
        ```bash
        ros2 run teleop_twist_keyboard teleop_twist_keyboard
        ```
    *   Movimentar o robô lentamente pelo cenário no Gazebo enquanto observa a geração do mapa no RViz2.
3.  **Salvar o Mapa Gerado**:
    *   Utilizar o plugin do SLAM Toolbox no RViz2 ou rodar o comando do `map_saver` para persistir os arquivos na pasta `mapas/`:
        ```bash
        ros2 run nav2_map_server map_saver_cli -f ~/Navigation/mapas/mapa_sim_teste
        ```

---

## Plan 2.2: Sensorização e Mapeamento no Robô Físico

### Goal
Configurar e executar o mapeamento real do laboratório/ambiente físico de competição usando o LIDAR físico RPLidar C1 e a base diferencial real controlada pelo Arduino.

### Requirements Covered
*   **DRV-01**: Conexão serial com o Arduino Mega/Uno.
*   **SLAM-01**: Driver do LIDAR RPLidar ativo e publicando em `/scan`.
*   **SLAM-03**: Salvar o mapa real gerado em `mapas/mapa_udh1.yaml` / `.pgm`.

### Proposed Execution Steps
1.  **Conexão do Hardware e Permissões**:
    *   Verificar se o Arduino está conectado em `/dev/ttyACM0` e o LIDAR em `/dev/ttyUSB0` dentro do WSL2.
    *   Dar permissão de escrita e leitura para as portas seriais:
        ```bash
        sudo chmod 666 /dev/ttyACM0 /dev/ttyUSB0
        ```
2.  **Inicializar o Bringup de Mapeamento**:
    *   Lançar o script unificado de mapeamento para o robô real:
        ```bash
        ros2 launch my_robot_bringup udh1_core_maping.launch.py
        ```
        (Este arquivo carrega o `base_driver_pulse` para odometria, o driver do `sllidar_node`, o `robot_state_publisher`, os filtros de laser e o mapeamento online assíncrono).
3.  **Mapear o Ambiente Real**:
    *   Executar a teleoperação por teclado para movimentar o robô fisicamente pelo ambiente de forma suave para evitar deslizamentos de roda que corrompem a odometria:
        ```bash
        ros2 run teleop_twist_keyboard teleop_twist_keyboard
        ```
4.  **Salvar o Mapa Real**:
    *   Salvar o mapa gerado para que seja carregado no Nav2 posteriormente:
        ```bash
        ros2 run nav2_map_server map_saver_cli -f ~/athome_ws/mapas/mapa_udh1
        ```

---

## Verification Plan

### Automated/Simulation Tests
*   Verificar se as leituras do LIDAR em `/scan` possuem cobertura correta (360 graus na simulação, filtrado na realidade).
*   Executar `ros2 topic echo /scan` e verificar a frequência de publicação (nominal de 10-15Hz).

### Manual Verification
*   Validar visualmente no RViz2 se as paredes detectadas pelo LIDAR coincidem com o desenho que o SLAM Toolbox está construindo no mapa `/map`.
*   Garantir que os arquivos `mapa_udh1.yaml` e `mapa_udh1.pgm` sejam gerados sem corrupção de imagem e com os caminhos corretos declarados no arquivo `.yaml`.
