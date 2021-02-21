#include <Servo.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "N!K ;D" ;
const char* password = "eieieiei" ;

const char* url = "http://158.108.182.17:2255/out" ; 

Servo myservo ;
int LDR = 34 ;
int pos = 0 ;
int buzz = 15 ;
char str[50] ;

const int _size = 2 * JSON_OBJECT_SIZE(3) ;

StaticJsonDocument<_size> JSONPost ;

void WiFi_Connect() {
  WiFi.disconnect() ;
  WiFi.begin(ssid, password) ;

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000) ;
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to the WiFi...") ;
  Serial.print("IP Address : ") ;
  Serial.println(WiFi.localIP()) ;
}

void _post() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http ;

    http.begin(url) ;
    http.addHeader("Content-Type", "application/json") ;

    JSONPost["mall"] = "B" ;
    serializeJson(JSONPost, str) ;
    int httpCode = http.POST(str) ;

    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString() ;
      Serial.println(httpCode) ;  
      Serial.println("Updated successfully") ; 
    } else {
      Serial.println(httpCode) ;
      Serial.println("Error on HTTP Request")  ;
    }
  } else {
    WiFi_Connect() ;  
  }
  delay(1000) ;
}

void setup() {
  myservo.attach(13) ;
  pinMode(LDR, INPUT) ;
  pinMode(buzz, OUTPUT) ;
  Serial.begin(115200) ;
  delay(4000) ;
  //myservo.write(90) ;
  WiFi_Connect() ;
}

void beep() {
  for (int i=0; i<1000; i++) {
  digitalWrite(buzz, HIGH) ;
  delayMicroseconds(500) ;
  digitalWrite(buzz, LOW) ;
  delayMicroseconds(500) ;
  }
}

void servo() {
  beep() ;
  myservo.write(90);
  _post() ;
  delay(2000) ;
  myservo.write(0) ;
}

void loop() {
  Serial.println(analogRead(LDR)) ;
  if (analogRead(LDR) > 2300) {
    servo() ;
  } 
  delay(500) ;
}
