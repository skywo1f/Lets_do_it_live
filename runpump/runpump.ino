int resval = 0;  // holds the value
int respin = A5; // sensor pin used
int LED_PIN = 3 ; //digital pin for relay/motor activation
void setup() { 

  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_PIN, OUTPUT); //tell it that ill be using this pin
  // start the serial console
  Serial.begin(9600);   //serial output for debugging
  
} 
  
void loop() { 
   
  resval = analogRead(respin); //Read data from analog pin and store it to resval variable
   
  if (resval<=100){           //if water is low
    Serial.println("Water Level: Empty"); 
    digitalWrite(LED_PIN, HIGH);      //turn on motor
  } 
  else if (resval>100 && resval<=300){ 
    Serial.println("Water Level: Low"); 
    digitalWrite(LED_PIN, HIGH);        //also turn on motor
    } 
  else if (resval>300 && resval<=330){ 
    Serial.println("Water Level: Medium"); 
    digitalWrite(LED_PIN, HIGH);    //also turn on motor
  } 
  else if (resval>330){ 
    Serial.println("Water Level: High"); 
    digitalWrite(LED_PIN, LOW);     //tank full, turn off motor
  }
  delay(1000); //wait for the motor to start/stop before making a new decision
}
