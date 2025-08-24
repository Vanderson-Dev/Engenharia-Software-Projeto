from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime

cartao_bp = Blueprint('cartao', __name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_cartao (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            birth_date DATE NOT NULL,
            card_type VARCHAR(50) NOT NULL,
            reason VARCHAR(50) NOT NULL,
            other_reason TEXT,
            additional_info TEXT,
            status VARCHAR(20) DEFAULT 'pendente',
            created_at DATETIME NOT NULL,
            INDEX idx_cpf (cpf),
            INDEX idx_status (status)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@cartao_bp.route('/api/solicitar-cartao', methods=['POST'])
def solicitar_cartao():
    data = request.json
    required = ['fullName', 'cpf', 'birthDate', 'cardType', 'reason']
    
    for campo in required:
        if not data.get(campo):
            return jsonify({'error': f'O campo {campo} é obrigatório'}), 400
    
    if data['reason'] == 'outro' and not data.get('otherReason'):
        return jsonify({'error': 'Por favor, especifique o motivo da solicitação'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO solicitacoes_cartao (
                full_name, cpf, birth_date, card_type, reason,
                other_reason, additional_info, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['fullName'],
            data['cpf'],
            data['birthDate'],
            data['cardType'],
            data['reason'],
            data.get('otherReason', ''),
            data.get('additionalInfo', ''),
            datetime.now()
        ))
        conn.commit()
        return jsonify({'message': 'Solicitação recebida com sucesso!'}), 201
    except pymysql.MySQLError:
        return jsonify({'error': 'Erro ao processar solicitação'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

