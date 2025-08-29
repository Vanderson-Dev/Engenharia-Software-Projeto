from flask import Blueprint, request, jsonify
from src.BackEnd.Classes.investimentos import realizar_investimento
import pymysql
from decimal import Decimal, ROUND_HALF_UP

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

def to_amount(v):
    try:
        return Decimal(str(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception:
        return None

def get_usuario_conta(cursor, email, senha):
    cursor.execute("""
        SELECT
            clientes.id   AS cliente_id,
            clientes.cpf  AS cpf,
            clientes.nome AS nome,
            Conta.id      AS conta_id,
            Conta.saldo   AS saldo
        FROM clientes
        JOIN Conta ON Conta.usuario_id = clientes.id
        WHERE clientes.email = %s AND clientes.senha = %s
    """, (email, senha))
    return cursor.fetchone()

# ---------------- DEPÓSITO ----------------
deposito_bp = Blueprint('deposito', __name__)

@deposito_bp.route('/deposito', methods=['POST'])
def realizar_deposito():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    valor = to_amount(data.get('valor'))

    if not email or not senha or valor is None or valor <= 0:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        usuario = get_usuario_conta(cursor, email, senha)
        if not usuario:
            return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

        conta_id = usuario['conta_id']
        cliente_id = usuario['cliente_id']

        cursor.execute("UPDATE Conta SET saldo = saldo + %s WHERE usuario_id = %s", (valor, cliente_id))
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, description)
            VALUES (%s, 'deposito', %s, %s)
        """, (conta_id, valor, 'Depósito realizado'))

        conn.commit()
        return jsonify({"mensagem": "Depósito realizado com sucesso!"}), 200
    except:
        conn.rollback()
        return jsonify({"mensagem": "Erro interno"}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- SAQUE ----------------
saque_bp = Blueprint('saque', __name__)

@saque_bp.route('/saque', methods=['POST'])
def realizar_saque():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    valor = to_amount(data.get('valor'))

    if not email or not senha or valor is None or valor <= 0:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        usuario = get_usuario_conta(cursor, email, senha)
        if not usuario:
            return jsonify({"mensagem": "E-mail ou senha inválidos"}), 401

        conta_id = usuario['conta_id']
        cliente_id = usuario['cliente_id']

        cursor.execute("SELECT saldo FROM Conta WHERE usuario_id = %s FOR UPDATE", (cliente_id,))
        row = cursor.fetchone()
        if not row or Decimal(str(row['saldo'])) < valor:
            return jsonify({"mensagem": "Saldo insuficiente para saque."}), 403

        cursor.execute("UPDATE Conta SET saldo = saldo - %s WHERE usuario_id = %s", (valor, cliente_id))
        cursor.execute("""
            INSERT INTO transactions (account_id, type, amount, description)
            VALUES (%s, 'saque', %s, %s)
        """, (conta_id, valor, 'Saque realizado'))

        conn.commit()
        return jsonify({"mensagem": "Saque realizado com sucesso!"}), 200
    except:
        conn.rollback()
        return jsonify({"mensagem": "Erro interno"}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- SALDO ----------------
saldo_bp = Blueprint('saldo', __name__)

@saldo_bp.route('/saldo', methods=['POST'])
def consultar_saldo():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        usuario = get_usuario_conta(cursor, email, senha)
        if not usuario:
            return jsonify({"mensagem": "Conta não encontrada"}), 404
        return jsonify({"saldo": float(usuario['saldo'])}), 200
    finally:
        cursor.close()
        conn.close()

# ---------------- CONSULTA NOME ----------------
@saldo_bp.route('/nome', methods=['POST'])
def consultar_nome():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nome FROM clientes WHERE email = %s AND senha = %s", (email, senha))
        resultado = cursor.fetchone()
        if resultado:
            return jsonify({"nome": resultado['nome']}), 200
        else:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404
    finally:
        cursor.close()
        conn.close()

# ---------------- TRANSFERÊNCIA ----------------
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

# ---------------- INVESTIMENTO ----------------
investir_bp = Blueprint('investir', __name__)

@investir_bp.route('/investir', methods=['POST'])
def investir():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    valor = to_amount(data.get('valor'))
    tipo = data.get('tipo')

    if not email or not senha or valor is None or valor <= 0 or not tipo:
        return jsonify({'erro': 'Dados inválidos.'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT clientes.id AS cliente_id, Conta.id AS conta_id
            FROM clientes
            JOIN Conta ON Conta.usuario_id = clientes.id
            WHERE clientes.email = %s AND clientes.senha = %s
        """, (email, senha))
        usuario = cursor.fetchone()
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado.'}), 400

        usuario_id = usuario['cliente_id']
        conta_id = usuario['conta_id']

        resultado = realizar_investimento(conn, usuario_id, float(valor), tipo)

        # Exemplo: registrar no extrato (se desejar)
        # cursor.execute("""
        #     INSERT INTO transactions (account_id, type, amount, description)
        #     VALUES (%s, 'investimento', %s, %s)
        # """, (conta_id, valor, f'Aplicação em {tipo}'))

        conn.commit()
        return jsonify(resultado)
    except:
        conn.rollback()
        return jsonify({'erro': 'Erro interno.'}), 500
    finally:
        cursor.close()
        conn.close()

# ---------------- EXTRATO ----------------
extrato_bp = Blueprint('extrato', __name__)

@extrato_bp.route('/extrato', methods=['POST'])
def extrato():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Dados incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT Conta.id
            FROM clientes
            JOIN Conta ON Conta.usuario_id = clientes.id
            WHERE clientes.email = %s AND clientes.senha = %s
        """, (email, senha))
        conta = cursor.fetchone()

        if not conta:
            return jsonify({"mensagem": "Usuário não encontrado"}), 404

        cursor.execute("""
            SELECT created_at, description, type, amount
            FROM transactions
            WHERE account_id = %s
            ORDER BY created_at DESC
        """, (conta['id'],))
        transacoes = cursor.fetchall()

        return jsonify({"transacoes": transacoes})
    finally:
        cursor.close()
        conn.close()
