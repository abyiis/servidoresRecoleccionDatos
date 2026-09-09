from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Datos de conexión al PostgreSQL local
DB_CONFIG = {
    "dbname": "lilygo_local",
    "user": "usuario_local",
    "password": "password123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Crear tabla con clave autoincrementable y timestamp en PostgreSQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id SERIAL PRIMARY KEY,
            dispositivo VARCHAR(50) NOT NULL,
            valor REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# 1. CREATE (POST)
@app.route('/datos', methods=['POST'])
def crear_registro():
    data = request.get_json()
    if not data or 'dispositivo' not in data or 'valor' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO lecturas (dispositivo, valor) VALUES (%s, %s) RETURNING id;",
        (data['dispositivo'], data['valor'])
    )
    nuevo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Registro creado en On-Premise", "id": nuevo_id}), 201

# 2. READ (GET)
@app.route('/datos', methods=['GET'])
def obtener_registros():
    conn = get_db_connection()
    # RealDictCursor permite devolver los registros como diccionarios/JSON automáticamente
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM lecturas ORDER BY id DESC;")
    lecturas = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(lecturas), 200

# 3. UPDATE (PUT)
@app.route('/datos/<int:id_registro>', methods=['PUT'])
def actualizar_registro(id_registro):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE lecturas SET dispositivo = %s, valor = %s WHERE id = %s;",
        (data.get('dispositivo'), data.get('valor'), id_registro)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Registro actualizado"}), 200

# 4. DELETE (DELETE)
@app.route('/datos/<int:id_registro>', methods=['DELETE'])
def eliminar_registro(id_registro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lecturas WHERE id = %s;", (id_registro,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Registro eliminado"}), 200

if __name__ == '__main__':
    init_db()
    # Escucha en la IP local (red local LAN)
    app.run(host='0.0.0.0', port=5000)
