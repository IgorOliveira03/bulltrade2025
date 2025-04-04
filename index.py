from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session 
import random 
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessário para usar sessões

# Lista de usuários e senhas válidas
USUARIOS_VALIDOS = [
    {"usuario": "dubaibull", "senha": "bulldubai", "nome": "Trader"}
]

@app.route('/usuarios')
def usuarios():
    # Renderiza a lista de usuários em um template HTML
    return render_template('usuarios.html', usuarios=USUARIOS_VALIDOS)

# Listas predefinidas para geração de sinais aleatórios
assets = ["EUR/USD", "USD/BRL", "USOUSD", "BTC/USD", "EUR/GBP", "AUD/CAD", "USD/CHF", "GBP/USD", "PEN/USD", "NZD/USD", "GBP/JPY", "ETH/USD ", "CARDANO", "TRUMP Coin ", "MELANIA Coin", "AUS 200", "ONDO", "SOL/USD", "DOGECOIN" ]
directions = ["COMPRA", "VENDA"]
durations = ["M1"]  # Em minutos

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form['usuario'].lower()
        senha = request.form['senha']
        nome = request.form['nome']

        # Verifica se o usuário já existe
        for credenciais in USUARIOS_VALIDOS:
            if credenciais['usuario'] == usuario:
                flash('Usuário já cadastrado!')
                return redirect(url_for('cadastro'))

        # Adiciona o novo usuário à lista de usuários válidos
        novo_usuario = {"usuario": usuario, "senha": senha, "nome": nome}
        USUARIOS_VALIDOS.append(novo_usuario)
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

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
 #Redireciona para a página inicial
            return redirect(url_for('home'))

    flash('Usuário ou senha incorretos!')
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'usuario' not in session:
        flash('Você precisa estar logado para acessar.')
        return redirect(url_for('login'))
    
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    return render_template('home.html', nome=nome_usuario)


@app.route('/academy')
def academy():
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    return render_template('academy.html', nome=nome_usuario)

@app.route('/news')
def news():
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    return render_template('news.html', nome=nome_usuario)

@app.route('/historico')
def historico():
    nome_usuario = session.get('nome')  # Obtém o usuário da sessão
    return render_template('historico.html', nome=nome_usuario)


@app.route('/logout')
def logout():
    session.clear()  # Limpa toda a sessão do usuário
    flash('Sessão encerrada com sucesso.')
    return redirect(url_for('login'))


@app.route('/generate-random-signal', methods=['GET'])
def generate_random_signal():
    if 'usuario' not in session:
        return jsonify({"error": "Usuário não está logado."}), 403

    asset = random.choice(assets)
    direction = random.choice(directions)
    duration = random.choice(durations)
 # Adiciona o horário no formato HH:MM:SS
    signal = {"asset": asset, "direction": direction, "duration": duration, "time_sent": (datetime.now() + timedelta(hours=-3) + timedelta(minutes=1)).strftime('%H:%M:%S')}

    # Adiciona o sinal gerado à lista do usuário logado
    session['signals'].append(signal)
    session.modified = True  # Necessário para salvar alterações na sessão
    return jsonify(signal)




@app.route('/get-signals', methods=['GET'])
def get_signals():
    if 'usuario' not in session:
        return jsonify({"error": "Usuário não está logado."}), 403

    # Retorna apenas os sinais do usuário logado
    return jsonify(session.get('signals', []))


if __name__ == '__main__':
    app.run(debug=True)


