def adicionar_ata(conn, descricao, data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO atas (descricao, data) VALUES (?, ?)", (descricao, data))
    conn.commit()

def listar_atas(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT id, descricao, data FROM atas").fetchall()
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
