# Módulo Orquestrador: main.py
# --- IMPORT DOS SERVIÇOS ---
import os
import time
from pynput import keyboard

# Serviços Modulares 
from services.target_service import carregar_file_config
from services.window_service import get_active_window
from services.capture_service import commit_ps
from services.db_service import inicializar_banco

os.system ('cls')

# VAR DE CONFIG (Pasta de Logs)
FOLDER_NAME = "logs_capturas"

# LÓGICA de EXECUÇÃO
def on_press(key):

    gatilho_acionado = False
    alvo_encontrado = ""

    # Função principal de monitoramento "TECLA ENTER"
    if key == keyboard.Key.enter:

        active_window = get_active_window()
        titulo_upper = active_window.upper()

        # Loop FOR para checar todos os alvos da lista de target
        for alvo in PROGRAMAS_ALVO:
            alvo_limpo = alvo.strip()
            if alvo_limpo in titulo_upper:
                gatilho_acionado = True
                alvo_encontrado = alvo
                break
        
        # Aplicação do Gatilho
        if gatilho_acionado:
            print(f"\n[GATILHO ATIVO - ENTER] Acionado pelo alvo '{alvo_encontrado}' na janela: {active_window[:40]}...")
            commit_ps(active_window)
        else:
            print(f"\n[GATILHO INATIVO] ENTER - Janela: {active_window[:40]}... (Alvo não encontrado na lista)")

    # Função de Cancelamento de Monitoramento Manual
    if key == keyboard.Key.esc:
        print("\nTecla ESC pressionada. Encerrando o monitor de teclas...")
        return False
    
if __name__ == "__main__":

    # 1. CONFIGURAÇÕES INICIAIS DDL E PASTAS
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    
    inicializar_banco()

    # 2. CARREGAMENTO DE TARGET (PREENCHIMENTO DE VARIAVEL GLOBAL PROGRAMAS_ALVO)
    global PROGRAMAS_ALVO
    PROGRAMAS_ALVO = carregar_file_config()

    print("--- Monitor de Teclas Iniciado ---")
    print(f"Programas Alvo: {', '.join(PROGRAMAS_ALVO)}")
    print("Pressione ENTER para capturar a tela se o programa alvo estiver ativo.")

    # 3. INICIAÇÃO DO LISTENER
    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    
    except KeyboardInterrupt:
        time.sleep(1)
    print("Programa finalizado com sucesso.")
