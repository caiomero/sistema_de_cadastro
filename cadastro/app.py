from flask import Flask, render_template, request, redirect
import sqlite3
import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app = Flask(__name__)

# ---------------- Banco ----------------

def inicializar_banco():
    conexao = sqlite3.connect('clientes.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            data_cadastro TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conexao.commit()
    conexao.close()

def conectar():
    return sqlite3.connect('clientes.db')


# ---------------- Rotas ----------------

@app.route('/')
def index():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conexao.close()
    return render_template('index.html', clientes=clientes)


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cpf = request.form['cpf']

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, email, telefone, cpf)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, cpf))
        conexao.commit()
        conexao.close()
    except:
        pass

    return redirect('/')


@app.route('/excluir/<cpf>')
def excluir(cpf):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
    conexao.commit()
    conexao.close()
    return redirect('/')


if __name__ == '__main__':
    inicializar_banco()

    app.run(debug=True)
