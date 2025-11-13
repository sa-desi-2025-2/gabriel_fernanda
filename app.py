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

@app.route('/logout')
def logout():
    session.clear() 
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login')) 

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('usuario', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        confirmar = request.form.get('confirmar', '')

        if not nome or not email or not senha:
            flash('Preencha todos os campos.')
            return redirect(url_for('cadastro'))

        if senha != confirmar:
            flash('As senhas não coincidem.')
            return redirect(url_for('cadastro'))

        try:
            conexao = conectar_bd()
            cursor = conexao.cursor()
            cursor.execute("SELECT id_usuario FROM Usuario WHERE nome = %s OR email = %s", (nome, email))
            if cursor.fetchone():
                flash('Nome de usuário ou email já cadastrado.')
                return redirect(url_for('cadastro'))

            cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            conexao.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except Error as e:
            flash(f"Erro ao cadastrar usuário: {e}")
        finally:
            try:
                cursor.close()
                conexao.close()
            except:
                pass

    return render_template('cadastro.html')

@app.route('/solicitacao', methods=['GET', 'POST'])
def solicitacao():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        tipo = request.form.get('tipo', '').strip()
        defeito = request.form.get('defeito', '').strip()
        lugar = request.form.get('lugar', '').strip()
        descricao = request.form.get('descricao', '').strip()

        campos_vazios = []
        if not usuario:
            campos_vazios.append('nome')
        if not defeito:
            campos_vazios.append('defeito')
        if not lugar:
            campos_vazios.append('local')

        if campos_vazios:

            if len(campos_vazios) == 1:
                msg = f"O campo {campos_vazios[0]} é obrigatório!"
            else:
                lista = ', '.join(campos_vazios[:-1]) + ' e ' + campos_vazios[-1]
                msg = f"Os campos {lista} são obrigatórios!"
            flash(msg, 'error')
            return redirect(url_for('solicitacao'))
        
        try:
            conexao = conectar_bd()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO Solicitacao (usuario, tipo, defeito, lugar, descricao) VALUES (%s, %s, %s, %s, %s)",(usuario, tipo, defeito, lugar, descricao))
            conexao.commit()
            flash('Solicitação enviada com sucesso!')
            return redirect(url_for('solicitacao'))
        except Error as e:
            flash(f'Erro ao salvar solicitação: {e}')
        finally:
            try:
                cursor.close()
                conexao.close()
            except:
                pass

    return render_template('solicitacao.html')

@app.route('/solicitacao_admin')
def solicitacao_admin():
    try:
        conexao = conectar_bd()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Solicitacao")
        solicitacoes = cursor.fetchall()
        return render_template('solicitacao_admin.html', solicitacoes=solicitacoes)
    except Error as e:
        return f"Erro ao carregar solicitações: {e}"
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass

@app.route('/api/pontos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pontos():
    if 'usuario' not in session:
        return {'error': 'Não autorizado'}, 401

    try:
        conexao = conectar_bd()
        cursor = conexao.cursor(dictionary=True)

        if request.method == 'GET':
            cursor.execute("SELECT * FROM Ponto")
            pontos = cursor.fetchall()
            return {'pontos': pontos}

        elif request.method == 'POST':
            if session.get('admin') != 1:
                return {'error': 'Não autorizado'}, 403

            dados = request.get_json()

            campos_requeridos = ['tipo', 'defeito', 'local', 'latitude', 'longitude']
            for campo in campos_requeridos:
                if campo not in dados:
                    return {'error': f'Campo obrigatório ausente: {campo}'}, 400

            try:
                cursor.execute("SELECT id_mapa FROM Mapa WHERE id_mapa = 1")
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Mapa (id_mapa) VALUES (1)")
                    conexao.commit()

                cursor.execute("""
                    INSERT INTO Ponto (tipo, defeito, local, latitude, longitude, descricao, id_mapa) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        dados.get('tipo'),
                        dados.get('defeito'),
                        dados.get('local'),
                        dados.get('latitude'),
                        dados.get('longitude'),
                        dados.get('descricao'),
                        1  
                    ))
                conexao.commit()
                return {'id': cursor.lastrowid}, 201
            except Error as e:
                conexao.rollback()
                print(f"Erro MySQL ao inserir ponto: {str(e)}")
                return {'error': f'Erro ao inserir ponto: {str(e)}'}, 500

        elif request.method == 'PUT':
            if session.get('admin') != 1:
                return {'error': 'Não autorizado'}, 403

            dados = request.get_json()

            if 'id' not in dados:
                return {'error': 'Campo id ausente'}, 400

            campos = []
            valores = []
            if 'tipo' in dados:
                campos.append('tipo = %s')
                valores.append(dados['tipo'])
            if 'defeito' in dados:
                campos.append('defeito = %s')
                valores.append(dados['defeito'])
            if 'local' in dados:
                campos.append('local = %s')
                valores.append(dados['local'])
            if 'descricao' in dados:
                campos.append('descricao = %s')
                valores.append(dados['descricao'])

            if not campos:
                return {'error': 'Nenhum campo para atualizar'}, 400

            valores.append(dados['id'])
            sql = f"UPDATE Ponto SET {', '.join(campos)} WHERE id_ponto = %s"
            cursor.execute(sql, tuple(valores))
            conexao.commit()
            return {'success': True}

        elif request.method == 'DELETE':
            if session.get('admin') != 1:
                return {'error': 'Não autorizado'}, 403

            dados = request.get_json()
            cursor.execute("DELETE FROM Ponto WHERE id_ponto = %s", (dados['id'],))
            conexao.commit()
            return {'success': True}

    except Error as e:
        print(f"Erro MySQL: {str(e)}")
        return {'error': str(e)}, 500
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        return {'error': str(e)}, 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()

if __name__ == '__main__':
    app.run(debug=True)
