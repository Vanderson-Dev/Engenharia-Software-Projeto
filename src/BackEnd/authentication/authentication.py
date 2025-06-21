from flask import Flask, request, jsonify
from flask_cors import CORS  # importa CORS

app = Flask(__name__)
CORS(app)  # habilita CORS para todas as rotas

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('password')

    if email == "teste@teste.com" and senha == "1":
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True)
