from db_config import conectar_bd
from mysql.connector import Error

def inicializar_banco(conexao):
    """
    Executa o script SQL completo para criar o banco de dados,
    as tabelas e as relações (Foreign Keys).
    """
    
    script_sql_completo = """
    CREATE DATABASE IF NOT EXISTS MapaInterativo;

    USE MapaInterativo;

    CREATE TABLE IF NOT EXISTS Usuario ( 
      id_usuario INT PRIMARY KEY AUTO_INCREMENT,   
      nome VARCHAR(40) NOT NULL,   
      email VARCHAR(40) NOT NULL,   
      senha VARCHAR(40) NOT NULL,   
      admin INT NOT NULL DEFAULT '0'   
    ); 

    CREATE TABLE IF NOT EXISTS Mapa ( 
      id_mapa INT PRIMARY KEY
    ); 

    CREATE TABLE IF NOT EXISTS Ponto ( 
      id_ponto INT PRIMARY KEY AUTO_INCREMENT,   
      nome VARCHAR(40) NOT NULL,   
      tipo VARCHAR(40) NOT NULL,   
      latitude FLOAT NOT NULL,   
      longitude FLOAT NOT NULL,   
      descricao VARCHAR(40),   
      id_mapa INT NOT NULL,
      FOREIGN KEY(id_mapa) REFERENCES Mapa (id_mapa)
    ); 

    CREATE TABLE IF NOT EXISTS Solicitação ( 
      id_solicitacao INT PRIMARY KEY AUTO_INCREMENT,   
      nome VARCHAR(40) NOT NULL,   
      tipo VARCHAR(40) NOT NULL,   
      descricao VARCHAR(40),   
      local VARCHAR(40) NOT NULL,   
      id_usuario INT,
      FOREIGN KEY(id_usuario) REFERENCES Usuario (id_usuario)
    );
    """
    
    print("Iniciando inicialização do banco de dados...")
    
    with conexao.cursor() as cursor:
        try:
            comandos_sql = script_sql_completo.split(';')
            for comando in comandos_sql:
                if comando.strip():
                    cursor.execute(comando)
            conexao.commit()
            print("Banco 'MapaInterativo' e tabelas criados/verificados com sucesso!")
        except Error as e:
            print(f"Erro ao executar script de inicialização: {e}")
            conexao.rollback()

if __name__ == "__main__":

    print("Iniciando aplicação...")
    
    conexao_db = conectar_bd()
    
    if conexao_db:
        
        inicializar_banco(conexao_db)
        
        if conexao_db.is_connected():
            conexao_db.close()
            print("\nConexão ao MySQL foi fechada.")
    else:
        print("Não foi possível conectar ao servidor MySQL. Verifique as configurações.")