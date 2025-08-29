from flask import Blueprint, request, jsonify
from src.BackEnd.Classes.conta import Conta  # importa a classe Conta
from src.BackEnd.Classes.investimentos import realizar_investimento
import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root", 
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )

deposito_bp = Blueprint('deposito', __name__)

@deposito_bp.route('/deposito', methods=['POST'])
def realizar_deposito():
    data = request.get_json()
    email = data.get('email')
    valor = data.get('valor')
    senha = data.get('senha')

    if not email or not valor or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca o cliente pelo e-mail e senha
    cursor.execute("""
    SELECT clientes.id, clientes.cpf, Conta.saldo 
    FROM clientes 
    JOIN Conta ON Conta.usuario_id = clientes.id 
    WHERE clientes.email = %s AND clientes.senha = %s
""", (email, senha))
    cliente = cursor.fetchone()


    if not cliente:
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

    conta = Conta(cpf=cliente['cpf'], saldo=cliente['saldo'], id=cliente['id'])
    conta.depositar(valor)

    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Depósito realizado com sucesso!"}), 200

#saque
saque_bp = Blueprint('saque', __name__)
@saque_bp.route('/saque', methods=['POST'])
def realizar_saque():
    data = request.get_json()
    email = data.get('email')
    valor = data.get('valor')
    senha = data.get('senha')

    if not email or not valor or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Busca o cliente e saldo atual
    cursor.execute("""
        SELECT clientes.id, clientes.cpf, Conta.saldo 
        FROM clientes 
        JOIN Conta ON Conta.usuario_id = clientes.id 
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
    cliente = cursor.fetchone()

    if not cliente:
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

    conta = Conta(cpf=cliente['cpf'], saldo=cliente['saldo'], id=cliente['id'])

    if not conta.sacar(valor):
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Saldo insuficiente para saque."}), 403

    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Saque realizado com sucesso!"}), 200

#saldo
@deposito_bp.route('/saldo', methods=['POST'])
def consultar_saldo():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Conta.saldo 
        FROM clientes 
        JOIN Conta ON Conta.usuario_id = clientes.id 
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return jsonify({"saldo": resultado['saldo']}), 200
    else:
        return jsonify({"mensagem": "Conta não encontrada"}), 404
   
    
saldo_bp = Blueprint('saldo', __name__)
@saldo_bp.route('/nome', methods=['POST'])
def consultar_nome():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM clientes WHERE email = %s AND senha = %s", (email, senha))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        return jsonify({"nome": resultado['nome']}), 200
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

# Blueprint: Transferência
transferencia_bp = Blueprint('transferencia', __name__)

@transferencia_bp.route('/transferencia', methods=['POST'])
def realizar_transferencia():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        cpf_destino = data.get('cpf_destino')
        valor = float(data.get('valor'))

        if not email or not senha or not cpf_destino or valor <= 0:
            return jsonify({"mensagem": "Dados inválidos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT clientes.id, clientes.cpf, clientes.nome, Conta.saldo 
        FROM clientes 
        JOIN Conta ON Conta.usuario_id = clientes.id 
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
        remetente = cursor.fetchone()
        if not remetente:
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Remetente inválido"}), 401

        if remetente['saldo'] < valor:
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Saldo insuficiente"}), 403

        cursor.execute("SELECT clientes.id FROM clientes WHERE cpf = %s", (cpf_destino,))
        destinatario = cursor.fetchone()

        if not destinatario:
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Destinatário não encontrado"}), 404

        cursor.execute("UPDATE Conta SET saldo = saldo - %s WHERE usuario_id = %s", (valor, remetente['id']))
        cursor.execute("UPDATE Conta SET saldo = saldo + %s WHERE usuario_id = %s", (valor, destinatario['id']))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Transferência realizada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro interno"}), 500
    
investir_bp = Blueprint('investir', __name__)

@investir_bp.route('/investir', methods=['POST'])
def investir():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    valor = float(data.get('valor'))
    tipo = data.get('tipo')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT clientes.id FROM clientes
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
    usuario = cursor.fetchone()
    if not usuario:
        cursor.close()
        conn.close()
        return jsonify({'erro': 'Usuário não encontrado.'}), 400

    usuario_id = usuario['id']
    resultado = realizar_investimento(conn, usuario_id, valor, tipo)
    cursor.close()
    conn.close()
    return jsonify(resultado)