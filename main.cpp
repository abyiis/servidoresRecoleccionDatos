#include <WiFi.h>
#include <HTTPClient.h>

// --- Credenciales de tu Red WiFi ---
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_CONTRASEÑA_WIFI";

// =========================================================================
// CONFIGURACIÓN DEL SERVIDOR
// =========================================================================

// Opción 1: Servidor AWS (SQLite) -> ACTIVA POR DEFECTO
const char* serverUrl = "http://TU_IP_PUBLICA_AWS:5000/datos";

// Opción 2: Servidor On-Premise Local (PostgreSQL) -> DESCOMENTA PARA USAR
// const char* serverUrl = "http://192.168.1.100:5000/datos"; // Reemplaza por la IP local de tu PC/servidor

// =========================================================================

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Conexión a la red WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n¡Conexión WiFi exitosa!");
  Serial.print("Dirección IP de la LilyGO: ");
  Serial.println(WiFi.localIP());
  Serial.print("Enviando datos a: ");
  Serial.println(serverUrl);
}

void loop() {
  // Verificar si la conexión WiFi está activa
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Inicializar la conexión HTTP hacia la URL elegida
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Simular un valor de lectura para prueba
    float valorSensor = random(200, 350) / 10.0;

    // JSON idéntico compatible con ambas soluciones Flask (SQLite y PostgreSQL)
    String jsonPayload = "{\"dispositivo\":\"LilyGO_ESP32\",\"valor\":" + String(valorSensor, 1) + "}";

    Serial.print("Enviando payload: ");
    Serial.println(jsonPayload);

    // Enviar la petición HTTP POST
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.printf("Respuesta del Servidor [%d]: %s\n", httpResponseCode, response.c_str());
    } else {
      Serial.printf("Error en el envío POST. Código de error: %d\n", httpResponseCode);
    }

    http.end(); // Liberar memoria de la sesión HTTP
  } else {
    Serial.println("Error: Conexión WiFi perdida");
  }

  // Pausa de 10 segundos entre lecturas
  delay(10000);
}
