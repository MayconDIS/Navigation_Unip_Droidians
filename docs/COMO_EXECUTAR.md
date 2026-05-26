# Guia de Execução no Ubuntu (WSL2 / Nativo)

Este guia fornece o passo a passo necessário para compilar e executar a pilha de navegação do robô **UD-H1** no ambiente Ubuntu (seja em instalação nativa ou usando WSL2 integrado com o Windows).

---

## 1. Configuração e Sincronização do Repositório

Antes de compilar, garanta que você está na pasta correta e na branch com as configurações de hardware estáveis e os parâmetros sintonizados:

```bash
# Navegue até a pasta do repositório no Linux
cd ~/athome_ws/src/Navigation_Unip_Droidians

# Atualize os metadados do repositório
git fetch origin

# Mude para a branch principal
git checkout main
git pull origin main
```

---

## 2. Permissões de Dispositivos USB (Apenas Hardware Real)

Se você estiver se comunicando com o robô físico via cabo USB, certifique-se de liberar o acesso de leitura/escrita para o Arduino e o sensor LIDAR no terminal do Ubuntu:

```bash
# Libera acesso para a porta serial do Arduino
sudo chmod 666 /dev/ttyACM0

# Libera acesso para a porta serial do RPLidar C1
sudo chmod 666 /dev/ttyUSB0
```

> **Dica para WSL2**: No PowerShell do Windows (como Administrador), utilize o comando `usbipd list` e `usbipd attach --wsl --busid <BUSID>` para redirecionar as portas USB físicas do Windows para o kernel do WSL2.

---

## 3. Compilação do Workspace

Navegue até a pasta raiz do seu workspace ROS 2 (`athome_ws`) e compile utilizando o `colcon`:

```bash
# Retorne à raiz do workspace
cd ~/athome_ws

# Realize a compilação utilizando links simbólicos para arquivos estáticos e Python
colcon build --symlink-install
```

---

## 4. Inicialização do Ambiente do ROS 2

Para cada terminal que você abrir para controlar o robô, execute as seguintes variáveis de ambiente:

```bash
# Carrega a instalação base do ROS 2 Humble
source /opt/ros/humble/setup.bash

# Carrega os pacotes e nós do robô compilados no workspace
source install/setup.bash
```

---

## 5. Comandos de Execução

Você pode inicializar diferentes partes do sistema dependendo do cenário de testes:

### Opção A: Executar a Base de Hardware e Sensor LIDAR (Mapeamento / Teleoperação)
Utilizado para verificar o funcionamento estático dos motores e leituras de laser sem inicializar toda a pilha de navegação autônoma. Executa os drivers e o modelo URDF:
```bash
ros2 launch my_robot_bringup udh1_core_maping.launch.py
```

### Opção B: Executar a Navegação Autônoma Completa (Nav2 + AMCL + RViz2 + Laser)
Lança o mapa de simulação/teste, a localização probabilística AMCL (com tolerâncias de TF sintonizadas) e o planejador global/local do Nav2. Abre o RViz2 automaticamente:
```bash
ros2 launch my_robot_bringup navigation.launch.py
```

### Opção C: Controle Manual via Teclado (WASD Teleop)
Para movimentar o robô manualmente usando o terminal, abra um **novo terminal**, repita o comando de carregamento do ambiente (`source install/setup.bash`) e rode:
```bash
ros2 run serial_com_py wasd_teleop
```

*   **W / S**: Move para frente / trás ($0.15\text{ m/s}$)
*   **A / D**: Rotaciona para esquerda / direita ($0.6\text{ rad/s}$)
*   **Barra de Espaço**: Para o robô imediatamente.

---

### Opção D: Controle Manual via Joystick (Controle de Videogame)

Para controlar o robô usando um gamepad (como o GameSir T4 Lite / Xbox 360), siga o procedimento abaixo:

1. **Instalar dependências no Ubuntu (WSL2 / Nativo):**
   ```bash
   sudo apt update
   sudo apt install -y ros-humble-joy joystick
   ```

2. **Conectar e redirecionar o controle no WSL2:**
   - No Windows, abra o PowerShell como Administrador.
   - Encontre o BUSID do controle (reconhecido como *Controlador XBOX 360*):
     ```powershell
     usbipd list
     ```
   - Vincule e redirecione o dispositivo para o WSL2 (se apresentar o erro `Device busy`, feche a Steam e outros mapeadores de controles no Windows):
     ```powershell
     usbipd attach --wsl --busid <BUSID>
     ```

3. **Verificar e liberar permissões no Ubuntu:**
   ```bash
   # Certifica-se de que o controle foi detectado como dispositivo de input no Linux
   ls -l /dev/input/js*
   
   # Concede permissão de leitura para o nó do ROS
   sudo chmod 666 /dev/input/js0
   ```

4. **Executar a Teleoperação por Joystick:**
   Abra um novo terminal no Ubuntu, carregue o ambiente do workspace e execute:
   ```bash
   ros2 launch my_robot_bringup joystick_teleop.launch.py
   ```
   *   **Como controlar:** Mantenha o botão **LB** (botão morto de segurança) pressionado e use o **analógico esquerdo** para se movimentar (frente/trás e curvas). Soltar o botão **LB** para o robô imediatamente.

---

## 6. Fluxo de Trabalho de Execução Passo a Passo (Para Testar Hoje)

Para movimentar o robô (seja por teclado ou por controle de videogame), você precisará de **dois terminais** no Ubuntu.

### Passo 1: Inicializar o Ambiente do Robô (Terminal 1)
No **Terminal 1** do Ubuntu, configure o ambiente:
```bash
cd ~/athome_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Agora escolha se deseja testar em **Simulação** ou no **Robô Real**:

#### Cenário A: Executar em Simulação (Gazebo + RViz2)
Excelente para demonstrar ou testar código sem necessidade do hardware físico:
```bash
ros2 launch udh1_gazebo gazebo.launch.py
```
> Isso abrirá a janela gráfica do Gazebo Classic e o RViz2 na sua tela.

#### Cenário B: Executar no Robô Físico Real
Conecte os cabos do Arduino e do LIDAR ao computador e rode:
```bash
# Conceder permissão de leitura/escrita para as portas USB/Serial
sudo chmod 666 /dev/ttyACM0
sudo chmod 666 /dev/ttyUSB0

# Inicializar os drivers da base física, sensores e modelo URDF
ros2 launch my_robot_bringup udh1_core_maping.launch.py
```
> **Nota**: Mantenha este terminal aberto. Ele roda os drivers principais que recebem a velocidade do teleop e enviam para os motores.


---

### Passo 2: Escolher o Método de Teleoperação (Terminal 2)
Abra um **novo terminal (Terminal 2)** no Ubuntu, navegue e configure o ambiente:
```bash
cd ~/athome_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
```

Agora, execute **uma** das opções abaixo:

#### Opção A: Controle via Teclado (WASD)
```bash
ros2 run serial_com_py wasd_teleop
```
*   **Movimentação**: Clique nas teclas **W** (Frente), **S** (Trás), **A** (Curva Esquerda) e **D** (Curva Direita).
*   **Parada de Emergência**: Pressione a barra de **Espaço** para parar o robô imediatamente.

#### Opção B: Controle via Joystick (GameSir T4 Lite)
*(Antes de rodar, certifique-se de ter conectado o controle no PowerShell do Windows como Administrador via: `usbipd attach --wsl --busid 1-11`)*

No **Terminal 2**, libere a permissão do joystick no Linux e inicie a execução:
```bash
# Libera acesso ao dispositivo de joystick
sudo chmod 666 /dev/input/js0

# Inicializa o joy_node e o tradutor de comandos
ros2 launch my_robot_bringup joystick_teleop.launch.py
```
*   **Movimentação**: Mantenha pressionado o botão **LB** (botão de segurança) e empurre o **analógico esquerdo** para se movimentar.
*   **Parada de Emergência**: Apenas solte o botão **LB** (ou desligue o controle) e o robô irá parar de forma instantânea.


