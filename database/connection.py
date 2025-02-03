import sqlite3

def get_connection():
    conn = sqlite3.connect("banco_de_dados_atas.db")
    return conn
def atualizar_banco(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE atas ADD COLUMN horario_inicio TEXT NOT NULL DEFAULT ''")
    except Exception as e:
        print("Erro ao adicionar a coluna 'horario_inicio' (possivelmente ela já existe):", e)
    try:
        cursor.execute("ALTER TABLE atas ADD COLUMN horario_termino TEXT NOT NULL DEFAULT ''")
    except Exception as e:
        print("Erro ao adicionar a coluna 'horario_termino' (possivelmente ela já existe):", e)
    conn.commit()
