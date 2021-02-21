#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

Servo myservo;

const char* ssid = "N!K ;D" ;
const char* password = "eieieiei" ;
const char* url1 = "http://158.108.182.17:2255/in" ; 
const char* url2 = "http://158.108.182.17:2255/in" ; 
char str[50] ;
const int _size = 2 * JSON_OBJECT_SIZE(3) ;

StaticJsonDocument<_size> JSONPost ;

int ledRed = 19;
int ledGreen = 18;
int ldr = 32;
int pos ;
int ldrRead;

int MotorPin1 = 2;
int MotorPin2 = 0;

// which analog pin to connect
int THERMISTORPIN = 34;
// resistance at 25 degrees C
#define THERMISTORNOMINAL 10000
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3500
// the value of the 'other' resistor
#define SERIESRESISTOR 500
int samples[NUMSAMPLES];

void setup(void){
  pinMode(ledRed, OUTPUT); 
  pinMode(ledGreen, OUTPUT);
  digitalWrite(ledRed,LOW);
  digitalWrite(ledGreen,LOW);

  myservo.attach(23);
  myservo.write(90);
  delay(100);

  pinMode(MotorPin1, OUTPUT);
  pinMode(MotorPin2, OUTPUT);

  pinMode(ldr,INPUT);
  
  lcd.begin();

  lcd.print("COME");
  lcd.setCursor(5,0);
  lcd.print("ON!");
  lcd.setCursor(0,1);
  lcd.print("LET's");
  lcd.setCursor(6,1);
  lcd.print("GO!");
  delay(3000);
  lcd.clear();
  lcd.print("Touch_Me");
  Serial.begin(115200) ;
  delay(4000) ;
  WiFi_Connect() ;
}

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

void _post(float x) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http ;

    http.begin(url2) ;
    http.addHeader("Content-Type", "application/json") ;

    JSONPost["mall"] = "B" ;
    JSONPost["temp"] = x ;
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

void loop(void){
  uint8_t i;
  float average;
  // take N samples in a row, with a slight delay
  for(i=0; i< NUMSAMPLES; i++){
  samples[i]= analogRead(THERMISTORPIN);
  delay(10);
  }
  // average all the samples out
  average =0;
  for(i=0; i< NUMSAMPLES; i++){
  average += samples[i];
  }
  average /= NUMSAMPLES;
  Serial.print("Average analog reading ");
  Serial.println(average);
  // convert the value to resistance
  average =1023/ average -1;
  average = SERIESRESISTOR / average;
  Serial.print("Thermistor resistance ");
  Serial.println(average);
  float steinhart;
  steinhart = average / THERMISTORNOMINAL;// (R/Ro)
  steinhart = log(steinhart);// ln(R/Ro)
  steinhart /= BCOEFFICIENT;// 1/B * ln(R/Ro)
  steinhart +=1.0/(TEMPERATURENOMINAL +273.15);// + (1/To)
  steinhart =1.0/ steinhart;// Invert
  steinhart -=273.15;// convert to C
  Serial.print("Temperature ");
  Serial.print(steinhart);
  Serial.println(" *C");
  ldrRead = analogRead(ldr);
  Serial.println(ldrRead);
  if (analogRead(ldr) > 2000 && steinhart >= 35.50) {
    lcd.clear();
    lcd.print("Temp: ");
    lcd.setCursor(12,0);
    lcd.print("*C");
    lcd.setCursor(6,0);
    lcd.print(steinhart);

    if (steinhart <= 38.00) {
      lcd.setCursor(6,1); 
      lcd.print("PASS!");
      digitalWrite(ledGreen,HIGH);
      delay(2000) ;
      digitalWrite(ledGreen,LOW);
      myservo.write(0) ;
      delay(1000) ;
      digitalWrite(MotorPin1, LOW); //สั่งงานให้ขา OUT3  เป็นขารับไฟจากขา OUT4
      digitalWrite(MotorPin2, HIGH); //สั่งงานให้โมดูลขับมอเตอร์จ่ายไฟ ออกขา OUT4
      Serial.println("Motor Left");
      delay(1000);
      digitalWrite(MotorPin1, LOW); //สั่งงานให้ขา OUT3 หยุดจ่ายไฟ
      digitalWrite(MotorPin2, LOW); //สั่งงานให้ขา OUT4 หยุดจ่ายไฟ
      Serial.println("Motor STOP");
      delay(1000) ;
      digitalWrite(MotorPin1, HIGH); //สั่งงานให้ขา OUT3  เป็นขารับไฟจากขา OUT4
      digitalWrite(MotorPin2, LOW); //สั่งงานให้โมดูลขับมอเตอร์จ่ายไฟ ออกขา OUT4
      Serial.println("Motor Right");
      delay(1000);
      digitalWrite(MotorPin1, LOW); //สั่งงานให้ขา OUT3 หยุดจ่ายไฟ
      digitalWrite(MotorPin2, LOW); //สั่งงานให้ขา OUT4 หยุดจ่ายไฟ
      Serial.println("Motor STOP");
    }
    else {
      lcd.setCursor(6,1); 
      lcd.print("FAIL!");
      digitalWrite(ledRed,HIGH);
      delay(2000) ;
      digitalWrite(ledRed,LOW);
      delay(2000);
    }
    delay(1000) ; 
    myservo.write(90);
    _post(steinhart) ;
  }
  lcd.clear();
  lcd.print("Touch_Me");
  delay(1000) ;
}
