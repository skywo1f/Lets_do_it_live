const int pingPin = 7; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 6; // Echo Pin of Ultrasonic Sensor

#include <FastLED.h>        //addressable led library

#define LED_PIN_R     10    //red leds pin 10
#define LED_PIN_Y     11    //yellow leds pin 10
#define LED_PIN_G     12    //green leds pin 10

#define NUM_LEDS    7       //number of leds on the strip
#define BRIGHTNESS  64      //default brightness
#define LED_TYPE    WS2811    //led strip type
#define COLOR_ORDER GRB       //grb rgb etc
CRGB leds_r[NUM_LEDS];      //prepare color arrays for each strip
CRGB leds_y[NUM_LEDS];
CRGB leds_g[NUM_LEDS];

#define UPDATES_PER_SECOND 100      //how often to update the colors

void setup() {
    delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN_R, COLOR_ORDER>(leds_r, NUM_LEDS).setCorrection( TypicalLEDStrip ); //start up led structure
    FastLED.addLeds<LED_TYPE, LED_PIN_Y, COLOR_ORDER>(leds_y, NUM_LEDS).setCorrection( TypicalLEDStrip ); 
    FastLED.addLeds<LED_TYPE, LED_PIN_G, COLOR_ORDER>(leds_g, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );     //set default brighness
        
   Serial.begin(9600); // Starting Serial Terminal
   Serial.print("starting device ");  //serial debug
}

void loop() {
   long duration, inches;       //initialize distances
   pinMode(pingPin, OUTPUT);    //check output pin
   digitalWrite(pingPin, LOW); //send ping
   delayMicroseconds(2);      
   digitalWrite(pingPin, HIGH); 
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   pinMode(echoPin, INPUT);   //read echo
   duration = pulseIn(echoPin, HIGH); //find how long it took
   inches = microsecondsToInches(duration);   //use speed of sound to approximate distance
   Serial.print(inches);        //print
   Serial.println("in, ");
   delay(100);
   static uint8_t colorIndex = 0; //prepare default colors
   uint8_t brightness = 255;      //reset brighness

   if (inches < 10)             //if we are within 10 inches, stop
   {
        for( int i = 0; i < NUM_LEDS; i++) {      //loop through leds on strips
        leds_r[i] = CRGB {brightness,0,0};        //turn on red on red strip
        leds_y[i] = CRGB {0,0,0};                 //turn off other strips
        leds_g[i] = CRGB {0,0,0};
        Serial.println("red ");   
        FastLED.show();                           //activate leds
    }
   }
    if (inches > 10 && inches < 20)                 //similar for yellow and green
   {
        for( int i = 0; i < NUM_LEDS; i++) {
        leds_r[i] = CRGB {0,0,0};
        leds_y[i] = CRGB {brightness,brightness,0};
        leds_g[i] = CRGB {0,0,0};
        Serial.println("yellow ");
        FastLED.show();
    }
   }
      if (inches > 20)
   {
        for( int i = 0; i < NUM_LEDS; i++) {
        leds_r[i] = CRGB {0,0,0};
        leds_y[i] = CRGB {0,0,0};
        leds_g[i] = CRGB {0,brightness,0};
        Serial.println("green ");
        FastLED.show();
    }
   }  
}

long microsecondsToInches(long microseconds) {            //convert microseconds to inches
   return microseconds / 74 / 2;
}
