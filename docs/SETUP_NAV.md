# Guia de Configuração de Ambiente: UNIP Droidians - Navegação

Este guia instrui o desenvolvedor sobre as etapas sequenciais para a configuração do ambiente local voltado à compilação, simulação e execução do módulo de Navegação do robô UD-H1.

---

## Passo 1: Subsistema Linux (WSL2) e ROS 2 Humble

O projeto requer o sistema **Ubuntu 22.04 LTS** com a instalação do **ROS 2 Humble Hawksbill** (versão Desktop ou Base). 

1.  Certifique-se de que o ROS 2 está configurado em seu shell:
    ```bash
    source /opt/ros/humble/setup.bash
    ```

---

## Passo 2: Instalação das Dependências do Sistema

Instale os pacotes principais do Nav2, SLAM Toolbox e utilitários de TF/Xacro necessários para a compilação:

```bash
sudo apt update && sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-xacro \
  ros-humble-joint-state-publisher-gui \
  ros-humble-laser-filters \
  ros-humble-teleop-twist-keyboard \
  python3-serial
```

---

## Passo 3: Configuração Física das Portas Seriais (WSL2 / Robô Real)

Se você estiver rodando no robô físico real via WSL2, é necessário dar permissão de escrita e leitura para os periféricos USB que conectam o Arduino e o LIDAR:

```bash
# Permissão para o Arduino (/dev/ttyACM0) e RPLidar (/dev/ttyUSB0)
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyUSB0
```

*Nota: No Windows, pode ser necessário mapear as portas COM para o WSL2 utilizando a ferramenta `usbipd`.*

---

## Passo 4: Compilação do Workspace

Navegue até a raiz do seu repositório de Navegação e compile os pacotes utilizando o `colcon`:

```bash
# Compilar todo o workspace
colcon build --symlink-install

# Carregar o workspace compilado
source install/setup.bash
```

*Dica: O parâmetro `--symlink-install` permite alterar os scripts Python (como drivers e teleoperação) sem a necessidade de rodar o `colcon build` novamente a cada modificação.*

---

## Passo 5: Inicialização e Teste

### A. Simulação (Gazebo)
Para testar a cinemática e a navegação em ambiente virtual simulado:
```bash
ros2 launch udh1_gazebo gazebo_nav2.launch.py
```

### B. Robô Real
Para rodar a odometria física, leitura de laser e orquestração do Nav2 no robô de competição:
```bash
ros2 launch my_robot_bringup navigation.launch.py
```

### C. Teleoperação WASD Customizada
Em um terminal separado, após carregar o workspace:
```bash
ros2 run serial_com_py wasd_teleop
```
Use as teclas `W`, `A`, `S`, `D` e `Espaço` para comandar e testar as direções retilíneas do robô.
