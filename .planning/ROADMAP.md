# Roadmap: UNIP Droidians Robotics (UD-H1 Navigation Stack)

## Overview

O roadmap deste módulo foi estruturado para desenvolver a pilha de navegação do robô UD-H1, partindo da integração básica dos drivers de motores e odometria via serial com o Arduino, avançando para a integração dos sensores LIDAR e mapeamento SLAM, calibração dinâmica da odometria, sintonia fina da navegação do Nav2 e, por fim, a automação de trajetórias complexas baseadas em waypoints.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3, 4, 5): Planned milestone work
- Decimal phases (e.g., 3.1): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Driver de Base e Odometria** - Implementação da comunicação serial, comandos de movimentação e integração inicial de odometria (/odom e transformações).
- [/] **Phase 2: Mapeamento e Sensorização** - Driver do LIDAR RPLidar C1 integrado ao ROS 2 e geração do primeiro mapa estático via SLAM Toolbox.
- [ ] **Phase 3: Calibração de Odometria e Filtros** - Resolução de inversões no RViz, calibração fina de translação/rotação e sintonia inicial do localizador AMCL.
- [ ] **Phase 4: Configuração e Sintonia do Nav2** - Ajuste fino de costmaps local/global, planners de trajetória (TEB/DWB) e desvio de obstáculos dinâmicos em simulação e hardware real.
- [ ] **Phase 5: Automação de Waypoints (Metas Sequenciais)** - Criação de nó ROS 2 para controle sequencial de waypoints e envio de metas de navegação para competições.

## Phase Details

### Phase 1: Driver de Base e Odometria
**Goal**: Desenvolver a ponte serial com o Arduino e obter estimativas básicas de odometria.
**Depends on**: Nothing
**Requirements**: [DRV-01, DRV-02, DRV-03, ODOM-01]
**Success Criteria**:
  1. O nó `base_driver_pulse` se conecta ao Arduino e envia velocidades lineares/angulares corretas via serial.
  2. O nó recebe leituras dos encoders e publica dados de odometria no frame `odom` e transform `/odom -> /base_footprint`.
**Plans**: 2 plans (Completed)

### Phase 2: Mapeamento e Sensorização
**Goal**: Integrar o LIDAR e gerar o mapa inicial 2D do ambiente de testes.
**Depends on**: Phase 1
**Requirements**: [SLAM-01, SLAM-02, SLAM-03]
**Success Criteria**:
  1. O nó `sllidar_node` publica leituras de laser de alta densidade no tópico `/scan`.
  2. É gerado um mapa estático (`mapa_udh1.yaml` / `.pgm`) em ambiente de teste usando SLAM Toolbox.
**Plans**: 2 plans

### Phase 3: Calibração de Odometria e Filtros
**Goal**: Resolver desvios sistemáticos de odometria e calibrar filtros de laser e AMCL.
**Depends on**: Phase 2
**Requirements**: [ODOM-02, ODOM-03, SLAM-02]
**Success Criteria**:
  1. O robô se move em linha reta por 1 metro e rotaciona 360 graus, e o desvio reportado pela odometria em relação à posição real é menor que 5%.
  2. Ajuste dos fatores de escala de odometria no driver e resolução da inversão de direção exibida no RViz2.
  3. Nós AMCL carregam os parâmetros corretos do mapa e a nuvem de partículas converge durante o movimento.
**Plans**: 2 plans

### Phase 4: Configuração e Sintonia do Nav2
**Goal**: Sintonia fina da pilha de navegação autônoma e desvio de obstáculos.
**Depends on**: Phase 3
**Requirements**: [NAV-01, NAV-02, NAV-03, NAV-04]
**Success Criteria**:
  1. O robô desvia de obstáculos estáticos e móveis em tempo de execução sem sofrer colisões no mapa.
  2. Os costmaps local e global estão configurados com raio de inflação seguro condizente com a largura física do robô (25 cm).
  3. Navegação autônoma funcional no RViz2 enviando poses pelo botão "Nav2 Goal".
**Plans**: 2 plans

### Phase 5: Automação de Waypoints (Metas Sequenciais)
**Goal**: Permitir que o robô visite uma sequência de posições pré-definidas de forma automática.
**Depends on**: Phase 4
**Requirements**: [WP-01, WP-02]
**Success Criteria**:
  1. Implementação de nó ROS 2 `waypoint_navigator` que lê uma lista de coordenadas de um arquivo YAML e comanda o robô sequencialmente através do Nav2 Action Interface.
  2. Logs e telemetria claros sobre a chegada em cada ponto e tempo total de percurso.
**Plans**: 2 plans

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Driver de Base e Odometria | 2/2 | Completed | 2026-05-22 |
| 2. Mapeamento e Sensorização | 0/2 | Active | |
| 3. Calibração de Odometria e Filtros | 0/2 | Pending | |
| 4. Configuração e Sintonia do Nav2 | 0/2 | Pending | |
| 5. Automação de Waypoints (Metas Sequenciais) | 0/2 | Pending | |
