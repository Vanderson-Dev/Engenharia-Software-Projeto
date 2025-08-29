from flask import Blueprint, request, jsonify
from src.BackEnd.Classes.investimentos import realizar_investimento
import pymysql
import requests
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
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    cpf_destino = data.get('cpf_destino')
    valor = to_amount(data.get('valor'))

    if not email or not senha or not cpf_destino or valor is None or valor <= 0:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            remetente = get_usuario_conta(cursor, email, senha)
            if not remetente: return jsonify({"mensagem": "Remetente inválido"}), 401
            if Decimal(str(remetente['saldo'])) < valor: return jsonify({"mensagem": "Saldo insuficiente"}), 403

            cursor.execute("SELECT c.id, c.nome, co.id AS conta_id FROM clientes c JOIN Conta co ON c.id = co.usuario_id WHERE c.cpf = %s", (cpf_destino,))
            destinatario = cursor.fetchone()
            if not destinatario: return jsonify({"mensagem": "Destinatário não encontrado"}), 404
            if destinatario['id'] == remetente['cliente_id']: return jsonify({"mensagem": "Não é possível transferir para si mesmo."}), 400

            # Atualiza saldos
            cursor.execute("UPDATE Conta SET saldo = saldo - %s WHERE id = %s", (valor, remetente['conta_id']))
            cursor.execute("UPDATE Conta SET saldo = saldo + %s WHERE id = %s", (valor, destinatario['conta_id']))

            # Registra transações para o extrato de ambos
            desc_remetente = f"Transferência para {destinatario['nome']}"
            cursor.execute(
                "INSERT INTO transactions (account_id, type, amount, target_account_id, description) VALUES (%s, 'transferencia', %s, %s, %s)",
                (remetente['conta_id'], valor, destinatario['conta_id'], desc_remetente)
            )
            desc_destinatario = f"Transferência recebida de {remetente['nome']}"
            cursor.execute(
                "INSERT INTO transactions (account_id, type, amount, target_account_id, description) VALUES (%s, 'transferencia', %s, %s, %s)",
                (destinatario['conta_id'], valor, remetente['conta_id'], desc_destinatario)
            )
            conn.commit()
        return jsonify({"mensagem": "Transferência realizada com sucesso!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"mensagem": f"Erro interno: {e}"}), 500
    finally:
        if conn:
            conn.close()

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

# ---------------- CONVERSÃO DE MOEDAS ---------------- 
moedas_bp = Blueprint('moedas', __name__)

@moedas_bp.route('/conversao-moedas', methods=['POST'])
def conversao_moedas():
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
            return jsonify({"mensagem": "Credenciais inválidas"}), 401
            
        saldo_brl = usuario['saldo']
        
        # Usando API ExchangeRate para obter cotações em tempo real
        try:
            response = requests.get('https://open.er-api.com/v6/latest/BRL')
            data = response.json()
            
            if data['result'] == 'success':
                rates = data['rates']
                usd_value = saldo_brl * rates['USD']
                eur_value = saldo_brl * rates['EUR']
                gbp_value = saldo_brl * rates['GBP']
                
                return jsonify({
                    "saldo_original": float(saldo_brl),
                    "conversoes": {
                        "USD": round(usd_value, 2),
                        "EUR": round(eur_value, 2),
                        "GBP": round(gbp_value, 2)
                    },
                    "taxas": {
                        "USD": round(rates['USD'], 4),
                        "EUR": round(rates['EUR'], 4),
                        "GBP": round(rates['GBP'], 4)
                    }
                }), 200
            else:
                return jsonify({"mensagem": "Erro ao obter cotações"}), 500
                
        except requests.exceptions.RequestException:
            # Fallback para taxas fixas em caso de erro na API
            usd_value = saldo_brl * 0.19  # Taxa aproximada USD
            eur_value = saldo_brl * 0.17  # Taxa aproximada EUR
            gbp_value = saldo_brl * 0.15  # Taxa aproximada GBP
            
            return jsonify({
                "saldo_original": float(saldo_brl),
                "conversoes": {
                    "USD": round(usd_value, 2),
                    "EUR": round(eur_value, 2),
                    "GBP": round(gbp_value, 2)
                },
                "taxas": {
                    "USD": 0.19,
                    "EUR": 0.17,
                    "GBP": 0.15
                },
                "aviso": "Usando taxas aproximadas"
            }), 200
            
    except Exception as e:
        return jsonify({"mensagem": f"Erro interno: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()