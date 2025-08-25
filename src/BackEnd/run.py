from flask import Flask
from flask_cors import CORS
from Login.login import login_bp
#from .cadastro import cadastro_bp
#from .transferencia import transferencia_bp
from ArmazenaSolicitacoesCartao.ArmazenaSolicitacoesCartao import cartao_bp
from ArmazenaSolicitacoesCartao.ArmazenaSolicitacoesCartao import init_db

app = Flask(__name__)
CORS(app)

# registra os Blueprints
app.register_blueprint(login_bp)
#app.register_blueprint(cadastro_bp)
#app.register_blueprint(transferencia_bp)
app.register_blueprint(cartao_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
