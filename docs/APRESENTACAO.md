# UNIPDroidians - Módulo de Navegação (UD-H1 Navigation Stack)
**Website:** [unipdroidians.com](http://unipdroidians.com)

## 🔧 Sobre o projeto  
UNIPDroidians é o grupo de robótica da UNIP empenhado em desenvolver soluções para robôs domésticos e participar da RoboCup At Home. Este repositório reúne o código-fonte, configurações de navegação, simulação e drivers de controle de movimentação da base diferencial do robô **UD-H1**:

- Integração com ROS 2 Humble e o framework **Nav2** (Navigation 2).
- Localização AMCL (Adaptive Monte Carlo Localization) e mapeamento SLAM via **SLAM Toolbox**.
- Driver Python de ponte serial (`serial_com_py`) e nó de monitoramento de segurança (`distance_watchdog`).
- Firmwares de baixo nível do Arduino (`Arduino/`) originais baseados em interrupções estáveis de PCINT e loop de 10Hz.
- Modelo cinemático/visual em URDF/Xacro (`udh1_description`) e simulação física no Gazebo Classic (`udh1_gazebo`).

## 📁 Conteúdo do repositório
- `/src` — Código-fonte dos pacotes do ROS 2 Humble (drivers, simulação, bringups, mapas e configurações do Nav2)
- `/Arduino` — Códigos do firmware e bibliotecas do Arduino para controle de motores e leitura de encoders
- `/mapas` — Arquivos de mapa de ocupação 2D (.yaml e .pgm) e configurações do RViz2
- `/docs` — Manuais de instalação, guias de setup da navegação, análises técnicas e relatórios
- `/.planning` — Metadados de planejamento das fases do projeto via GSD workflow

## 🤝 Contribuição  
Contribuidores são bem-vindos! Para contribuir:  

1. Faça um fork deste repositório  
2. Crie uma branch com a feature ou correção (`feature/xyz`)  
3. Commit suas mudanças e envie um Pull Request  
