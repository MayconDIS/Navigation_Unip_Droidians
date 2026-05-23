# Guia de Configuração de Ambiente: UNIP Droidians - Visão Computacional

Este guia instrui o desenvolvedor sobre as etapas sequenciais para a configuração do ambiente local voltado ao módulo de Visão Computacional do robô UD-H1.

---

## Etapa 1: Subsistema Linux (WSL2)

Para instalar a distribuição recomendada no ambiente Windows, execute o comando abaixo no **Windows PowerShell Preview** (com privilégios de Administrador):

```powershell
wsl --install -d Ubuntu-22.04
```

* **Função**: Ativa os recursos opcionais do Windows necessários para execução do WSL2 e realiza a instalação limpa da distribuição Ubuntu 22.04 LTS.

---

## Etapa 2: Motor de Contêineres (Docker)

Para que a arquitetura em contêineres do projeto seja suportada, realize a integração do Docker Desktop com o WSL2:

1. Efetue o download e a instalação do **Docker Desktop** no Windows.
2. Inicie o Docker Desktop e acesse o menu de configurações (ícone de engrenagem).
3. Na seção **General**, verifique se a opção **Use the WSL 2 based engine** está selecionada.
4. Navegue até **Resources** > **WSL Integration**.
5. Habilite a integração global e ative o seletor correspondente à distribuição **Ubuntu-22.04**.
6. Clique em **Apply & Restart** para aplicar as configurações e reiniciar os serviços do Docker.

* **Função**: Disponibiliza o daemon do Docker nativo do host para a distribuição do WSL2, permitindo a execução de comandos `docker` e `docker-compose` diretamente no terminal Ubuntu.

---

## Etapa 3: Ambiente de Desenvolvimento (Antigravity IDE)

Siga os passos a seguir para conectar o Antigravity IDE ao ambiente do subsistema Linux:

1. Com o Antigravity IDE aberto, acesse o marketplace de extensões (`Ctrl+Shift+X`).
2. Busque e instale a extensão oficial **WSL** (da Microsoft).
3. No canto inferior esquerdo da tela da IDE, clique no botão de status remoto (ícone verde `><`) ou use o atalho `Ctrl+Shift+P` para abrir a paleta de comandos, digitando `WSL: Connect to WSL`. Selecione a distribuição **Ubuntu-22.04**.
4. Uma nova janela da IDE será aberta conectada ao subsistema. Abra a pasta do repositório contida no Linux.
5. Instale as seguintes extensões dentro do contexto remoto do WSL:
   * **Python**: Suporte a sintaxe, IntelliSense, refatoração e depuração.
   * **Docker**: Realce de sintaxe e gestão visual de imagens e contêineres.

---

## Etapa 4: Repositório e Versionamento

Dentro do terminal do **Ubuntu 22.04 LTS**, execute o comando de clonagem para obter a base de código do robô:

```bash
git clone https://github.com/roboticaunip/UNIP_Droidians_Robotics.git
```

* **Função**: Clona localmente o repositório oficial da divisão de robótica para o sistema de arquivos do subsistema Linux.

---

## Etapa 5: Isolamento de Dependências (Python venv)

Acesse o terminal do **Ubuntu 22.04 LTS**, navegue até o diretório do projeto e execute a sequência de comandos para provisionar o ambiente virtual e as bibliotecas exigidas:

```bash
# Atualização de pacotes locais e instalação do gerenciador pip e biblioteca venv
sudo apt update && sudo apt install -y python3-pip python3-venv

# Criação do diretório virtual do Python
python3 -m venv venv

# Ativação do ambiente virtual
source venv/bin/activate

# Atualização da ferramenta pip
pip install --upgrade pip

# Instalação das dependências do módulo de Visão Computacional
pip install opencv-python ultralytics mediapipe
```

* **Função de cada comando**:
  * `sudo apt update && sudo apt install...`: Atualiza a lista de pacotes apt e instala o compilador/interpretador Python 3 com as ferramentas de gerenciamento de dependências e ambientes virtuais.
  * `python3 -m venv venv`: Instala uma versão isolada do executável Python e do diretório de pacotes locais na pasta `venv`.
  * `source venv/bin/activate`: Aponta as variáveis de ambiente ativas do terminal para o diretório local do `venv`, isolando a instalação de pacotes globais do SO.
  * `pip install --upgrade pip`: Atualiza o gerenciador de pacotes para a versão estável mais recente.
  * `pip install opencv-python ultralytics mediapipe`: Instala a biblioteca OpenCV (processamento de imagem), Ultralytics (reconhecimento de objetos por YOLOv8) e MediaPipe (reconhecimento de gestos e mapeamento de pontos corporais).
