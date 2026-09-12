from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Reemplaza con tus datos de RDS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:password@rds-endpoint.amazonaws.com:5432/mitabla'
db = SQLAlchemy(app)

class LecturaSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    dispositivo = db.Column(db.String(50), nullable=False)

@app.route('/sensor', methods=['POST'])
def crear_lectura():
    data = request.json
    nueva_lectura = LecturaSensor(valor=data['valor'], dispositivo=data['dispositivo'])
    db.session.add(nueva_lectura)
    db.session.commit()
    return jsonify({"mensaje": "Dato guardado"}), 201

@app.route('/sensor', methods=['GET'])
def obtener_lecturas():
    lecturas = LecturaSensor.query.all()
    return jsonify([{"id": l.id, "valor": l.valor, "dispositivo": l.dispositivo} for l in lecturas])

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
