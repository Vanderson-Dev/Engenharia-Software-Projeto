
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do MySQL
db_config = {
    'host': os.getenv('DB_HOST', 'switchback.proxy.rlwy.net'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'RxrFzneigIEmxTWcZWTlaaPGeaTbeehl'),
    'database': os.getenv('DB_NAME', 'railway'),
    'port': int(os.getenv('DB_PORT', 14474))  
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        raise

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                endereco TEXT NOT NULL,
                cpf VARCHAR(14) NOT NULL UNIQUE,
                data_nascimento DATE NOT NULL,
                sexo ENUM('masculino', 'feminino', 'outro') NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL,
                INDEX idx_cpf_cliente (cpf)
            )
        ''')
        
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao inicializar banco de dados: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/cadastrar-cliente', methods=['POST'])
def cadastrar_cliente():
    data = request.json

    required_fields = ['nome', 'endereco', 'cpf', 'data_nascimento', 'sexo', 'email', 'senha']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'O campo {field} é obrigatório'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO clientes (
                nome, endereco, cpf, data_nascimento, sexo, email, senha, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['nome'],
            data['endereco'],
            data['cpf'],
            data['data_nascimento'],
            data['sexo'],
            data['email'],
            data['senha'],  
            datetime.now()
        ))

        conn.commit()
        return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 201

    except mysql.connector.IntegrityError as err:
        return jsonify({'error': 'CPF ou e-mail já cadastrado'}), 409
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
        return jsonify({'error': 'Erro ao cadastrar cliente'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    #init_db()
    app.run(debug=True)