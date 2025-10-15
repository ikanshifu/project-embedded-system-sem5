// Libraries for Wi-Fi and HTTP communication
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";         // Wi-Fi name
const char* password = "YOUR_WIFI_PASSWORD"; // Wi-Fi password
String serverUrl = "http://yourserver.com/api/update_bin"; // URL of your backend server

// Unique ID for this bin
String binId = "BIN_001"; 

// Sensor pins
const int trigPin = D1;
const int echoPin = D2;

// Depth of the trash bin in centimeters
const int BIN_DEPTH_CM = 75; 

void setup() {
  Serial.begin(115200);
  
  // Set pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
}

void loop() {
  // 1. Measure the distance
  long duration, distance_cm;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance_cm = duration * 0.034 / 2;

  // 2. Calculate fullness percentage
  int fullness = 100 - ((float)distance_cm / BIN_DEPTH_CM * 100);
  if (fullness < 0) fullness = 0;
  if (fullness > 100) fullness = 100;
  
  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.print(" cm, Fullness: ");
  Serial.print(fullness);
  Serial.println("%");

  // 3. Send data to the server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Create JSON payload
    String jsonPayload = "{\"bin_id\":\"" + binId + "\", \"fullness\":" + String(fullness) + "}";

    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  // Wait for 15 minutes before sending the next update to save battery
  delay(15 * 60 * 1000); 
}
