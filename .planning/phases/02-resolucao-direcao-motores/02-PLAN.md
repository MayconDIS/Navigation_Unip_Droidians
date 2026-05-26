# Plano da Fase 2: Restauração da Base Física e Otimização da Navegação

Este plano descreve as modificações necessárias para restaurar a base de controle física (Arduino e drivers de baixo nível) a partir do backup `Navigation-main` (devido a restrições e relutância da equipe com as novas mudanças de controle) e aplicar melhorias de navegação estritamente via sintonia de parâmetros do Nav2 e AMCL.

## Goals

1.  **Restauração da Base Física**: Reverter o firmware do Arduino e os drivers Python para o estado original estável do backup `Navigation-main`.
2.  **Melhorias na Configuração do Nav2/AMCL**: Sintonia fina nos arquivos `nav2_params.yaml` e `nav2_params_realsense.yaml` para otimizar o comportamento autônomo.
3.  **Segurança Física Ativa**: Garantir que o nó `safe_stop` seja executado para evitar colisões frontais.
4.  **Resolução de timeouts e erros de movimentação**: Corrigir o parâmetro `min_y_velocity_threshold` e ajustar tolerâncias de transformadas (TF) no controlador e localizador.

---

## Proposed Changes

### 1. Arduino (`Arduino/`)
*   Substituir o firmware na pasta `Arduino/odometrypulse-malha/` pelo original do backup `Navigation-main`.
*   Garantir a restauração dos arquivos `odometrypulse.ino` e `odometry_new.ino`.

### 2. ROS 2 (`serial_com_py/`)
*   Restaurar `base_driver.py` e `base_driver_pulse.py` para as versões originais do backup `Navigation-main`.
*   Restaurar `safe_stop.py` e integrá-lo nos arquivos de launch correspondentes.

### 3. Parâmetros de Navegação (`src/udh1_mapping/config/`)
*   Sintonizar os arquivos de parâmetros do Nav2 (`nav2_params.yaml`, `nav2_params_realsense.yaml` e `nav2_params_sim.yaml`) ajustando os limites de velocidade lateral para robô diferencial, as tolerâncias de TF/AMCL, e removendo recuperações agressivas de rotação.

### 4. Launch Files (`src/my_robot_bringup/launch/`)
*   Garantir que os launch files executem os nós corretos da base física (`base_driver`) e de segurança (`safe_stop`).

---

## Verification Plan

### Testes e Verificação
*   **Compilação**: Executar `colcon build` para garantir que a compilação do workspace seja concluída sem erros de compilação ou de sintaxe.
*   **Parâmetros**: Validar que os limites de velocidade do Nav2 estão sintonizados corretamente para evitar travamentos ou timeouts de movimento do robô diferencial.
