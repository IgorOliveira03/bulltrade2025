from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para usar sessões

# Lista de usuários e senhas válidas
USUARIOS_VALIDOS = [
    {"usuario": "bullex@gmail.com", "senha": "123", "nome": "Bullex"},
    {"usuario": "gui", "senha": "123", "nome": "Gui"},
    {"usuario": "andrey", "senha": "123", "nome": "Andrey"},
    {"usuario": "joao@gmail.com", "senha": "456", "nome": "João"}
]

# Listas predefinidas para geração de sinais aleatórios
assets = ["EUR/JPY", "USD/BRL", "EUR/USD", "BTC/USD", "EUR/GBP", "AUD/CAD", "USD/CHF", "GBP/USD", "PEN/USD", "NZD/USD", "GBP/JPY", "TRUMP Coin"]
directions = ["COMPRA", "VENDA"]
durations = ["M1", "M3", "M5"]  # Em minutos


@app.route('/')
def login():
    if 'usuario' in session:
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario'].lower()
    senha = request.form['senha']
    
    for credenciais in USUARIOS_VALIDOS:
        if credenciais['usuario'] == usuario and credenciais['senha'] == senha:
            session['usuario'] = usuario
            session['nome'] = credenciais['nome']
            session['signals'] = []  # Inicializa a lista de sinais para o usuário logado
            session['progresso'] = 0  # Inicializa o progresso do usuário
            session['botoes_concluidos'] = []  # Inicializa a lista de botões concluídos
            return redirect(url_for('home'))

    flash('Usuário ou senha incorretos!')
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar.')
        return redirect(url_for('login'))
    
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    progresso = session.get('progresso', 0)
    botoes_concluidos = session.get('botoes_concluidos', [])
    return render_template('home.html', nome=nome_usuario, progresso=progresso, botoes_concluidos=botoes_concluidos)


@app.route('/academy')
def academy():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar.')
        return redirect(url_for('login'))
    
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    progresso = session.get('progresso', 0)
    botoes_concluidos = session.get('botoes_concluidos', [])
    return render_template('academy.html', nome=nome_usuario, progresso=progresso, botoes_concluidos=botoes_concluidos)


@app.route('/logout')
def logout():
    session.clear()  # Limpa toda a sessão do usuário
    flash('Sessão encerrada com sucesso.')
    return redirect(url_for('login'))


@app.route('/marcar-concluido', methods=['POST'])
def marcar_concluido():
    if 'usuario' not in session:
        return jsonify({"error": "Usuário não está logado."}), 403

    data = request.json
    botao_id = data.get('botao_id')
    progresso = data.get('progresso')

    if botao_id not in session.get('botoes_concluidos', []):
        session['botoes_concluidos'].append(botao_id)
        session['progresso'] = progresso
        session.modified = True
        return jsonify({"message": "Botão marcado como concluído.", "progresso": progresso})
    else:
        return jsonify({"message": "Botão já concluído."})


if __name__ == '__main__':
    app.run(debug=True)