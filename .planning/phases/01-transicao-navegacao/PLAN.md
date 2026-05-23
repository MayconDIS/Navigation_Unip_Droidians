# Transição de Escopo para Módulo de Navegação (UD-H1 Navigation Stack)

Este plano descreve as alterações necessárias nos arquivos de planejamento do diretório `.planning/` para que o repositório passe a refletir o estado de desenvolvimento, requisitos e roadmap do módulo de **Navegação** (Navigation Stack) do robô UD-H1, em vez do módulo de Visão Computacional.

## Proposed Changes

Faremos modificações nos quatro arquivos principais de planejamento do repositório para refletir o stack de navegação do ROS 2 Humble.

### Planning Artifacts

#### [MODIFY] [PROJECT.md](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/.planning/PROJECT.md)
*   **Título**: Alterar para `# UNIP Droidians Robotics (UD-H1 Navigation Stack)`.
*   **Descrição**: Atualizar a definição para focar na pilha de navegação baseada no ROS 2 Humble, Nav2, SLAM Toolbox e drivers de hardware (RPLIDAR, Arduino).
*   **Core Value**: Definir como "Navegação autônoma segura, robusta e precisa do robô de serviço doméstico UD-H1".
*   **Requisitos**:
    *   Marcar os requisitos de driver de base, odometria de roda, mapeamento SLAM inicial e arquivos de launch do Nav2 como concluidos.
    *   Adicionar requisitos ativos de calibração fina de odometria, sintonia de costmaps e envio de waypoints sequenciais.
*   **Contexto**: Atualizar com a execução local de simulação (Gazebo) e integração física com o Arduino e LIDAR.

#### [MODIFY] [ROADMAP.md](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/.planning/ROADMAP.md)
*   Reestruturar o roadmap em 5 fases realistas alinhadas com o estado atual do repositório:
    1.  **Fase 1: Driver de Base e Odometria** (Concluído) - Comunicação serial com Arduino e cálculo de odometria em `serial_com_py`.
    2.  **Fase 2: Mapeamento e Sensorização** (Concluído) - Driver do RPLidar e geração de mapa inicial via SLAM Toolbox.
    3.  **Fase 3: Calibração de Odometria e Filtros** (Ativa/Atual) - Correção fina de fatores de escala, inversão no RViz e sintonia inicial do localizador AMCL.
    4.  **Fase 4: Configuração e Sintonia do Nav2** (Pendente) - Ajuste dos costmaps local/global, desvio de obstáculos dinâmicos e seleção de planejadores (TEB/DWB).
    5.  **Fase 5: Automação de Waypoints (Metas Sequenciais)** (Pendente) - Nó ROS 2 de missão para navegação sequencial em tarefas domésticas.

#### [MODIFY] [REQUIREMENTS.md](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/.planning/REQUIREMENTS.md)
*   Remover todos os requisitos de YOLOv8 e MediaPipe.
*   Adicionar novos requisitos funcionais e não-funcionais de navegação:
    *   `DRV-01` a `DRV-04` (Comunicação serial com Arduino, controle de motores e telemetria).
    *   `ODO-01` a `ODO-03` (Cálculo de odometria, publicação no TF `/odom` e calibração de escala).
    *   `SLAM-01` a `SLAM-03` (Mapeamento 2D, filtragem de laser e mapas estáticos).
    *   `NAV-01` a `NAV-04` (Navegação guiada pelo Nav2, AMCL, costmaps local/global, desvio de obstáculos).
    *   `WP-01` e `WP-02` (Execução de caminhos por waypoints/pontos de interesse).

#### [MODIFY] [STATE.md](file:///c:/Users/mayco/Documents/GitHub/Navigation_Unip_Droidians/.planning/STATE.md)
*   Mudar o estado atual de "concluído" (do módulo de Visão) para ativo na **Fase 3 (Calibração de Odometria e Filtros)**.
*   Registrar o progresso atualizado (Fases 1 e 2 100% completas).

---

## Verification Plan

### Manual Verification
1.  Verificar se os comandos do GSD (/gsd-progress) reconhecem e exibem a nova árvore de fases corretamente após as mudanças nos arquivos.
2.  Garantir que a consistência das dependências de fases em `ROADMAP.md` e `REQUIREMENTS.md` esteja correta.
