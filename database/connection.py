import sqlite3

def get_connection():
    conn = sqlite3.connect("banco_de_dados_atas.db")
    return conn
def atualizar_banco(conn):
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE secretarios ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT 1")
    conn.commit()
