# Módulo Orquestrador: main.py

# --- IMPORTS DE SERVIÇOS ---
import os
import time
from pynput import keyboard

# Importa todas as lógicas dos módulos
from services.target_service import carregar_file_config, carregar_words_config
from services.window_service import get_active_window
from services.capture_service import commit_ps
from services.db_service import inicializar_banco


# --- VARIÁVEIS GLOBAIS DE ESTADO E RISCO ---
FOLDER_NAME = "logs_capturas" 
DB_FOLDER = "data"
DB_NAME = "target_monitor.db" 
DB_FULL_PATH = os.path.join(DB_FOLDER, DB_NAME)

TECLAS_BUFFER = []  
BUFFER_SIZE = 50 
PROGRAMAS_ALVO = [] 
PALAVRAS_DE_RISCO = [] 

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
            print(f"\n🚨🚨 ALERTA DE RISCO DETECTADO: '{risco_encontrado}' na janela: {active_window[:40]} 🚨🚨")

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
            print(f"\n[GATILHO ATIVO - ENTER] Acionado pelo alvo '{alvo_encontrado}'...")
        else:
            print(f"\n[GATILHO INATIVO] ENTER - Janela: {active_window[:40]}... (Alvo não encontrado)")

    # Função de Cancelamento de Monitoramento Manual
    if key == keyboard.Key.esc:
        print("\nTecla ESC pressionada. Encerrando o monitor de teclas...")
        return False
    

if __name__ == "__main__":
    
    os.system('cls')

    # 1. CONFIGURAÇÕES INICIAIS
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    if not os.path.exists(DB_FOLDER): 
        os.makedirs(DB_FOLDER)
    
    inicializar_banco(DB_FULL_PATH)

    # 2. CARREGAMENTO DE CONFIGURAÇÕES
    PROGRAMAS_ALVO = carregar_file_config()
    PALAVRAS_DE_RISCO = carregar_words_config()

    # 3. INICIAÇÃO DO LISTENER
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    
    except KeyboardInterrupt:
        time.sleep(1)
    print("Programa finalizado com sucesso.")