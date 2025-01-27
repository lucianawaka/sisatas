def adicionar_secretario(conn, nome, secretaria_nome):
    cursor = conn.cursor()
    # Busca o ID da secretaria pelo nome
    cursor.execute("SELECT id FROM secretarias WHERE nome = ?", (secretaria_nome,))
    secretaria_id = cursor.fetchone()
    if secretaria_id:
        # Insere o secretário com a flag 'ativo' como padrão (1)
        cursor.execute(
            "INSERT INTO secretarios (nome, secretaria_id, ativo) VALUES (?, ?, 1)",
            (nome, secretaria_id[0]),
        )
        conn.commit()
    else:
        raise ValueError("Secretaria não encontrada.")

def listar_secretarios(conn, incluir_inativos=False):
    cursor = conn.cursor()
    # Ajusta a query com base na flag para incluir ou não secretários inativos
    if incluir_inativos:
        query = """
            SELECT secretarios.id, secretarios.nome, secretarias.nome AS secretaria, secretarios.ativo 
            FROM secretarios
            INNER JOIN secretarias ON secretarios.secretaria_id = secretarias.id
        """
        return cursor.execute(query).fetchall()
    else:
        query = """
            SELECT secretarios.id, secretarios.nome, secretarias.nome AS secretaria, secretarios.ativo 
            FROM secretarios
            INNER JOIN secretarias ON secretarios.secretaria_id = secretarias.id
            WHERE secretarios.ativo = 1
        """
        return cursor.execute(query).fetchall()

def get_secretaria_by_secretario(conn, secretario_nome):
    """
    Retorna o nome da secretaria vinculada ao secretário especificado.
    Inclui apenas secretários ativos.
    """
    cursor = conn.cursor()
    query = """
        SELECT s.nome 
        FROM secretarios sec
        INNER JOIN secretarias s ON sec.secretaria_id = s.id
        WHERE sec.nome = ? AND sec.ativo = 1
    """
    cursor.execute(query, (secretario_nome,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else "Sem secretaria"

def ativar_secretario(conn, secretario_id):
    """
    Ativa um secretário desativado (muda a flag 'ativo' para 1).
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE secretarios SET ativo = 1 WHERE id = ?", (secretario_id,))
    conn.commit()

def desativar_secretario(conn, secretario_id):
    """
    Desativa um secretário (muda a flag 'ativo' para 0).
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE secretarios SET ativo = 0 WHERE id = ?", (secretario_id,))
    conn.commit()


def editar_secretario(conn, secretario_id, novo_nome, nova_secretaria_nome):
    cursor = conn.cursor()
    # Busca o ID da nova secretaria pelo nome
    cursor.execute("SELECT id FROM secretarias WHERE nome = ?", (nova_secretaria_nome,))
    nova_secretaria_id = cursor.fetchone()
    if nova_secretaria_id:
        # Atualiza os dados do secretário
        cursor.execute(
            "UPDATE secretarios SET nome = ?, secretaria_id = ? WHERE id = ?",
            (novo_nome, nova_secretaria_id[0], secretario_id),
        )
        conn.commit()
    else:
        raise ValueError("Secretaria não encontrada.")
    
def get_secretario_por_id(conn, secretario_id):
    """
    Retorna os dados do secretário (nome e secretaria) pelo ID.
    """
    cursor = conn.cursor()
    query = """
        SELECT secretarios.nome, secretarias.nome
        FROM secretarios
        INNER JOIN secretarias ON secretarios.secretaria_id = secretarias.id
        WHERE secretarios.id = ?
    """
    cursor.execute(query, (secretario_id,))
    return cursor.fetchone()

