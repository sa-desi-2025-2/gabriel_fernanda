import mysql.connector
from mysql.connector import Error
import os

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = 'mapainterativo'

def conectar_bd():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=3307
        )
        
        if conexao.is_connected():
            print("Conexão ao MySQL bem-sucedida!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None