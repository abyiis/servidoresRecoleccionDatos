# Sistema de Recolección de Datos IoT con LilyGo (ESP32)

Este repositorio contiene una suite completa de backends construidos en **Python (Flask)** diseñados para recibir telemetría enviada desde placas **LilyGo (ESP32)** a través de peticiones `HTTP POST` en el puerto **5000**. 

El proyecto incluye **4 arquitecturas de almacenamiento diferentes** (locales y en la nube de AWS), junto con el firmware en C++ (`main.cpp`) listo para subir a la microcontroladora.

---

## Arquitecturas Disponibles

| Arquitectura | Tipo | Ruta Backend | Caso de Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **1. SQLite** | Relacional Local | `serverSqlite/app.py` | Pruebas rápidas, prototipado e entornos locales sin instalación de SGBD. |
| **2. PostgreSQL Local** | Relacional Local | `PostgreSQL/app_local.py` | Desarrollo local estructurado antes del despliegue en la nube. |
| **3. AWS RDS** | Relacional Cloud | `serverRDS/app.py` | Producción en la nube con base de datos administrada y acceso SSH. |
| **4. AWS S3** | Data Lake / Objetos | `serverS3/app.py` | Almacenamiento masivo de lecturas JSON o imágenes (LilyGo CAM) a bajo costo. |

---

## Requisitos Previos

### En el Servidor (Local o EC2):
* Python 3.8 o superior.
* Gestor de paquetes `pip`.
* Puerto `5000` abierto en el Firewall (o Security Group en AWS EC2).

### En la placa LilyGo (ESP32):
* Visual Studio Code con extensión **PlatformIO** O **Arduino IDE**.
* Cable de datos USB a Type-C.

---

## Paso a Paso para la Instalación y Despliegue

### Paso 1: Clonar el Repositorio e Instalar Dependencias

Conéctate por SSH a tu servidor EC2 o abre una terminal local:

```bash
git clone https://github.com/tu-usuario/servidoresRecoleccionDatos.git
cd servidoresRecoleccionDatos-main
pip install flask flask_sqlalchemy psycopg2-binary boto3
```

---

### Paso 2: Iniciar el Servidor Elegido

Selecciona uno de los 4 servidores para ponerlo en escucha en el puerto 5000:

#### Opción A: Base de datos SQLite (Local)
```bash
python3 serverSqlite/app.py
```

#### Opción B: Base de datos PostgreSQL (Local)
*(Requiere PostgreSQL corriendo en localhost y base de datos creada)*
```bash
python3 PostgreSQL/app_local.py
```

#### Opción C: Base de datos AWS RDS
*(Asegúrate de haber configurado tu URI de conexión a RDS en `serverRDS/app.py`)*
```bash
python3 serverRDS/app.py
```

#### Opción D: Amazon S3 (Data Lake)
*(Asegúrate de que la instancia EC2 tenga un Rol IAM asignado con acceso a S3)*
```bash
python3 serverS3/app.py
```

> **Nota:** Para mantener el servidor ejecutándose en segundo plano en Linux (EC2) aunque cierres la terminal SSH, utiliza:
> ```bash
> nohup python3 serverRDS/app.py > app.log 2>&1 &
> ```

---

### Paso 3: Configurar y Cargar el Firmware LilyGo (`main.cpp`)

1. Abre el archivo `main.cpp` en PlatformIO o Arduino IDE.
2. Modifica los parámetros de red y la dirección IP de tu servidor:

```cpp
// Configuración de red WiFi
const char* WIFI_SSID = "NOMBRE_DE_TU_RED";
const char* WIFI_PASSWORD = "CONTRASEÑA_DE_TU_RED";

// IP de tu servidor (IP Local o IP Pública de la EC2)
const char* SERVER_IP = "54.123.45.67";
```

3. Selecciona la opción de backend activa cambiando la constante `TIPO_SERVIDOR`:

```cpp
#define OPCION_POSTGRESQL 1
#define OPCION_RDS        2
#define OPCION_S3         3
#define OPCION_SQLITE     4

// Selecciona tu servidor activo aquí:
#define TIPO_SERVIDOR OPCION_RDS
```

4. Compila y carga el programa en tu placa LilyGo ESP32.
5. Abre el **Monitor Serie** a `115200 baudios` para verificar que la transmisión sea exitosa (deberás recibir un código `HTTP 201`).

---

## Verificación y Pruebas Manuales (cURL)

Puedes simular el envío de datos desde la terminal de tu computadora sin la placa LilyGo ejecutando:

```bash
curl -X POST http://TU_IP_SERVIDOR:5000/sensor \
  -H "Content-Type: application/json" \
  -d '{"dispositivo": "LilyGo_Test", "valor": 25.4, "humedad": 60.2}'
```

---

## 🔒 Consideraciones de Seguridad en AWS

1. **Security Group (EC2):** Habilita reglas de entrada (*Inbound Rules*) para el puerto **22 (SSH)** y el puerto **5000 (Custom TCP)**.
2. **Security Group (RDS):** Permite conexiones al puerto 5432/3306 **únicamente** desde el Security Group asignado a tu EC2.
3. **Credenciales S3:** No guardes `AWS_ACCESS_KEY` ni `AWS_SECRET_KEY` dentro del código. Asigna un **Rol IAM** a la instancia EC2 con la política `AmazonS3FullAccess`.
