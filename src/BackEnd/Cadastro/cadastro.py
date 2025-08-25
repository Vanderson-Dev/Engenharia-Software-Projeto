# Arquivo: src/BackEnd/Cadastro/cadastro.py
from flask import Blueprint, request, jsonify
# Importa a classe Cliente do arquivo vizinho
from src.BackEnd.Cadastro.Cliente import Cliente

# Cria um "módulo" para as rotas de cadastro
cadastro_bp = Blueprint('cadastro', __name__)

# Define a rota específica para o cadastro
@cadastro_bp.route('/api/cadastrar-cliente', methods=['POST'])
def cadastrar_cliente_route():
    data = request.json # Pega os dados JSON enviados

    # Validação para garantir que todos os campos necessários foram enviados
    required = ['nome', 'endereco', 'cpf', 'data_nascimento', 'sexo', 'email', 'senha']
    if not all(field in data for field in required):
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    # Cria um objeto Cliente com os dados recebidos
    novo_cliente = Cliente(
        nome=data['nome'],
        endereco=data['endereco'],
        cpf=data['cpf'],
        data_nascimento=data['data_nascimento'],
        sexo=data['sexo'],
        email=data['email'],
        senha=data['senha']
    )

    # Tenta cadastrar o cliente no banco de dados
    if novo_cliente.cadastrar():
        return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 201
    else:
        return jsonify({'error': 'CPF ou e-mail já cadastrado'}), 409