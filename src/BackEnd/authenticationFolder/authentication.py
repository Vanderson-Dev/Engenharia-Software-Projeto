
import os
import mysql.connector
from flask import Blueprint, request, jsonify

login_bp = Blueprint('login', __name__)

# Configuração do banco de dados MySQL
db_config = {
    'host': os.getenv('DB_HOST', 'switchback.proxy.rlwy.net'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'RxrFzneigIEmxTWcZWTlaaPGeaTbeehl'),
    'database': os.getenv('DB_NAME', 'railway'),
    'port': int(os.getenv('DB_PORT', 14474))
}

# Rota de login
@login_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('password')

    try:
        # Conectando ao banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Consulta SQL para buscar o usuário
        query = "SELECT * FROM clientes WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return jsonify({"success": True, "usuario": usuario})
        else:
            return jsonify({"success": False, "mensagem": "Usuário ou senha inválidos."})

    except mysql.connector.Error as err:
        return jsonify({"success": False, "erro": str(err)}), 500