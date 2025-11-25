import tkinter as tk
from tkinter import messagebox
import os 
import subprocess

LOGS_FOLDER = "logs_capturas"

def open_folder_logs():

    path = os.path.abspath(LOGS_FOLDER)

    if not os.path.exists(path):
        messagebox.showwarning("Aviso", f" A pasta de logs não existe.")
        return
    
    try:
        subprocess.run(['start', '', path], shell=True, check=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir a pasta. Erro: {e}")

# --- Configuração da Janela Tkinter ---
root = tk.Tk()
root.title("Acesso ao Monitor")
root.geometry("350x150") 

# Label de Instrução
label = tk.Label(root, text="Clique no botão para acessar os registros:")
label.pack(pady=10)

# Botão para Abrir a Pasta
btn_abrir = tk.Button(root, 
                      text="📂 Abrir Pasta de Prints",
                      command=open_folder_logs) # Liga o botão à função
btn_abrir.pack(pady=10)

# Iniciar o loop principal da janela
root.mainloop()