def adicionar_fala(conn, ata_descricao, secretario_nome, fala):
    
    cursor = conn.cursor()
    # Busca o ID da ata pelo número
    cursor.execute("SELECT id FROM atas WHERE descricao = ?", (ata_descricao,))
    ata_id = cursor.fetchone()

    # Busca o ID do secretário pelo nome
    cursor.execute("SELECT id FROM secretarios WHERE nome = ?", (secretario_nome,))
    secretario_id = cursor.fetchone()

    if ata_id and secretario_id:
        cursor.execute(
            "INSERT INTO falas (ata_id, secretario_id, fala) VALUES (?, ?, ?)",
            (ata_id[0], secretario_id[0], fala),
        )
        conn.commit()
    else:
        raise ValueError("Ata ou Secretário não encontrado.")

def listar_falas(conn):
    cursor = conn.cursor()
    return cursor.execute(
        "SELECT falas.id, atas.numero AS ata, secretarios.nome AS secretario, falas.fala "
        "FROM falas "
        "INNER JOIN atas ON falas.ata_id = atas.id "
        "INNER JOIN secretarios ON falas.secretario_id = secretarios.id"
    ).fetchall()
def listar_falas_por_ata(conn, ata_id):
    cursor = conn.cursor()
    return cursor.execute(
        """
        SELECT falas.id, secretarios.nome, falas.fala
        FROM falas
        INNER JOIN secretarios ON falas.secretario_id = secretarios.id
        WHERE falas.ata_id = ?
        """,
        (ata_id,),
    ).fetchall()

def limpar_todas_as_entidades(conn):
    """Deleta todas as atas e falas do banco de dados."""
    cursor = conn.cursor()

    # Deleta todas as falas
    cursor.execute("DELETE FROM falas")

    # Deleta todas as atas
    cursor.execute("DELETE FROM atas")

    conn.commit()

def atualizar_fala(conn, fala_id, novo_texto):
    """
    Atualiza o texto de uma fala no banco de dados.
    :param conn: Conexão com o banco de dados.
    :param fala_id: ID da fala a ser atualizada.
    :param novo_texto: Novo texto da fala.
    """
    cursor = conn.cursor()
    query = "UPDATE falas SET fala = ? WHERE id = ?"
    cursor.execute(query, (novo_texto, fala_id))
    conn.commit()
def deletar_fala(conn, fala_id):
    """
    Deleta uma fala específica do banco de dados.
    :param conn: Conexão com o banco de dados.
    :param fala_id: ID da fala a ser deletada.
    """
    cursor = conn.cursor()
    query = "DELETE FROM falas WHERE id = ?"
    cursor.execute(query, (fala_id,))
    conn.commit()
