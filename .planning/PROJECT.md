# UNIP Droidians Robotics (UD-H1 Navigation Stack)

## What This Is

O módulo de Navegação (Navigation Stack) para o robô UD-H1, focado no deslocamento autônomo, seguro e preciso em ambientes domésticos. O sistema utiliza a pilha de navegação **Nav2** (Navigation 2) do ROS 2 Humble, algoritmos de localização como AMCL (Adaptive Monte Carlo Localization) e mapeamento baseado em SLAM (Simultaneous Localization and Mapping) com o SLAM Toolbox, integrando sensores de distância LIDAR (RPLidar) e odometria baseada em encoders de rodas conectados via Serial a um Arduino.

## Core Value

Navegação autônoma segura, robusta e precisa do robô de serviço doméstico UD-H1 em cenários de competição (RoboCup@Home).

## Requirements

### Validated

- [x] Implementação da comunicação serial bidirecional estável com o Arduino (transmissão de velocidade linear/angular e recepção de odometria de encoders).
- [x] Integração física e configuração de driver do sensor LIDAR RPLidar.
- [x] Geração e validação de mapa estático 2D do ambiente de testes utilizando SLAM Toolbox.
- [x] Desenvolvimento de launch files unificados para inicialização do hardware real, localizadores AMCL e a pilha de navegação Nav2.

### Active

- [ ] Calibração dinâmica da odometria física (ajuste fino dos fatores de escala de rotação/translação e tratamento de inversões de eixos).
- [ ] Sintonia fina dos parâmetros de navegação do Nav2 (costmaps local/global, algoritmos de planejamento local como DWB/TEB e limites de aceleração).
- [ ] Implementação de nó ROS 2 para automatizar a execução de sequências de waypoints (metas domésticas).

### Out of Scope

- Integração total com câmera de profundidade (Intel RealSense) para filtragem de obstáculos 3D (diferido para marcos futuros para focar na calibração básica da odometria e laser 2D).

## Context

- **Subsistema**: O projeto é executado dentro do WSL2 (Ubuntu 22.04 LTS) integrado com o hardware embarcado real (Jetson + Arduino + LIDAR) ou em simulação no Gazebo Classic.
- **Odometria**: Baseada em contagem de pulsos de encoders com interrupções no Arduino e integrada no nó Python `base_driver_pulse`.
- **IDE**: Antigravity IDE conectada ao WSL2/Windows.

## Constraints

- **Tech Stack**: Python 3.10+ (venv), C++11/17, ROS 2 Humble, Nav2, SLAM Toolbox.
- **Interface Física**: Comunicação serial via USB (/dev/ttyACM0 para Arduino e /dev/ttyUSB0 para LIDAR) no WSL2/Ubuntu.

## Architecture & SOLID Guidelines

Para garantir que o código seja testável sem o ROS 2 ativo e altamente extensível, seguimos os seguintes princípios de Clean Architecture e SOLID:

### Separação de Middleware e Algoritmos
*   **Thin ROS Nodes (SRP - Single Responsibility Principle)**: Os nós ROS 2 (Python ou C++) atuam estritamente como adaptadores de barramento (interfaces de comunicação). Eles apenas assinam tópicos (`/scan`, `/odom`), publicam dados (`/cmd_vel`) e delegam toda lógica complexa de processamento para classes puras (Engines).
*   **Engine Core**: Toda lógica matemática, como planejamento de caminhos (Path Planning), cálculo de odometria refinada ou desvio de obstáculos, reside em classes puras separadas, sem qualquer herança ou acoplamento com classes ROS (`rclpy.node.Node` ou `rclcpp::Node`).
*   **Abstrações e Inversão de Dependência (DIP/OCP/LSP)**: Definição de interfaces abstratas centralizadas. Se um algoritmo de planejamento for alterado ou substituído, ele herda da classe abstrata base, permitindo troca imediata sem necessidade de reescrever ou alterar o nó ROS 2.

### Mensagens Estruturadas e Parâmetros
*   **Configuração Dinâmica**: Limiares de colisão, velocidade máxima, margens físicas e arquivos de mapas são externalizados em arquivos YAML e injetados via Launch files.
*   **Mensagens Customizadas**: Tráfego de dados estruturado com tipagem forte para relatar telemetria (status, posição no mapa) em vez de serializações genéricas (ex: JSON String).

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Uso de Arduino para processamento de encoders | Evitar perdas de pulsos de alta frequência no processamento principal do ROS 2 | — Validated |
| Protocolo serial baseado em string (`CMD:`/`ODO:`) | Simplicidade na depuração e processamento dos pacotes serial | — Validated |
| Uso do SLAM Toolbox (online async) | Melhor desempenho em ambientes dinâmicos domésticos em comparação com gmapping/cartographer padrão | — Validated |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-23 for Navigation transition*
