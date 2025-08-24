from flask import Blueprint, request, jsonify
import pymysql

login_bp = Blueprint('login', __name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clientes WHERE email=%s AND senha=%s", (email, password))
        user = cursor.fetchone()
    conn.close()

    return jsonify({"success": bool(user)})
