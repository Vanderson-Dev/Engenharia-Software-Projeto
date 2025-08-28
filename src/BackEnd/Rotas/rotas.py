from flask import Blueprint, request, jsonify
from src.BackEnd.Classes.Conta import Conta
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

# Função auxiliar para buscar cliente
def buscar_cliente(cursor, email, senha):
    cursor.execute("""
        SELECT clientes.id, clientes.cpf, clientes.nome, Conta.saldo 
        FROM clientes 
        JOIN Conta ON Conta.usuario_id = clientes.id 
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
    return cursor.fetchone()

# Blueprint: Depósito
deposito_bp = Blueprint('deposito', __name__)

@deposito_bp.route('/deposito', methods=['POST'])
def realizar_deposito():
    try:
        data = request.get_json()
        email = data.get('email')
        valor = float(data.get('valor'))
        senha = data.get('senha')

        if not email or not valor or not senha or valor <= 0:
            return jsonify({"mensagem": "Dados inválidos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cliente = buscar_cliente(cursor, email, senha)
        if not cliente:
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

        conta = Conta(cpf=cliente['cpf'], saldo=cliente['saldo'], id=cliente['id'])
        conta.depositar(valor)

        cursor.execute("UPDATE Conta SET saldo = %s WHERE usuario_id = %s", (conta.saldo, conta.id))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Depósito realizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro interno"}), 500

# Blueprint: Saque
saque_bp = Blueprint('saque', __name__)

@saque_bp.route('/saque', methods=['POST'])
def realizar_saque():
    try:
        data = request.get_json()
        email = data.get('email')
        valor = float(data.get('valor'))
        senha = data.get('senha')

        if not email or not valor or not senha or valor <= 0:
            return jsonify({"mensagem": "Dados inválidos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cliente = buscar_cliente(cursor, email, senha)
        if not cliente:
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

        conta = Conta(cpf=cliente['cpf'], saldo=cliente['saldo'], id=cliente['id'])

        if not conta.sacar(valor):
            cursor.close()
            conn.close()
            return jsonify({"mensagem": "Saldo insuficiente para saque."}), 403

        cursor.execute("UPDATE Conta SET saldo = %s WHERE usuario_id = %s", (conta.saldo, conta.id))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Saque realizado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"mensagem": "Erro interno"}), 500

# Blueprint: Saldo
saldo_bp = Blueprint('saldo', __name__)

@saldo_bp.route('/saldo', methods=['POST'])
def consultar_saldo():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            return jsonify({"mensagem": "Dados incompletos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cliente = buscar_cliente(cursor, email, senha)
        cursor.close()
        conn.close()

        if cliente:
            return jsonify({"saldo": cliente['saldo']}), 200
        else:
            return jsonify({"mensagem": "Conta não encontrada"}), 404

    except Exception as e:
        return jsonify({"mensagem": "Erro interno"}), 500

@saldo_bp.route('/nome', methods=['POST'])
def consultar_nome():
    try:
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

    except Exception as e:
        return jsonify({"mensagem": "Erro interno"}), 500

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

        remetente = buscar_cliente(cursor, email, senha)
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
