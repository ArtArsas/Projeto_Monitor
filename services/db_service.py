import os
import sqlite3
import datetime


DB_FOLDER = "data"
DB_NAME = f"{DB_FOLDER}/target_monitor.db"

def inicializar_banco():

    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS logs(
            data_hora_id TEXT PRIMARY KEY,
            tipo_evento TEXT,
            janela_ativa TEXT,
            caminho_arquivo TEXT,
            timestamp_insercao DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def registrar_log_captura(f_base, tipo_evento, window_title, save_path):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO logs (data_hora_id, tipo_evento, janela_ativa, caminho_arquivo)
                       VALUES (?, ?, ?, ?)
                       """, (f_base, tipo_evento, window_title, save_path))
        conn.commit()
        conn.close()
        return True
    
    except sqlite3.Error as e:
        print(f"ERRO SQL: Não foi possível registrar no banco de dados: {e}")
        return False