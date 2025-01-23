def adicionar_secretario(conn, nome, secretaria_nome):
    cursor = conn.cursor()
    # Busca o ID da secretaria pelo nome
    cursor.execute("SELECT id FROM secretarias WHERE nome = ?", (secretaria_nome,))
    secretaria_id = cursor.fetchone()
    if secretaria_id:
        cursor.execute(
            "INSERT INTO secretarios (nome, secretaria_id) VALUES (?, ?)",
            (nome, secretaria_id[0]),
        )
        conn.commit()
    else:
        raise ValueError("Secretaria não encontrada.")

def listar_secretarios(conn):
    cursor = conn.cursor()
    return cursor.execute(
        "SELECT secretarios.id, secretarios.nome, secretarias.nome AS secretaria FROM secretarios "
        "INNER JOIN secretarias ON secretarios.secretaria_id = secretarias.id"
    ).fetchall()

def get_secretaria_by_secretario(conn, secretario_nome):
    """
    Retorna o nome da secretaria vinculada ao secretário especificado.
    """
    cursor = conn.cursor()
    query = """
        SELECT s.nome 
        FROM secretarios sec
        INNER JOIN secretarias s ON sec.secretaria_id = s.id
        WHERE sec.nome = ?
    """
    cursor.execute(query, (secretario_nome,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else "Sem secretaria"
