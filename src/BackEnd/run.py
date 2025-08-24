from flask import Flask
from flask_cors import CORS
from Login.login import login_bp
#from .cadastro import cadastro_bp
#from .transferencia import transferencia_bp

app = Flask(__name__)
CORS(app)

# registra os Blueprints
app.register_blueprint(login_bp)
#app.register_blueprint(cadastro_bp)
#app.register_blueprint(transferencia_bp)

if __name__ == "__main__":
    app.run(debug=True)
