from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_config import conectar_bd
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'chave_sessao'

@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('tela_inicial'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['usuario']
        senha = request.form['senha']

        try:
            conexao = conectar_bd()
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE nome = %s AND senha = %s", (nome, senha))
            usuario = cursor.fetchone()

            if usuario:
                session['usuario'] = usuario['nome']
                session['admin'] = usuario['admin']
                flash('Login realizado com sucesso!')
                return redirect(url_for('tela_inicial'))
            else:
                flash('Usuário ou senha incorretos.')

        except Error as e:
            flash(f"Erro ao conectar ao banco: {e}")

        finally:
            cursor.close()
            conexao.close()

    return render_template('login.html')

@app.route('/tela_inicial')  
def tela_inicial():   
    return render_template('tela_inicial.html')

@app.route('/cadastro')  
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
