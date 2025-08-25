from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="admin",  # Substitua pela sua senha do MySQL
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SolicitacaoCartao (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome_completo VARCHAR(100) NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            data_nascimento DATE NOT NULL,
            tipo_cartao VARCHAR(50) NOT NULL,
            motivo_solicitacao VARCHAR(100) NOT NULL,
            outro_motivo VARCHAR(255),
            info_adicional VARCHAR(255),
            created_at DATETIME NOT NULL,
            CONSTRAINT unique_cpf UNIQUE (cpf)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/api/solicitar-cartao', methods=['POST'])
def solicitar_cartao():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado recebido'}), 400

    # Campos obrigatórios do formulário
    required_fields = ['fullName', 'cpf', 'birthDate', 'cardType', 'reason']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'O campo {field} é obrigatório'}), 400

    # Determinar o motivo da solicitação e outro motivo
    motivo = data['reason']
    outro_motivo = data.get('otherReason', '') if motivo == 'outro' else ''
    if motivo == 'outro' and not outro_motivo:
        return jsonify({'error': 'Por favor, especifique o motivo da solicitação'}), 400
    motivo_solicitacao = outro_motivo if motivo == 'outro' else motivo

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SolicitacaoCartao (
                nome_completo, cpf, data_nascimento, tipo_cartao, 
                motivo_solicitacao, outro_motivo, info_adicional, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['fullName'],
            data['cpf'],
            data['birthDate'],
            data['cardType'],
            motivo_solicitacao,
            outro_motivo,
            data.get('additionalInfo', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        return jsonify({'message': 'Solicitação recebida com sucesso!'}), 201

    except pymysql.Error as e:
        error_msg = str(e)
        if e.args[0] == 1062:  # Erro de duplicação (CPF único)
            return jsonify({'error': 'Erro: CPF já possui uma solicitação registrada'}), 400
        elif e.args[0] == 1406:  # Erro de valor muito longo
            return jsonify({'error': 'Erro: Um ou mais campos excedem o limite de caracteres permitido'}), 400
        elif e.args[0] == 1292:  # Erro de formato de data inválida
            return jsonify({'error': 'Erro: Formato de data inválido. Use o formato aaaa-mm-dd'}), 400
        else:
            return jsonify({'error': f'Erro ao processar solicitação: {error_msg}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    #init_db()  # Cria a tabela se não existir
    app.run(debug=True, host='0.0.0.0', port=5000)