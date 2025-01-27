def adicionar_secretaria(conn, nome):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secretarias (nome) VALUES (?)", (nome,))
    conn.commit()

def listar_secretarias(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT id, nome FROM secretarias").fetchall()

def atualizar_secretaria(conn, secretaria_id, novo_nome):
    """
    Atualiza o nome de uma secretaria no banco de dados.
    :param conn: Conexão com o banco de dados.
    :param secretaria_id: ID da secretaria a ser atualizada.
    :param novo_nome: Novo nome da secretaria.
    """
    cursor = conn.cursor()
    query = "UPDATE secretarias SET nome = ? WHERE id = ?"
    cursor.execute(query, (novo_nome, secretaria_id))
    conn.commit()


def deletar_secretaria(conn, secretaria_id):
    """
    Deleta uma secretaria do banco de dados pelo ID.
    """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM secretarias WHERE id = ?", (secretaria_id,))
    conn.commit()

def get_secretaria_por_id(conn, secretaria_id):
    """
    Retorna os dados de uma secretaria pelo ID.
    """
    cursor = conn.cursor()
    query = "SELECT id, nome FROM secretarias WHERE id = ?"
    cursor.execute(query, (secretaria_id,))
    resultado = cursor.fetchone()
    if resultado:
        return {"id": resultado[0], "nome": resultado[1]}
    return None
