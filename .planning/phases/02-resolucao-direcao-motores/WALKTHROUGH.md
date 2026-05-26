# Walkthrough: Restauração da Base Física, Otimização de Navegação e Teleoperação

Este walkthrough documenta as alterações finais e validadas da **Fase 2** para estabilização física do robô, sintonia fina de navegação autônoma de alto nível e opções de controle manual (teclado e joystick).

---

## Changes Made

### 1. Restauração e Estabilização Física (Arduino e Python)
*   **Reversão**: Devido a problemas de derrapagem e instabilidade no controle de baixo nível anterior, restauramos o firmware original do Arduino ([odometrypulse-malha.ino](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/Arduino/odometrypulse-malha/odometrypulse-malha.ino)) e o driver da base ([base_driver.py](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/base_driver.py)) a partir do backup estável `Navigation-main`.
*   **TRIM Estático**: Mantido o ajuste de TRIM estático para alinhamento físico estável das rodas.
*   **Segurança**: O nó `safe_stop` foi integrado de volta nos launchs para proteção contra colisões frontais.

### 2. Sintonia Fina do Nav2 e AMCL (Alto Nível)
*   **Arquivos de Parâmetros**: Configurados e sincronizados em `nav2_params.yaml`, `nav2_params_realsense.yaml` e `nav2_params_sim.yaml`.
*   **Ajustes Críticos**:
    - Frequência de planejamento reduzida para `5.0 Hz` para aliviar carga de processamento.
    - Tolerância a latência de TF (`transform_tolerance`) aumentada de `1.0s` para `1.5s` no AMCL e de `0.2s` para `1.0s` no controlador DWB.
    - Limiar de progresso (`SimpleProgressChecker`) relaxado de `0.5m` para `0.3m` e timeout aumentado para `15.0s`.
    - Remoção de recuperações agressivas de rotação (plugin `spin`) para locais apertados.

### 3. Teleoperação via Teclado (Retentivo / Latching)
*   **Implementação**: Refatorado o nó [wasd_teleop.py](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/wasd_teleop.py).
*   **Velocidade**: Velocidade linear ajustada para o limite seguro de `0.15 m/s` (reduzido de 0.20 m/s).
*   **Comportamento**: Roda continuamente no clique da tecla (W/S/A/D) e para apenas ao pressionar **Espaço** ou enviar sinal de interrupção (Ctrl+C).

### 4. Teleoperação via Joystick (GameSir T4 Lite / Xbox 360)
*   **Código**: Criado o script [joystick_teleop.py](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/src/serial_com_py/serial_com_py/joystick_teleop.py).
*   **Controle Seguro**: Implementado botão morto (**LB**) de segurança. O robô só se move ao segurar LB e utilizar o analógico esquerdo. Soltar o botão interrompe o movimento de imediato.
*   **Launch File**: Criado [joystick_teleop.launch.py](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/src/my_robot_bringup/launch/joystick_teleop.launch.py) inicializando o `joy_node` e o tradutor juntos.

---

## Verification & Usage Steps

A compilação do workspace foi validada com sucesso via `colcon build`. Para operar os controles, siga as instruções atualizadas no [COMO_EXECUTAR.md](file:///c:/Users/mayco/Documents/PROJECTS/Navigation_Unip_Droidians/docs/COMO_EXECUTAR.md).

### Resolução de Conexão do Controle (erro `Device busy` no `usbipd`):
Se o redirecionamento USB travar no Windows:
1. Reinicie o sistema operacional Windows para descarregar hooks ativos.
2. Feche a **Steam** e qualquer outro mapeador de gamepad em execução na barra de tarefas.
3. Altere o modo de emparelhamento do controle segurando `Home + A` ou `Home + X`.
4. Plugue o cabo em outra porta USB para obter um novo BUSID antes de rodar `usbipd attach`.
