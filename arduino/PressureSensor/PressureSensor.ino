/*
@williamtoll
Willian Toledo

Get the pressure from sensor MPX5050GP

*/

//Used Pins
const int sensorPin = A1;

long ts;

void setup() { 
    Serial.begin(57600);
    ts = millis();
}

void loop() {
  int pressure = analogRead(sensorPin);
  //Read every 500 ms
   if (millis() > ts + 500) {
       ts = millis();
       //Serial.println(ts);
       Serial.println(pressure);
   }
}
