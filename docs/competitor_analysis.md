# Relatório de Análise Técnica e Práticas de Engenharia: Módulo de Visão UD-H1

Este documento apresenta uma análise técnica detalhada do módulo de visão do robô **UD-H1 (UNIP Droidians)**, comparando o estado de desenvolvimento inicial com os padrões de engenharia de software de nível industrial recomendados para competições de robótica de serviço (como a RoboCup@Home). 

Além disso, integra as diretrizes técnicas documentadas nos Team Description Papers (TDPs) de 2026 localizados na pasta `documents/`.

---

## 1. Informações Consumidas dos Documentos (`documents/`)

A análise dos arquivos `RoboCup@Home Korea 2026 - UnipDroidians TDP.pdf` e `Robocup@Home - UnipDroidians Korea 2026.pdf` revelou as seguintes especificações técnicas do robô **UD-H1**:

### Hardware do UD-H1
*   **Processamento Embarcado**: Centralizado em uma placa **NVIDIA Jetson** executando Ubuntu 22.04 LTS + **ROS 2 Humble**, auxiliada por um notebook Dell de suporte.
*   **Atuadores da Base**: Dois motores de hoverboard de 6.5" controlados via drivers RioRand ZS-X11H, integrados ao ROS 2.
*   **Manipulador**: Um braço robótico SCARA de 6 graus de liberdade (6-DOF) controlado por motores de passo NEMA 17 via Arduino Uno + CNC Shield.
*   **Sensores de Visão**: 
    *   Câmera Intel RealSense D435/D457 para percepção 3D, desvio de obstáculos e navegação.
    *   Webcam USB convencional para captura de imagem padrão.
*   **Outros Sensores**: 2x RPLIDAR C1 (mapeamento/SLAM), sonar HC-SR04 e Sharp GP2D120 (curto alcance).

### Software do UD-H1
*   **Localização/Navegação**: SLAM com Cartographer (2D) e ORB-SLAM3 (visual 3D) fundidos via Filtro de Kalman Estendido (EKF), alimentando o stack **Nav2**.
*   **Manipulação**: Controle via **MoveIt 2** integrado com algoritmo de *visual servoing* (servovisualização) para correção de posicionamento baseada nas coordenadas do YOLOv8.
*   **Interação Humano-Robô (HRI)**: Reconhecimento de voz Vosk + Google Speech, Rasa NLU/SpaCy para diálogos, e árvores de comportamento (**ros2_behavior_tree**).
*   **Infraestrutura (Docker)**: Conforme o TDP (Seção 3.4), *cada subsistema do robô deve operar em containers Docker isolados*, garantindo reprodutibilidade e rápida implantação.

---

## 2. Comparativo de Engenharia: Arquitetura Inicial vs. Padrões de Produção (Target)

Abaixo está o quadro comparativo relacionando o estado inicial do pacote `droidians_vision` com os padrões de engenharia recomendados para sistemas robóticos em produção:

| Critério | Padrões de Produção Recomendados | Estado Inicial (`droidians_vision`) | Avaliação Técnica e Ganhos da Transição |
| :--- | :--- | :--- | :--- |
| **Organização do Repositório** | **Multi-pacotes**: Divisão clara entre o pacote de nós de processamento (`droidians_vision`) e interfaces de comunicação (`droidians_vision_msgs`). | **Mono-pacote**: Um único pacote ROS 2 concentrando todos os nós, scripts e definições de mensagens. | **Melhoria na modularidade**. Separar as definições de mensagens permite que outros nós do robô assinem tópicos sem depender de dependências de visão pesadas como OpenCV e MediaPipe. |
| **Modelagem de Dados** | **Tipos Customizados**: Uso de mensagens estruturadas (`.msg` customizadas do ROS 2) com tipagem forte para tráfego eficiente. | **Tipos Genéricos + JSON**: Publicava landmarks do MediaPipe serializados como string JSON (`std_msgs/String`). | **Segurança de tipos (Type Safety)**. A eliminação do JSON serializado como String reduz o overhead de parsing e permite ferramentas nativas de visualização (como Rviz2) e filtragem de tópicos. |
| **Gerenciamento de Parâmetros** | Arquivos de parâmetros padronizados em `.yaml` externos, carregados dinamicamente no launch. | Parâmetros de thresholds e caminhos declarados inline dentro do código Python dos nós. | **Facilidade de ajuste**. Centralizar a configuração facilita a calibração de câmeras e thresholds no ambiente real de competição sem necessidade de alterar o código. |
| **DevOps / Deploy** | Conteinerização completa via **Docker** e **Docker Compose** mapeando periféricos e displays locais. | Sem suporte a Docker estruturado no repositório. | **Garantia de portabilidade**. O uso do Docker garante que a stack execute de forma idêntica na Jetson embarcada e nos notebooks de simulação, isolando dependências do Python. |
| **Testes e Qualidade** | Validação sintática contínua dos scripts e conformidade com as diretrizes do ROS 2. | Execução de testes manuais pontuais sem script de build unificado. | **Robustez e estabilidade**. Evita erros em tempo de execução no robô real através de verificações pré-compilação e validação do pipeline. |

---

## 3. Avaliação Técnica e Prontidão de Software

> [!TIP]
> **A refatoração do módulo de visão eleva o UD-H1 a um patamar profissional de nível de competição.**
> Embora a implementação inicial dos nós do ROS 2 (`yolo_detector.py`, `mediapipe_tracker.py`, `video_publisher.py` e `vision_viewer.py`) contasse com excelente tratamento de erros e integridade algorítmica, o acoplamento de tipos de dados (JSON string) e a ausência de Docker dificultavam a integração e portabilidade exigidas pelo TDP de 2026. A nova estrutura multi-pacotes e conteinerizada atende integralmente a essas necessidades.

---

## 4. Plano de Ação e Melhorias Estruturais Concluídas

Para implementar as melhores práticas levantadas, as seguintes melhorias técnicas estruturais foram realizadas:

### 1. Criação das Mensagens ROS 2 Personalizadas (`droidians_vision_msgs`)
Substituição do tráfego de String JSON no tópico `/vision/landmarks` por mensagens de ROS 2 tipadas e eficientes, definindo arquivos `.msg`:
*   `Landmark.msg` (contendo `int32 id`, `float64 x`, `float64 y`, `float64 z`, `float64 visibility`)
*   `HandLandmarks.msg` (contendo `string label` e `Landmark[] landmarks`)
*   `PoseLandmarks.msg` (contendo `Landmark[] landmarks`)
*   `LandmarksTelemetry.msg` (mensagem agregadora contendo Header, mãos e pose)

### 2. Externalização das Configurações para Arquivo YAML
Criação do diretório `config/` dentro de `droidians_vision` com o arquivo `params.yaml`:
```yaml
yolo_detector:
  ros__parameters:
    model_path: "yolov8n.pt"
    threshold: 0.5

mediapipe_tracker:
  ros__parameters:
    mode: "both"
    min_detection_confidence: 0.5
    min_tracking_confidence: 0.5
```
Ajuste do `vision_pipeline.launch.py` para injetar os parâmetros em tempo de execução.

### 3. Dockerização dos Subsistemas de Visão
Desenvolvimento da infraestrutura de build e deploy isolada:
*   `Dockerfile` otimizado compilando o workspace completo com OpenCV, PyTorch e MediaPipe.
*   `docker-compose.yml` para orquestração de containers com mapeamento do display X11/WSLg e comunicação via rede host.

---

## 5. Próximos Passos de Evolução

Com o alinhamento arquitetural concluído, os próximos passos sugeridos para o desenvolvimento são:
1.  **Integração com MoveIt 2**: Consumir os tópicos estruturados de `/vision/landmarks` para guiar os movimentos de aproximação do manipulador SCARA.
2.  **Validação na Jetson Embarcada**: Clonar o repositório no hardware embarcado do UD-H1 e testar o desempenho do Docker container com aceleração de GPU (se disponível).
3.  **Expansão de HRI**: Conectar a telemetria do MediaPipe à árvore de comportamento (`ros2_behavior_tree`) para triggers de interação baseada em gestos.
