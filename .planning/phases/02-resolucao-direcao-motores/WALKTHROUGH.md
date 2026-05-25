# Walkthrough: Restauração da Base Física e Otimização da Navegação

Este walkthrough documenta as alterações realizadas para restaurar a base de controle física (Arduino e drivers de baixo nível) a partir do backup `Navigation-main` (devido a restrições e relutância da equipe com as novas mudanças de controle) e aplicar melhorias de navegação estritamente via sintonia de parâmetros do Nav2 e AMCL.

## Changes Made

### 1. Restauração do Firmware do Arduino
Para respeitar a decisão da equipe em relação ao controle mecânico do robô, os seguintes firmwares foram restaurados para a versão estável e original da pasta `Navigation-main`:
*   `Arduino/odometrypulse-malha/odometrypulse-malha.ino` (Retorno ao loop original de 100ms e controle de TRIM antigo)
*   `Arduino/odometrypulse/odometrypulse.ino`
*   `Arduino/odometry_new/odometry_new.ino`

### 2. Restauração dos Drivers de Baixo Nível (Python)
Os arquivos de driver e os nós ROS 2 da pasta `serial_com_py` foram reestabelecidos para suas respectivas versões de backup:
*   `src/serial_com_py/serial_com_py/base_driver.py` (Revertido para o baseline)
*   `src/serial_com_py/serial_com_py/base_driver_pulse.py` (Revertido para o baseline)
*   `src/serial_com_py/serial_com_py/base_driver_sim.py` (Nó de simulação restaurado)
*   `src/serial_com_py/serial_com_py/safe_stop.py` (Nó de segurança ativa restaurado)

### 3. Registro e Integração no Package Setup
*   `src/serial_com_py/setup.py`: Adicionados os entry points `safe_stop` e `base_driver_sim` nos console scripts para que o ROS 2 possa localizá-los e executá-los normalmente.

### 4. Ajustes Finos nos Parâmetros do Nav2 e AMCL
Para melhorar a navegação do robô sem fazer alterações físicas, sintonizamos as configurações de navegação nos seguintes arquivos de parâmetros (`nav2_params_realsense.yaml` e `nav2_params_sim.yaml`), alinhando-os com as correções de `nav2_params.yaml`:
*   **Correção de Velocidade Lateral**: Ajustado `min_y_velocity_threshold` de `0.5` para `0.001` (essencial para que o Nav2 não trave a navegação de robôs diferenciais).
*   **Tolerância a Atrasos**: Aumentada a tolerância de transformadas (`transform_tolerance`) no AMCL para `1.5` e no DWB (`FollowPath`) para `1.0`.
*   **Progress Checker**: Reduzido o raio mínimo de movimento exigido (`required_movement_radius`) para `0.3` e aumentado o tempo limite (`movement_time_allowance`) para `15.0` (evitando abortos inesperados de navegação).
*   **Segurança e Suavidade**: Desativado o plugin de recuperação agressiva por giro (`spin recovery`) mantendo apenas `backup` e `wait` (reduz risco de colisões em locais estreitos).

### 5. Launch Files Atualizados
*   `src/my_robot_bringup/launch/udh1_core.launch.py`: Modificado para carregar o executável `base_driver` em vez de `base_driver_pulse`.
*   `src/my_robot_bringup/launch/udh1_core_maping.launch.py`: Modificado para carregar o executável `base_driver`.
*   `src/my_robot_bringup/launch/navigation.launch.py`: Modificado para carregar o executável `base_driver` e reinserir o nó de segurança `safe_stop` ativo por padrão.

---

## Verification Plan & Steps for the Team

Como o robô necessita de validação física no laboratório com a base original, a equipe deve seguir estes passos de teste:

1.  **Validação com Rodas Suspensas (Estático)**:
    *   Suspender o robô para evitar contato com o chão.
    *   Iniciar a teleoperação:
        ```bash
        ros2 run serial_com_py wasd_teleop
        ```
    *   Verificar se a resposta dos motores atende aos setpoints com o TRIM antigo.
2.  **Validação de Navegação Autônoma**:
    *   Garantir que a velocidade lateral do Nav2 está definida como `0.001` nos costmaps e planners correspondentes.
    *   Executar o Nav2 com poses e verificar a ausência de abortamentos causados pelo SimpleProgressChecker.
