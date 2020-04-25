#include <Servo.h>          //using servo library
#include <IRremote.h>    //using ir library
Servo myservo;  // create servo object to control a servo

int pos = 0;    // variable to store the servo position
 
int RECV_PIN =2;     //digital 2 for ir receiver
IRrecv irrecv(RECV_PIN);     //tell it I am using that pin for that purpose
decode_results results;     //create a decoder class to store ir input
void setup(){               //regular setup
 Serial.begin(9600);   //serial for debugging
 myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  
 irrecv.enableIRIn();     //enable ir input
}     
void loop(){     
   if (irrecv.decode(&results)){     //if it saw something
int value = results.value;     //read the value that it saw
Serial.println(value);      //print that value to serial
       switch(value){     //do something depending on what value it saw
         case -23971: //first button
         myservo.write(160);   //servo up
         }     
       switch(value){     
         case -7651: //second button 
         myservo.write(20);    //servo down
         }   
       irrecv.resume();      //start looking for messages again
   }     
}      
