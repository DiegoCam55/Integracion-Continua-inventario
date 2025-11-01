from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Conexión a MySQL (el host será el nombre del servicio del contenedor)
def get_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="rootpassword",
        database="mi_base"
    )

@app.route("/")
def home():
    return jsonify({"message": "Backend Flask funcionando correctamente!"})

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
