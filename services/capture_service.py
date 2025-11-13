import os
import datetime
import time
from PIL import Image
import mss
from .db_service import registrar_log_captura

FOLDER_NAME = "logs_capturas"
FILE_EXT = ".png"

def commit_ps(window_title):

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

        if registrar_log_captura(f_base, 'GATILHO_TECLA', window_title, save_path):
            print(f"\n[CAPTURA ACIONADA PELA TECLA ENTER] Sucesso no Registro e Log!")
            print(f"Janela Ativa: {window_title[:40]} | Arquivo: {f_base}")
        else:
            print(f"\n[CAPTURA ACIONADA PELA TECLA ENTER] Captura OK, mas falha ao registrar no banco.")

    except Exception as e:
        print(f"!ERRO na Captura ou Salvamento: {e}!")