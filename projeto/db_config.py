import mysql.connector
from mysql.connector import Error
import os

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = os.environ.get('DB_PASSWORD', 'root')
DB_PORT = 3307
DB_NAME = 'mapainterativo'

def conectar_bd():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME, 
            port=DB_PORT
        )
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        conexao = None

    return conexao
