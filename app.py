# Arquivo: app.py (na raiz do projeto)
from flask import Flask
from flask_cors import CORS

# Importa o "módulo" de cadastro que criamos
from src.BackEnd.Cadastro.cadastro import cadastro_bp

# Cria a aplicação principal
app = Flask(__name__)
# Permite que o front-end acesse a API
CORS(app)

# "Conecta" o módulo de cadastro ao servidor principal
app.register_blueprint(cadastro_bp)

# Rota de teste para verificar se o servidor está no ar
@app.route("/")
def index():
    return "Servidor de Cadastro está funcionando!"

# Inicia o servidor quando você executa 'python app.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)