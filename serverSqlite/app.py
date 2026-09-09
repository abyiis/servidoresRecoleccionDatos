from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "lilygo.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabla lista para recibir datos típicos de tu LilyGO (ej. id, sensor, valor, timestamp)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lecturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo TEXT,
            valor REAL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 1. CREATE: Tu LilyGO enviará un POST con datos JSON
@app.route('/datos', methods=['POST'])
def crear_registro():
    data = request.get_json()
    if not data or 'dispositivo' not in data or 'valor' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lecturas (dispositivo, valor) VALUES (?, ?)", 
                   (data['dispositivo'], data['valor']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"mensaje": "Registro creado", "id": nuevo_id}), 201

# 2. READ: Obtener todas las lecturas
@app.route('/datos', methods=['GET'])
def obtener_registros():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lecturas ORDER BY id DESC")
    filas = cursor.fetchall()
    conn.close()
    
    lecturas = [{"id": f[0], "dispositivo": f[1], "valor": f[2], "fecha": f[3]} for f in filas]
    return jsonify(lecturas), 200

# 3. UPDATE: Actualizar una lectura específica por ID
@app.route('/datos/<int:id_registro>', methods=['PUT'])
def actualizar_registro(id_registro):
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE lecturas SET dispositivo = ?, valor = ? WHERE id = ?", 
                   (data.get('dispositivo'), data.get('valor'), id_registro))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Registro actualizado"}), 200

# 4. DELETE: Eliminar una lectura por ID
@app.route('/datos/<int:id_registro>', methods=['DELETE'])
def eliminar_registro(id_registro):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lecturas WHERE id = ?", (id_registro,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Registro eliminado"}), 200

if __name__ == '__main__':
    init_db()
    # Permitir conexiones externas desde tu puerto 5000
    app.run(host='0.0.0.0', port=5000)
