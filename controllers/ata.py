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
