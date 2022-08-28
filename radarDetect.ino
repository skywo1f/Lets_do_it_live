int outPin = 9;  // LED connected to digital pin 13
int inPin = 3;    // pushbutton connected to digital pin 7
int value = 0;      // variable to store the read value
int screenState = 0;
unsigned long timeStart = 0;
void setup() {
  pinMode(outPin, OUTPUT);  
  digitalWrite(outPin, HIGH);
  pinMode(inPin,INPUT);
  Serial.begin(9600); // open the serial port at 9600 bps:
 
}

void loop() {
  value = digitalRead(inPin);   // read the input pin
  //Serial.println(value);
  if (value == HIGH){
    timeStart = millis();
    if (screenState == 0){
       digitalWrite(outPin,LOW);
       delay(250);
       digitalWrite(outPin,HIGH);
       screenState = 1;
    }
  }
  if (millis() - timeStart > 10000){
    if(screenState == 1){
       digitalWrite(outPin,LOW);
       delay(250);
       digitalWrite(outPin,HIGH);
       screenState = 0;
    }
  }
  delay(100);
Serial.println(screenState);
Serial.println(millis()-timeStart);
Serial.println("time now");
Serial.println(millis());
Serial.println(timeStart);
}
