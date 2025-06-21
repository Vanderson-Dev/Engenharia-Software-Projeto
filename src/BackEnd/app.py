from flask import Flask
from flask_cors import CORS

from authenticationFolder.authentication import login_bp

from ArmazenaSolicitacoesCartao.ArmazenaSolicitacoesCartao import cartao_bp, init_db

app = Flask(__name__)
CORS(app)

# Registra os blueprints
app.register_blueprint(login_bp)
app.register_blueprint(cartao_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
