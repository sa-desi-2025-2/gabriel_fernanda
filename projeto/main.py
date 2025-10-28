from db_config import conectar_bd
from mysql.connector import Error

def consultar_dados(conexao):
    """Exemplo de como usar a conexão para fazer uma consulta."""
    
    with conexao.cursor() as cursor:
        try:
            cursor.execute("SELECT DATABASE();")
            banco_atual = cursor.fetchone()
            print(f"Você está conectado ao banco: {banco_atual[0]}")
        except Error as e: 
            print(f"Erro ao executar a consulta: {e}")

def criar_tabela_usuarios(conexao):
    """Cria a tabela 'usuarios' se ela não existir."""
    
    with conexao.cursor() as cursor:
        try:
            sql_create_table = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(sql_create_table)
            conexao.commit() 
            print("Tabela 'usuarios' verificada/criada com sucesso.")
            
        except Error as e:
            print(f"Erro ao criar a tabela 'usuarios': {e}")

if __name__ == "__main__":
    
    print("Iniciando aplicação...")
    
    conexao_db = conectar_bd()
    
    if conexao_db:
        
        criar_tabela_usuarios(conexao_db)
        
        consultar_dados(conexao_db)

        if conexao_db.is_connected():
            conexao_db.close()
            print("\nConexão ao MySQL foi fechada.")
    else:
        print("Não foi possível conectar ao banco. Verifique as configurações.")