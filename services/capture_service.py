import os
import datetime
import time
from PIL import Image
import mss

# Importa o serviço de banco de dados (Caminho Relativo)
from .db_service import registrar_log_captura

# VAR DE CONFIG
FOLDER_NAME = "logs_capturas"
FILE_EXT = ".jpeg"

# MUDANÇA: Agora aceita os argumentos de alerta
def commit_ps(active_window, tipo_evento, log_risco=None):

    tn = datetime.datetime.now()
    f_base = tn.strftime("%Y%m%d_%H%M%S")
    time.sleep(0.5)

    try:
        with mss.mss() as sct:
            for i, monitor in enumerate(sct.monitors[1:], 1):
                cap_image_data = sct.grab(monitor)
                f_name = f"PS_{f_base}_{i}{FILE_EXT}"
                save_path = os.path.join(FOLDER_NAME, f_name) 

                cap_image = Image.frombytes("RGB", cap_image_data.size, cap_image_data.rgb)
                cap_image.save(save_path)
                
        # REGISTRA NO BANCO DE DADOS
        # MUDANÇA: Passa active_window e log_risco para o db_service
        if registrar_log_captura(f_base, tipo_evento, active_window, save_path, log_risco):
            print(f"\n[SUCESSO] Registro salvo. Janela: {active_window[:30]}...")
        else:
             print(f"\n[ERRO] Falha ao registrar no banco.")

    except Exception as e:
        print(f"❌ ERRO na Captura ou Salvamento: {e}")