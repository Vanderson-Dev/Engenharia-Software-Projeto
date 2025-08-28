from flask import Blueprint, request, jsonify
from src.BackEnd.Classes.Conta import Conta  # importa a classe Conta
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
