def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS secretarias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS secretarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        secretaria_id INTEGER,
        ativo BOOLEAN NOT NULL DEFAULT 1, -- Flag para indicar se o secretário está ativo ou não
        FOREIGN KEY (secretaria_id) REFERENCES secretarias (id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS atas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        data TEXT NOT NULL,
        horario_inicio TEXT NOT NULL,
        horario_termino TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS falas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ata_id INTEGER,
        secretario_id INTEGER,
        fala TEXT NOT NULL,
        FOREIGN KEY (ata_id) REFERENCES atas (id),
        FOREIGN KEY (secretario_id) REFERENCES secretarios (id)
    )
    ''')
    conn.commit()
