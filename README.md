# Guía de Comandos: Servidor AWS (SQLite), Servidor On-Premise (PostgreSQL) y LilyGO (ESP32)

Este documento contiene los comandos y pasos de ejecución rápida para desplegar las dos opciones de servidor y probar los endpoints HTTP.

---

## ☁️ Opción 1: Servidor AWS EC2 (SQLite)

### 1. Conexión e Instalación de Dependencias
~bash
# Conectarse a la instancia EC2 por SSH
ssh -i /ruta/a/tu-clave.pem ubuntu@TU_IP_PUBLICA_AWS

# Actualizar repositorios e instalar pip
sudo apt update && sudo apt install -y python3-pip

# Instalar Flask
pip3 install flask
~

### 2. Ejecutar el Servidor
~bash
# Opción A: Ejecución en primer plano (para desarrollo/pruebas)
python3 app.py

# Opción B: Ejecución en segundo plano (persistente tras cerrar la sesión SSH)
nohup python3 app.py > server.log 2>&1 &
~

### 3. Monitoreo y Gestión del Proceso
~bash
# Ver si el proceso app.py está activo
ps aux | grep app.py

# Ver logs de la aplicación en tiempo real
tail -f server.log

# Detener el servidor en segundo plano
kill $(pgrep -f app.py)
~

### 4. Pruebas de Endpoints (cURL)
~bash
# CREATE: Insertar una lectura (POST)
curl -X POST http://localhost:5000/datos \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_AWS", "valor": 25.4}'

# READ: Consultar todas las lecturas (GET)
curl http://localhost:5000/datos

# UPDATE: Actualizar una lectura por ID (PUT)
curl -X PUT http://localhost:5000/datos/1 \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_AWS", "valor": 28.1}'

# DELETE: Eliminar una lectura por ID (DELETE)
curl -X DELETE http://localhost:5000/datos/1
~

---

## 🏢 Opción 2: Servidor On-Premise (PostgreSQL)

### 1. Instalación del Motor PostgreSQL y Driver Python
~bash
# Actualizar e instalar servicio PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Instalar Flask y conector nativo de PostgreSQL
pip3 install flask psycopg2-binary
~

### 2. Configurar Base de Datos y Usuario
~bash
# Entrar a la CLI de PostgreSQL
sudo -u postgres psql
~

*Ejecutar dentro de la consola de PostgreSQL (`psql`):*
~sql
CREATE DATABASE lilygo_local;
CREATE USER usuario_local WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE lilygo_local TO usuario_local;
\q
~

### 3. Iniciar el Servicio de PostgreSQL
~bash
# Verificar estado del servicio
sudo systemctl status postgresql

# Iniciar o reiniciar el servicio
sudo systemctl start postgresql
sudo systemctl restart postgresql
~

### 4. Ejecutar el Servidor On-Premise
~bash
# Ejecutar servidor local
python3 app_local.py

# Ejecutar en segundo plano
nohup python3 app_local.py > server_local.log 2>&1 &
~

### 5. Pruebas de Endpoints On-Premise (cURL)
~bash
# CREATE: Insertar una lectura (POST)
curl -X POST http://localhost:5000/datos \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_Local", "valor": 19.8}'

# READ: Consultar todas las lecturas (GET)
curl http://localhost:5000/datos

# UPDATE: Actualizar una lectura por ID (PUT)
curl -X PUT http://localhost:5000/datos/1 \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_Local", "valor": 21.0}'

# DELETE: Eliminar una lectura por ID (DELETE)
curl -X DELETE http://localhost:5000/datos/1
~

---

## 📡 Pruebas Remotas desde la LilyGO (o Cliente Externo)

Para probar los servidores desde tu máquina local apuntando a la IP pública o privada:

~bash
# Probar Servidor AWS desde equipo remoto
curl -X POST http://<TU_IP_PUBLICA_AWS>:5000/datos \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_Remote", "valor": 30.2}'

# Probar Servidor On-Premise desde red LAN
curl -X POST http://<TU_IP_LOCAL_LAN>:5000/datos \
     -H "Content-Type: application/json" \
     -d '{"dispositivo": "LilyGO_LAN", "valor": 22.4}'
~
