# IMPORTS
import os
from PIL import ImageGrab
import datetime
import time

# VARIAVEIS 
FOLDER_NAME = "logs_capturas"
FILE_EXT = ".png"
INTERVALO = 5

# CONFIG

if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)

print(f"Capturas de tela serão salvas na pasta: {FOLDER_NAME} e irá capturar uma as fotos a cada {INTERVALO} segundos.")
print("Pressione Ctrl+C para parar a captura.")

# FUNÇÃO DE CAPTURA DE TELA

while True:
    try:
        tempo_agora = datetime.datetime.now()
        nome_base = tempo_agora.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = "PRT_" + nome_base + FILE_EXT

        caminho_salvar = os.path.join(FOLDER_NAME, nome_arquivo)    
        imagem_capturada = ImageGrab.grab() 
        imagem_capturada.save(caminho_salvar)

        print(f"Captura salva na data [{nome_base}]")

        time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("Captura de tela interrompida pelo usuário.")
        break

