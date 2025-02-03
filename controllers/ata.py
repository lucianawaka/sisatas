def adicionar_ata(conn, descricao, data, horario_inicio, horario_termino):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO atas (descricao, data, horario_inicio, horario_termino) VALUES (?, ?, ?, ?)",
        (descricao, data, horario_inicio, horario_termino)
    )
    conn.commit()

def listar_atas(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT id, descricao, data, horario_inicio, horario_termino FROM atas").fetchall()

def obter_dados_ata(conn, ata_id):
    """
    Busca e retorna os dados da ata e as suas falas.

    :param conn: Conexão com o banco de dados.
    :param ata_id: ID da ata.
    :return: uma tupla (descricao, data, falas), onde falas é uma lista de tuplas (id, secretario, fala).
    :raises ValueError: se a ata não for encontrada.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT descricao, data, horario_inicio, horario_termino FROM atas WHERE id = ?", (ata_id,))
    ata = cursor.fetchone()
    if not ata:
        raise ValueError("Ata não encontrada.")
    descricao, data, horario_inicio, horario_termino = ata

    falas = listar_falas_por_ata(conn, ata_id)
    return descricao, data, falas, horario_inicio, horario_termino


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
def buscar_atas_por_descricao(conn, descricao_parcial):
    """Busca atas que contenham a descrição informada."""
    cursor = conn.cursor()
    query = """
        SELECT id, descricao, data
        FROM atas
        WHERE descricao LIKE ?
    """
    return cursor.execute(query, (f"%{descricao_parcial}%",)).fetchall()
def deletar_ata(conn, ata_id):
    """Deleta uma ata específica e todas as falas associadas a ela."""
    cursor = conn.cursor()

    # Deleta todas as falas associadas à ata
    cursor.execute("DELETE FROM falas WHERE ata_id = ?", (ata_id,))

    # Deleta a ata
    cursor.execute("DELETE FROM atas WHERE id = ?", (ata_id,))

    conn.commit()

def editar_ata(conn, ata_id, nova_descricao, nova_data, novo_horario_inicio, novo_horario_termino):
    """Edita a descrição, data, horário de início e horário de término de uma ata específica."""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE atas SET descricao = ?, data = ?, horario_inicio = ?, horario_termino = ? WHERE id = ?",
        (nova_descricao, nova_data, novo_horario_inicio, novo_horario_termino, ata_id)
    )
    conn.commit()
