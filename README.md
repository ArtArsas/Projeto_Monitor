# 🖥️ Monitor de Atividade Condicional (Código Mentor Leigo)

Este projeto é um software de **monitoramento de *background*** em Python, focado em registrar atividades específicas (captura de tela e log de banco de dados) apenas quando programas pré-definidos (os **Alvos**) estão ativos, acionado por um gatilho de teclado (**ENTER**).

O projeto adota a prática de **modularização**, separando a lógica de banco de dados e configuração em módulos independentes para facilitar a manutenção.

---

### 🚀 Funcionalidades Chave

* **Gatilho Condicional Inteligente:** A captura de tela só é acionada se a tecla `ENTER` for pressionada **E** a janela ativa contiver uma palavra-chave definida na lista de alvos (Ex: "CHROME" ou "DISCORD").
* **Lista de Alvos Externa:** Programas monitorados são carregados dinamicamente do arquivo `config/target_config.txt`, permitindo atualizações sem mexer no código principal.
* **Captura Multi-Monitor:** Utiliza a biblioteca `mss` para capturar **todos os monitores conectados**, salvando cada monitor em um arquivo de imagem separado.
* **Logs Estruturados (SQLite):** Registra cada evento de captura em um banco de dados local (`rastreamento_monitor.db`), armazenando o caminho do arquivo, a janela ativa e a data/hora exata.
* **Execução em *Background*:** Opcional via `PyInstaller`, para rodar de forma invisível no sistema operacional.

---

### ⚙️ Stack Tecnológica e Dependências

O projeto requer a instalação das seguintes bibliotecas Python:

| Componente | Ferramenta/Linguagem | Finalidade |
| :--- | :--- | :--- |
| **Linguagem Base** | Python 3.x | Lógica principal e orquestração. |
| **Monitoramento** | `pynput`, `pygetwindow` | Ouvinte de teclado e leitura do título da janela ativa. |
| **Captura de Tela** | `mss`, `Pillow` | Captura eficiente de multi-monitores e manipulação de imagem. |
| **Banco de Dados** | `sqlite3` (Nat.) | Armazenamento estruturado de logs. |

**Comando Único para Instalação de Dependências:**

```bash
py -m pip install Pillow pynput mss pygetwindow
