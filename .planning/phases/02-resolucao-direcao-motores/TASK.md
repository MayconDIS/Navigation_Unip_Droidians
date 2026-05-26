# Tasks: Restauração da Base Física, Otimização da Navegação e Teleoperação

- [x] Restaurar o firmware do Arduino (`odometrypulse-malha.ino`, `odometrypulse.ino`, `odometry_new.ino`) a partir do backup `Navigation-main`
- [x] Restaurar os nós Python da base física e segurança (`base_driver.py`, `base_driver_sim.py`, `safe_stop.py`) a partir do backup `Navigation-main`
- [x] Ajustar os parâmetros de navegação para melhorar o comportamento diferencial (`nav2_params_realsense.yaml`, `nav2_params_sim.yaml`)
- [x] Sintonizar/Ajustar `nav2_params.yaml` de forma a garantir as melhorias de navegação (tolerâncias de TF, controle diferencial, etc.)
- [x] Atualizar os launch files (`udh1_core.launch.py`, `udh1_core_maping.launch.py`, `navigation.launch.py`) para apontar para os drivers e nós corretos restaurados
- [x] Implementar o nó de teleoperação por joystick (`joystick_teleop.py`) e registrar no `setup.py`
- [x] Criar o arquivo launch unificado (`joystick_teleop.launch.py`)
- [x] Ajustar velocidade linear máxima do teclado e do controle para `0.15 m/s`
- [x] Validar a compilação do workspace via `colcon build`
