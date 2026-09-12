#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Configuración WiFi
const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASSWORD = "TU_PASSWORD_WIFI";

// Dirección IP de tu servidor (EC2 o Servidor Local)
const char* SERVER_IP = "192.168.1.100"; // Cambiar por tu IP Pública de EC2 o IP local

// Selecciona el servidor destino descomentando SOLO UNO:
#define OPCION_POSTGRESQL 1
#define OPCION_RDS        2
#define OPCION_S3         3
#define OPCION_SQLITE     4

#define TIPO_SERVIDOR OPCION_POSTGRESQL

// Configuración del endpoint según la opción elegida
String obtenerUrlServidor() {
  String baseUrl = "http://" + String(SERVER_IP) + ":5000";
  
  #if TIPO_SERVIDOR == OPCION_POSTGRESQL
    return baseUrl + "/sensor";          // Servidor PostgreSQL Local
  #elif TIPO_SERVIDOR == OPCION_RDS
    return baseUrl + "/sensor";          // Servidor AWS RDS
  #elif TIPO_SERVIDOR == OPCION_S3
    return baseUrl + "/sensor";          // Servidor AWS S3
  #elif TIPO_SERVIDOR == OPCION_SQLITE
    return baseUrl + "/sensor";          // Servidor SQLite Local
  #endif
}

void conectarWiFi() {
  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado!");
  Serial.print("IP asignada: ");
  Serial.println(WiFi.localIP());
}

void enviarDatosSensor() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String serverUrl = obtenerUrlServidor();
    
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Simulación de lectura del sensor LilyGo
    float temperatura = random(200, 350) / 10.0;
    float humedad = random(400, 800) / 10.0;
    
    // Construcción del JSON
    String jsonPayload = "{";
    jsonPayload += "\"dispositivo\":\"LilyGo_ESP32\",";
    jsonPayload += "\"valor\":" + String(temperatura) + ",";
    jsonPayload += "\"humedad\":" + String(humedad);
    jsonPayload += "}";

    Serial.println("Enviando petición a: " + serverUrl);
    Serial.println("Payload: " + jsonPayload);

    int httpCode = http.POST(jsonPayload);

    if (httpCode > 0) {
      String response = http.getString();
      Serial.printf("Respuesta HTTP: %d\n", httpCode);
      Serial.println("Respuesta servidor: " + response);
    } else {
      Serial.printf("Error enviando POST: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  } else {
    Serial.println("Error: Conexión WiFi perdida");
  }
}

void setup() {
  Serial.begin(115200);
  conectarWiFi();
}

void loop() {
  enviarDatosSensor();
  delay(10000); // Envío cada 10 segundos
}
