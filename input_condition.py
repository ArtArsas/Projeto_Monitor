#IMPORT DE FERRAMENTAS
import os
import datetime
import time
from PIL import Image
from pynput import keyboard
import mss
import pygetwindow as gw

os.system('cls')

#VAR DE CONFIG
FOLDER_NAME = "logs_capturas"
FILE_EXT = ".png"
FILE_CONFG = "config/target_config.txt"

#TARGET_W = "Chrome"

#CARREGA ARQUIVO DE CONFIGURAÇÃO
def carregar_file_config():
    uploaded_target = []
    try:
        with open(FILE_CONFG) as f:
            for linha in f:
                alvo_limpo = linha.strip().upper()
                if alvo_limpo:
                    uploaded_target.append(alvo_limpo)

        return uploaded_target
    except FileNotFoundError:
        print(f"Arquivo de configuração '{FILE_CONFG}' não encontrado. Usando valor padrão.")
        return ["CHROME"]
    except Exception as e:  
        print(f"Erro ao carregar o arquivo de configuração: {e}. Usando valor padrão.")
        return ["CHROME"]

#OBTEM TITULO DA JANELA ATIVA
def get_active_window():
    try:
        focus = gw.getActiveWindow()
        if focus:
            return focus.title
        return "N/A"
    except Exception:
        return "ERRO_JANELA"

#LOGICA DE CAPTURA
def commit_ps(window_title):

    tn = datetime.datetime.now()
    f_base = tn.strftime("%Y%m%d_%H%M%S")

    time.sleep(0.5)

    with mss.mss() as sct:
        for i, monitor in enumerate(sct.monitors[1:], 1):
            cap_image_data = sct.grab(monitor)
            f_name = f"PS_{f_base}_{i}{FILE_EXT}"
            save_path = os.path.join(FOLDER_NAME, f_name)

            cap_image = Image.frombytes("RGB", cap_image_data.size, cap_image_data.rgb)
            cap_image.save(save_path)
            print(f"\n[CAPTURA ACIONADA PELA TECLA ENTER] Salvo: Monitor {i} Salvo em: {save_path}")
            print(f"Janela Ativa:{window_title[:40]}")

#Logica do Listener
def on_press(key):
    gatilho_acionado = False
    alvo_encontrado = ""

    #FUNC TECLA ENTER + CHROME
    if key == keyboard.Key.enter:
        active_window = get_active_window()
        titulo_upper = active_window.upper()

        for alvo in PROGRAMAS_ALVO:
            alvo_limpo = alvo.strip()
            if alvo_limpo in titulo_upper:
                gatilho_acionado = True
                alvo_encontrado = alvo
                break

        if gatilho_acionado:
            print(f"\n[ALVO DETECTADO: {alvo_encontrado}] Janela Ativa: {active_window}")
            commit_ps(active_window)
        else:
            print(f"\n[ALVO NÃO DETECTADO] Janela Ativa: {active_window}. Nenhum programa alvo em execução.")

      
    #FUNC TECLA ESC PARA CANCELAR PROGRAMA
    if key == keyboard.Key.esc:
        print("\nTecla ESC pressionada. Encerrando o monitor de teclas...")
        return False 

if __name__ == "__main__":

    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    global PROGRAMAS_ALVO
    PROGRAMAS_ALVO = carregar_file_config()

    print("--- Monitor de Teclas Iniciado ---")
    print(f"Programas Alvo: {', '.join(PROGRAMAS_ALVO)}")
    print("Pressione ENTER para capturar a tela se o programa alvo estiver ativo.")
    print("Pressione ESC para encerrar o programa.")

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
            
    except KeyboardInterrupt:
        time.sleep(1)
    print("Programa finalizado com sucesso.")