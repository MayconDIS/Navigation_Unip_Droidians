# Relatório de Análise Técnica e Práticas de Engenharia: Módulo de Navegação UD-H1

Este documento apresenta uma análise técnica detalhada do módulo de navegação do robô **UD-H1 (UNIP Droidians)**, comparando o estado de desenvolvimento com os padrões industriais de engenharia de software e controle recomendados para competições de robótica de serviço (RoboCup@Home).

---

## 1. Arquitetura de Navegação Recomendada para Competição (Target)

De acordo com o Team Description Paper (TDP) de 2026, o robô UD-H1 deve operar em ambientes domésticos altamente dinâmicos. A pilha técnica recomendada envolve:
*   **Frequência de Controle Elevada**: Frequência de controle de malha fechada das rodas entre 50Hz e 100Hz no firmware para garantir que a cinemática diferencial responda instantaneamente aos desvios físicos.
*   **Controle Robusto (PI + Feedforward)**: Uso de controle proporcional e integral com rampa de Feedforward de aceleração para vencer a inércia dos motores pesados de hoverboard.
*   **Consistência Cinemática no ROS**: Sinais e eixos de odometria linear/angular rigorosamente positivos ao ir para a frente e girar para a esquerda (anti-horário), permitindo convergência rápida do AMCL.
*   **Mecanismos de Segurança (Watchdogs)**: Nós dedicados para interromper a movimentação do robô em caso de derrapagem, patinação ou colisões não previstas no mapa.

---

## 2. Comparativo de Engenharia: Estado Inicial vs. Produção (Target)

Abaixo está o quadro comparativo relacionando a nossa implementação do pacote de navegação com os padrões industriais:

| Critério | Padrões de Produção Recomendados | Estado Atual (Navegação UD-H1) | Avaliação Técnica e Ganhos da Transição |
| :--- | :--- | :--- | :--- |
| **Ponte de Odometria** | **Drivers Nativos em C++**: Baixa latência e alta consistência de thread com o core do ROS 2. | **Nó Adaptador em Python**: Conexão simples via `serial_com_py` com rampa de aceleração. | **Fácil Calibração**. O nó em Python facilita a calibração de escala e testes iterativos de direção retilínea. |
| **Frequência de Controle** | **Frequências de 50Hz a 100Hz** no microcontrolador para motores de alto torque. | **Frequência de 10Hz**: Firmware original de 100ms mantido sob demanda da equipe. | **Estável e Conhecido**. A equipe optou por manter a frequência de 10Hz original para evitar riscos elétricos/mecânicos. |
| **Tratamento de Obstáculos** | **Detecção 3D**: Uso de câmera de profundidade (RealSense) projetando nuvem de pontos no costmap 2D. | **LIDAR 2D (Filtrado)**: Costmap com dados 2D limpos de ruídos pelo filtro angular 180° frontal. | **Prevenção de Colisões Básica**. Suficiente para paredes e móveis baixos; precisará de RealSense em fases futuras para objetos altos/baixos fora da linha do laser. |
| **Segurança e Watchdogs** | **Mapeamento de desvios por odometria**: Parada automática em caso de divergência de trajetória. | **Distance Watchdog Ativo**: Nó que calcula o comprimento do plano e desativa o robô se andar mais do que o limite. | **Excelente nível de segurança**. Impede o robô de forçar os motores de hoverboard se ficar travado fisicamente. |

---

## 3. Próximos Passos Recomendados para Desenvolvimento
1.  **Validação Física do Eixo**: Realizar testes lineares de 1m utilizando o script `wasd_teleop` para calibração do fator de escala.
2.  **Integração do RealSense no Costmap**: Reativar a projeção da RealSense D435 (`navigation_realsense.launch.py`) para evitar colisões com quinas de mesas em competições domésticas.
3.  **Encapsulamento Docker**: Criar o container Docker correspondente para deploy do build do workspace.
