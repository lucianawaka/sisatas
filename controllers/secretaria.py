def adicionar_secretaria(conn, nome):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secretarias (nome) VALUES (?)", (nome,))
    conn.commit()

def listar_secretarias(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT id, nome FROM secretarias").fetchall()

def deletar_secretaria(conn, secretaria_id):
    """
    Deleta uma secretaria do banco de dados pelo ID.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secretarias WHERE id = ?", (secretaria_id,))
    conn.commit()
