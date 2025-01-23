import sqlite3

def get_connection():
    conn = sqlite3.connect("banco_de_dados_atas.db")
    return conn
