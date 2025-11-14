from db_config import conectar_bd
from mysql.connector import Error


def inicializar_banco(conexao):
    script_sql = """
CREATE DATABASE IF NOT EXISTS MapaInterativo;
USE MapaInterativo;

CREATE TABLE IF NOT EXISTS Usuario (
  id_usuario INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL UNIQUE,
  senha VARCHAR(100) NOT NULL,
  admin TINYINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Mapa (
  id_mapa INT PRIMARY KEY AUTO_INCREMENT
);

INSERT IGNORE INTO Mapa (id_mapa) VALUES (1);

CREATE TABLE IF NOT EXISTS Ponto (
  id_ponto INT PRIMARY KEY AUTO_INCREMENT,
  tipo VARCHAR(40) NOT NULL,
  defeito VARCHAR(120) NOT NULL,
  local VARCHAR(120) NOT NULL,
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  descricao TEXT,
  id_mapa INT NOT NULL,
  FOREIGN KEY (id_mapa) REFERENCES Mapa(id_mapa)
);

CREATE TABLE IF NOT EXISTS Solicitacao (
  id_solicitacao INT PRIMARY KEY AUTO_INCREMENT,
  usuario VARCHAR(100) NOT NULL,
  tipo VARCHAR(40) NOT NULL,
  defeito VARCHAR(120) NOT NULL,
  lugar VARCHAR(120) NOT NULL,
  descricao TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'Em análise',
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO Usuario (nome, email, senha, admin)
VALUES ('admin', 'admin@email.com', '1234', 1);
"""

    try:
        print("Iniciando inicialização do banco de dados...")
        cursor = conexao.cursor()
        for comando in script_sql.split(';'):
            comando = comando.strip()
            if comando:
                cursor.execute(comando)
        conexao.commit()
        print("Banco criado/verificado com sucesso!")
    except Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        conexao.rollback()


if __name__ == '__main__':
    print("Iniciando aplicação...")
    conexao_db = conectar_bd()
    if conexao_db:
        inicializar_banco(conexao_db)
        if conexao_db.is_connected():
            conexao_db.close()
            print("Conexão ao MySQL foi fechada.")
    else:
        print("Não foi possível conectar ao servidor MySQL. Verifique as configurações.")