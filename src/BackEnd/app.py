from flask import Flask
from flask_cors import CORS
from Conta.conta import Conta
from Transacao.transacao import Transacao
from flask import request, jsonify


from authenticationFolder.authentication import login_bp

from ArmazenaSolicitacoesCartao.ArmazenaSolicitacoesCartao import cartao_bp, init_db

app = Flask(__name__)
CORS(app)

# Registra os blueprints
app.register_blueprint(login_bp)
app.register_blueprint(cartao_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# Consulta o saldo de uma conta pelo CPF
@app.route('/api/consultar-saldo/<cpf>', methods=['GET'])
def consultar_saldo(cpf):
    conta = Conta(cpf)
    saldo = conta.consultar_saldo()
    if saldo is not None:
        return jsonify({'cpf': cpf, 'saldo': saldo}), 200
    else:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
# Realiza transferência entre contas
@app.route('/api/transferir', methods=['POST'])
def transferir():
    data = request.json
    cpf_origem = data.get('cpf_origem')
    cpf_destino = data.get('cpf_destino')
    valor = float(data.get('valor'))
    transacao = Transacao(cpf_origem, cpf_destino, valor)
    sucesso, mensagem = transacao.realizar()
    if sucesso:
        return jsonify({'mensagem': mensagem}), 200
    else:
        return jsonify({'erro': mensagem}), 400

# Realiza depósito em uma conta
@app.route('/api/depositar', methods=['POST'])
def depositar():
    data = request.json
    cpf = data.get('cpf')
    valor = float(data.get('valor'))
    conta = Conta(cpf)
    conta.depositar(valor)
    return jsonify({'mensagem': 'Depósito realizado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)