import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

GOOGLE_DRIVE_FOLDER_ID = "1BNk3uSvj4PqA6yfIWqE_XC1f_NuL3FkM"
LOGS_FOLDER = "logs_capturas"

def inicializar_drive():

    try:
        gauth = GoogleAuth()

        gauth.LoadClientConfigFile("credenciais_drive.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        
        gauth.SaveCredentialsFile("credenciais_drive.txt")

        return GoogleDrive(gauth)
    except Exception as e:
        print(f"ERRO DE AUTENTICAÇÃO DO DRIVE: {e}")
        return None