# Plano da Fase 2: Restauração da Base Física, Otimização de Navegação e Teleoperação

Este plano descreve as modificações necessárias para restaurar a base de controle física (Arduino e drivers de baixo nível) a partir do backup `Navigation-main`, aplicar melhorias de navegação estritamente via sintonia de parâmetros do Nav2/AMCL e adicionar opções de controle manual flexíveis (teclado e joystick).

## Goals

1.  **Restauração da Base Física**: Reverter o firmware do Arduino e os drivers Python para o estado original estável do backup `Navigation-main`.
2.  **Melhorias na Configuração do Nav2/AMCL**: Sintonia fina nos arquivos `nav2_params.yaml`, `nav2_params_realsense.yaml` e `nav2_params_sim.yaml` para otimizar o comportamento autônomo.
3.  **Segurança Física Ativa**: Garantir que o nó `safe_stop` seja executado para evitar colisões frontais.
4.  **Resolução de timeouts e erros de movimentação**: Corrigir o parâmetro `min_y_velocity_threshold` e ajustar tolerâncias de transformadas (TF) no controlador e localizador.
5.  **Opções de Teleoperação Manual**: Implementar controle via teclado WASD (latching mode) e via Joystick (com botão de segurança deadman), ambos limitados a `0.15 m/s` para maior segurança.

---

## Proposed Changes

### 1. Arduino (`Arduino/`)
*   Substituir o firmware na pasta `Arduino/odometrypulse-malha/` pelo original do backup `Navigation-main`.
*   Garantir a restauração dos arquivos `odometrypulse.ino` e `odometry_new.ino`.

### 2. ROS 2 (`serial_com_py/`)
*   Restaurar `base_driver.py` para a versão original do backup `Navigation-main`.
*   Restaurar `safe_stop.py` e integrá-lo nos arquivos de launch correspondentes.
*   [NEW] Criar `joystick_teleop.py` para assinar o `/joy` e publicar `/cmd_vel`.
*   [MODIFY] Registrar `joystick_teleop` nos entry points do `setup.py`.

### 3. Parâmetros de Navegação (`src/udh1_mapping/config/`)
*   Sintonizar os arquivos de parâmetros do Nav2 (`nav2_params.yaml`, `nav2_params_realsense.yaml` e `nav2_params_sim.yaml`) ajustando os limites de velocidade lateral para robô diferencial, as tolerâncias de TF/AMCL, e removendo recuperações agressivas de rotação.

### 4. Launch Files (`src/my_robot_bringup/launch/`)
*   Garantir que os launch files executem os nós corretos da base física (`base_driver`) e de segurança (`safe_stop`).
*   [NEW] Criar o arquivo `joystick_teleop.launch.py` para lançar o `joy_node` e o tradutor de controle físico.

---

## Verification Plan

### Testes e Verificação
*   **Compilação**: Executar `colcon build` no workspace do WSL2 para garantir que todos os pacotes compilem sem erros.
*   **Teleoperação Teclado**: Rodar `wasd_teleop` e checar controle em modo latching a 0.15 m/s.
*   **Teleoperação Joystick**: Redirecionar o controle Xbox pelo `usbipd`, rodar o launch file correspondente e verificar a recepção de dados no `/cmd_vel` ao segurar o botão **LB**.
