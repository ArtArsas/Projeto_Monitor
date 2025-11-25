import sqlite3
import datetime

# --- LOGICA AUXILIAR: DDL DO BANCO DE DADOS ---
def inicializar_banco(db_path):
    """Cria o banco de dados e a tabela 'logs' se não existirem."""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL (DDL): Adicionada a coluna 'risco_detectado'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            data_hora_id TEXT PRIMARY KEY,
            tipo_evento TEXT,
            janela_ativa TEXT, 
            caminho_arquivo TEXT,
            risco_detectado TEXT,
            timestamp_insercao DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    conn.close()

# --- LOGICA DML: REGISTRAR LOG ---
def registrar_log_captura(f_base, tipo_evento, active_window, save_path, log_risco=None):
    """Insere um novo registro de captura na tabela 'logs'."""
    # Precisamos saber onde está o banco. 
    # O ideal é passar o path, mas para simplificar vamos assumir o padrão 'data/target_monitor.db' 
    # ou você pode passar o db_path como argumento extra se quiser ser muito estrito.
    # Vamos usar o caminho hardcoded da pasta data por enquanto para facilitar:
    db_path_interno = "data/target_monitor.db"

    try:
        conn = sqlite3.connect(db_path_interno)
        cursor = conn.cursor()
        
        # SQL (DML): Insere o registro incluindo risco_detectado
        cursor.execute("""
            INSERT INTO logs (data_hora_id, tipo_evento, janela_ativa, caminho_arquivo, risco_detectado) 
            VALUES (?, ?, ?, ?, ?)
        """, (f_base, tipo_evento, active_window, save_path, log_risco))
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ ERRO SQL: Não foi possível registrar no banco de dados: {e}")
        return False