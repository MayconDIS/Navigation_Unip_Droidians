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

# Mude para a branch sintonizada
git checkout feature/restauracao-base-otimizacao-nav2
git pull origin feature/restauracao-base-otimizacao-nav2
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

*   **W / S**: Move para frente / trás ($0.2\text{ m/s}$)
*   **A / D**: Rotaciona para esquerda / direita ($0.6\text{ rad/s}$)
*   **Barra de Espaço**: Para o robô imediatamente.
