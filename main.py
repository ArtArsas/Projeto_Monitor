# Módulo Orquestrador: main.py

# --- IMPORTS DE SERVIÇOS ---
import os
import time
import threading
import logging
from pynput import keyboard

# Importa todas as lógicas dos módulos
from services.target_service import carregar_file_config, carregar_words_config
from services.window_service import get_active_window
from services.capture_service import commit_ps
from services.db_service import inicializar_banco


# --- VARIÁVEIS GLOBAIS DE ESTADO E RISCO ---
FOLDER_NAME = "logs_capturas" 
FOLDER_LOG = "logs"
DB_FOLDER = "data"
DB_NAME = "target_monitor.db" 
LOG_FILE = os.path.join(FOLDER_LOG, "sistema_monitor.log")
DB_FULL_PATH = os.path.join(DB_FOLDER, DB_NAME)

# --- MODO DESENVOLVEDOR - POSSIBILITA O ENCERRAMENTO DO MONITOR COM A TECLA ESC
MODO_DESENVOLVEDOR = True
NIVEL_LOG = "INFO"

TECLAS_BUFFER = []  
BUFFER_SIZE = 50 
PROGRAMAS_ALVO = [] 
PALAVRAS_DE_RISCO = [] 
INTERVALO_CAPTURA = 5

STOP_MONITORING = threading.Event()
TIMER_GLOBAL = None

# --- GERA LOGS no diretório logs

def registrar_logs(mensagem, nivel="info"):
    if nivel == "info":
        logging.info(mensagem)
    elif nivel == "warning":
        logging.warning(mensagem)
    elif nivel == "error":
        logging.error(mensagem)

# --- CAPTURA PERIÓDICA AUTOMÁTICA ---
def start_monitoring():

    registrar_logs(f"[AUTO] Config Monitoramento Automatico: {INTERVALO_CAPTURA} segundos")
    print(f"[AUTO] Config Monitoramento Automatico: {INTERVALO_CAPTURA} segundos")

    #CONTROLADOR STOP_MONITORING
    if STOP_MONITORING.is_set():
        return
    #FIM CONTROLADOR

    try:
        #1. Verifica active window
        active_window = get_active_window()
        titulo_upper = active_window.upper()
        alvo_encontrado = None

        #2. Cruza com a target list
        for alvo in PROGRAMAS_ALVO:
            if alvo.strip() in titulo_upper:
                alvo_encontrado = alvo.strip()
                break
            
        #3. Trigger de captura
        if alvo_encontrado:
            registrar_logs(f"[AUTO] Monitoramento Periodico: Alvo '{alvo_encontrado}' detectado. Capturando...")
            commit_ps(active_window, tipo_evento='CAPTURA_PERIODICA')

    except Exception as e:
        registrar_logs(f"[AUTO] Erro no ciclo de monitoramento: {e}")

    #CONTROLADOR STOP_MONITORING    
    if not STOP_MONITORING.is_set():
        global TIMER_GLOBAL

        TIMER_GLOBAL = threading.Timer(INTERVALO_CAPTURA, start_monitoring)
        TIMER_GLOBAL.start()
    #FIM CONTROLADOR

# --- LÓGICA AUXILIAR: VERIFICAÇÃO DE RISCO ---
def verificar_buffer(risco_words):
    """
    Verifica se a string do buffer de memória (TECLAS_BUFFER) contém alguma palavra de risco.
    """
    buffer_texto = "".join(TECLAS_BUFFER).upper()
    
    for palavra in risco_words:
        if palavra in buffer_texto:
            return palavra 
            
    return None 


# --- LÓGICA PRINCIPAL DE EXECUÇÃO ---
def on_press(key):
    
    # AÇÃO 1: KEYLOGGING DE BAIXO RISCO
    try:
        char = key.char
        TECLAS_BUFFER.append(char)
        
        if len(TECLAS_BUFFER) > BUFFER_SIZE:
            TECLAS_BUFFER.pop(0) 
            
        risco_encontrado = verificar_buffer(PALAVRAS_DE_RISCO)
        
        if risco_encontrado:
            active_window = get_active_window()
            
            commit_ps(active_window, tipo_evento='RISCO_CONTEUDO', log_risco=risco_encontrado)
            
            TECLAS_BUFFER.clear()
            registrar_logs(f"\n ALERTA DE RISCO DETECTADO: '{risco_encontrado}' na janela: {active_window[:40]}")

    except AttributeError:
        pass

    # AÇÃO 2: GATILHO DE CAPTURA MANUAL (ENTER)
    if key == keyboard.Key.enter:
        
        gatilho_acionado = False
        alvo_encontrado = "Desconhecido" # Inicializa com valor padrão
        active_window = get_active_window()
        titulo_upper = active_window.upper()

        for alvo in PROGRAMAS_ALVO:
            alvo_limpo = alvo.strip()
            if alvo_limpo in titulo_upper:
                gatilho_acionado = True
                alvo_encontrado = alvo_limpo # <--- CORREÇÃO AQUI: Define a variável
                break
        
        # APLICAÇÃO DO GATILHO
        if gatilho_acionado:
            commit_ps(active_window, tipo_evento='GATILHO_TECLA') 
            # Agora a variável alvo_encontrado existe e tem valor!
            registrar_logs(f"\n[GATILHO ATIVO - ENTER] Acionado pelo alvo '{alvo_encontrado}'...")
        else:
            registrar_logs(f"\n[GATILHO INATIVO] ENTER - Janela: {active_window[:40]}... (Alvo não encontrado)")

    # Função de Cancelamento de Monitoramento Manual
    if key == keyboard.Key.esc:
        if MODO_DESENVOLVEDOR:
            registrar_logs("\nTecla ESC pressionada. Encerrando o monitor de teclas...")
            STOP_MONITORING.set()
            if TIMER_GLOBAL:
                TIMER_GLOBAL.cancel()
            return False   
        else:
            pass
if __name__ == "__main__":

    # 1. CONFIGURAÇÕES INICIAIS
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    if not os.path.exists(DB_FOLDER): 
        os.makedirs(DB_FOLDER)

    if not os.path.exists(FOLDER_LOG): 
        os.makedirs(FOLDER_LOG)

    #--- LOGGING CONFIG
    logging.basicConfig(
        filename=LOG_FILE,
        level=NIVEL_LOG.upper(),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    registrar_logs("\n ::::::: INICIANDO SISTEMA :::::::")

    # Limpa a tela apenas se estiver em modo DEV
    if MODO_DESENVOLVEDOR:
        os.system('cls')
        print("--- MODO DESENVOLVEDOR ATIVO ---")
        print("logs sendo gravados em:", LOG_FILE)
    else:
        pass
   
    inicializar_banco(DB_FULL_PATH)

    # 2. CARREGAMENTO DE CONFIGURAÇÕES
    PROGRAMAS_ALVO = carregar_file_config()
    PALAVRAS_DE_RISCO = carregar_words_config()

    start_monitoring()
    registrar_logs("\n ::::::: SISTEMA INICIADO COM SUCESSO:::::::")

    # 3. INICIAÇÃO DO LISTENER
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    
    except KeyboardInterrupt:
        time.sleep(1)
    print("Programa finalizado com sucesso.")