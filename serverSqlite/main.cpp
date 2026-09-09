#include <WiFi.h>
#include <HTTPClient.h>

// --- Configuración de Red y Servidor ---
const char* ssid = "TU_RED_WIFI";
const char* password = "TU_CONTRASEÑA_WIFI";

// Reemplaza con la IP PÚBLICA de tu instancia EC2 de AWS
const char* serverUrl = "http://TU_IP_PUBLICA_AWS:5000/datos";

void setup() {
  Serial.begin(115200);
  
  // Conexión a la red WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n¡Conectado a WiFi!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Inicializar cliente HTTP con la URL del servidor
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Simular un valor de lectura (ejemplo: temperatura o sensor)
    float valorSensor = random(200, 350) / 10.0;

    // Construir la cadena JSON a enviar
    String jsonPayload = "{\"dispositivo\":\"LilyGO_ESP32\",\"valor\":" + String(valorSensor, 1) + "}";

    Serial.print("Enviando POST a ");
    Serial.println(serverUrl);
    Serial.print("Payload: ");
    Serial.println(jsonPayload);

    // Enviar la petición HTTP POST
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Código de respuesta: ");
      Serial.println(httpResponseCode);
      Serial.print("Respuesta del servidor: ");
      Serial.println(response);
    } else {
      Serial.print("Error en el envío POST. Código: ");
      Serial.println(httpResponseCode);
    }

    http.end(); // Liberar recursos
  } else {
    Serial.println("Error: Conexión WiFi perdida");
  }

  // Esperar 10 segundos antes de enviar la siguiente lectura
  delay(10000);
}
