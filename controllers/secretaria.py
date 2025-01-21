def adicionar_secretaria(conn, nome):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secretarias (nome) VALUES (?)", (nome,))
    conn.commit()

def listar_secretarias(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT id, nome FROM secretarias").fetchall()
