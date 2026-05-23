# Requirements: UNIP Droidians Robotics (UD-H1 Navigation Stack)

**Defined:** 2026-05-23
**Core Value:** Navegação autônoma segura, robusta e precisa do robô de serviço doméstico UD-H1 em cenários de competição.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Base Driver & Communication

- [ ] **DRV-01**: O sistema estabelece uma conexão serial confiável com o Arduino Mega/Uno a 115200 bps (/dev/ttyACM0).
- [ ] **DRV-02**: O nó traduz mensagens do ROS 2 `geometry_msgs/Twist` (`cmd_vel`) em velocidades diferenciais de rodas esquerda e direita.
- [ ] **DRV-03**: O firmware do Arduino implementa um controle de velocidade proporcional e integral (PI) para manter o robô na velocidade desejada.
- [ ] **DRV-04**: O sistema desliga os motores de forma segura se nenhum comando do computador principal for recebido dentro de 500ms (Watchdog serial).

### Odometry Integration

- [ ] **ODO-01**: O nó `base_driver_pulse` calcula e publica a estimativa de odometria no frame `odom` e no TF `/odom` -> `/base_footprint`.
- [ ] **ODO-02**: A odometria é calibrada dinamicamente, de forma que o robô apresente erro linear e angular inferior a 5% em trajetos de teste.
- [ ] **ODO-03**: O nó publica o estado das juntas (`sensor_msgs/JointState`) correspondente à rotação das rodas no RViz2 de forma consistente.

### SLAM & Mapping

- [ ] **SLAM-01**: O driver do sensor RPLidar C1 inicializa com sucesso a 460800 baud e publica leituras de laser de alta densidade no tópico `/scan`.
- [ ] **SLAM-02**: O sistema de filtros de laser remove leituras falsas ou ruídos que prejudicam o custo local da navegação.
- [ ] **SLAM-03**: O desenvolvedor pode gerar, salvar e carregar mapas estáticos do ambiente doméstico em arquivos `.yaml`/`.pgm`.

### Navigation Stack (Nav2)

- [ ] **NAV-01**: O localizador AMCL carrega o mapa estático e converge a nuvem de partículas de forma correta ao receber comandos de navegação.
- [ ] **NAV-02**: O sistema de costmaps local e global calcula corretamente os obstáculos reais baseados nas varreduras do LIDAR e nos mapas estáticos.
- [ ] **NAV-03**: O planejador de trajetórias gera trajetórias suaves e livres de colisões, operando dentro dos limites físicos do robô.
- [ ] **NAV-04**: O robô desvia dinamicamente de obstáculos inesperados surgindo em sua rota com tempo de resposta ágil.

### Waypoint Execution

- [ ] **WP-01**: O sistema permite a definição de múltiplos pontos de interesse (coordenadas espaciais) a serem percorridos em uma sequência configurável.
- [ ] **WP-02**: O sistema envia a sequência de poses ao Nav2, monitorando os estados de conclusão (sucesso, falha ou timeout de cada waypoint) e reportando o status.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Detecção de pessoas ou rostos integrados na navegação | A detecção visual e processamento inteligente pertencem ao subsistema de Visão Computacional separado, conforme TDP. |
| Integração 3D com câmera de profundidade na V1 | Para manter o foco na integridade básica do sistema diferencial e segurança, usaremos apenas LIDAR 2D na primeira fase. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DRV-01 | Phase 1 | Validated |
| DRV-02 | Phase 1 | Validated |
| DRV-03 | Phase 1 | Validated |
| DRV-04 | Phase 1 | Validated |
| ODOM-01 | Phase 1 | Validated |
| ODOM-02 | Phase 3 | Active |
| ODOM-03 | Phase 1 | Validated |
| SLAM-01 | Phase 2 | Validated |
| SLAM-02 | Phase 3 | Active |
| SLAM-03 | Phase 2 | Validated |
| NAV-01 | Phase 3 | Active |
| NAV-02 | Phase 4 | Pending |
| NAV-03 | Phase 4 | Pending |
| NAV-04 | Phase 4 | Pending |
| WP-01 | Phase 5 | Pending |
| WP-02 | Phase 5 | Pending |
