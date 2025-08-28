from flask import Blueprint, request, jsonify
import pymysql

# Criando o Blueprint
login_bp = Blueprint("login", __name__)

class BancoDigital:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "admin"
        self.database = "Banco"

    def get_db_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def login(self, email, senha):
        conn = self.get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM clientes WHERE email=%s AND senha=%s",
                (email, senha)
            )
            user = cursor.fetchone()
        conn.close()
        return user is not None

# instância da classe
banco = BancoDigital()

# rota do login usando a classe
@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("password")

    if banco.login(email, senha):
        return jsonify({"success": True})
    return jsonify({"success": False})
