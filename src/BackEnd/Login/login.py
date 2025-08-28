from flask import Blueprint, request, jsonify
from BackEnd.Classes.Cliente import Cliente

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("password")

    cliente = Cliente.autenticarCliente(email, senha)
    if cliente:
        # Aqui você pode retornar dados do cliente se quiser
        return jsonify({"success": True, "cliente": {"nome": cliente["nome"], "email": cliente["email"]}})
    return jsonify({"success": False})