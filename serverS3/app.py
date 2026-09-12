from flask import Flask, request, jsonify
import boto3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de S3
BUCKET_NAME = "nombre-de-tu-bucket-s3"  # Cambia esto por el nombre de tu bucket
s3_client = boto3.client('s3', region_name='us-east-1')  # Ajusta tu región

@app.route('/sensor', methods=['POST'])
def recibir_y_guardar_s3():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        # Añadir timestamp de recepción en el servidor
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        data['timestamp_servidor'] = timestamp

        # Definir la estructura del archivo en S3: lecturas/2026/09/12/lectura_15-30-00.json
        fecha_carpeta = datetime.now().strftime("%Y/%m/%d")
        file_name = f"lecturas/{fecha_carpeta}/lectura_{timestamp}.json"

        # Subir directamente el objeto JSON a S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(data, indent=2),
            ContentType='application/json'
        )

        return jsonify({
            "mensaje": "Dato guardado exitosamente en Amazon S3",
            "s3_path": f"s3://{BUCKET_NAME}/{file_name}"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sensor/archivos', methods=['GET'])
def listar_archivos_s3():
    """Endpoint opcional para consultar los últimos archivos almacenados en S3"""
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='lecturas/', MaxKeys=20)
        archivos = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify({"archivos": archivos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Escucha en todas las interfaces en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
