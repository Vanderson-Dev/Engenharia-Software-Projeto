# Arquivo: app.py (na raiz do projeto)
from flask import Flask
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Importa o "módulo" de cadastro que criamos
from src.BackEnd.Cadastro.cadastro import cadastro_bp
from src.BackEnd.Login.login import login_bp
from src.BackEnd.Rotas.rotas import deposito_bp
from src.BackEnd.Rotas.rotas import saque_bp
from src.BackEnd.Rotas.rotas import saldo_bp
from src.BackEnd.Rotas.rotas import transferencia_bp
from src.BackEnd.Rotas.rotas import investir_bp
from src.BackEnd.Rotas.rotas import extrato_bp
# Cria a aplicação principal
app = Flask(__name__)
CORS(app)

# "Conecta" o módulo de cadastro ao servidor principal
app.register_blueprint(cadastro_bp)
app.register_blueprint(login_bp)
app.register_blueprint(deposito_bp)
app.register_blueprint(saque_bp)
app.register_blueprint(saldo_bp)
app.register_blueprint(transferencia_bp)
app.register_blueprint(investir_bp)
app.register_blueprint(extrato_bp)

# Rota de teste para verificar se o servidor está no ar
@app.route("/")
def index():
    return "Servidor de Cadastro está funcionando!"

# Inicia o servidor quando você executa 'python app.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)