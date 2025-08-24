import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="admin",
        database="Banco",
        cursorclass=pymysql.cursors.DictCursor
    )
