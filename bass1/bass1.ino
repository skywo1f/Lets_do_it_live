#include <FastLED.h>
#define LED_PIN     7
#define NUM_LEDS    300
CRGB leds[NUM_LEDS];
int tempo = 1000;
const int songLength = 8;

typedef struct {
    int coord;
    int tab;
} note;    //  creates a struct type dataNode

note mySong[songLength] =  {{0, 3},{0, 5}, {1,2},{1,3},{1,5},{2,2},{2,4},{2,5}};
//note mySong[songLength] =  {{3, 15},{3, 14}, {3,13},{3,12},{3,11},{3,10},{3,9},{3,8},{3, 7},{3, 6}, {3,5},{3,4},{3,3},{3,2},{3,1},{3,0}};

int ledsPerLayer[] =  {6,6 ,5,5,5,5,5,5,5,5,5,4,4,4,4,4};
int ledsInBetween[] = {6,10,9,9,9,9,9,3,9,9,8,9,9,9,9,2};

int sumUp(int coord, int tab){
  int thisLayer = 15 - tab;
  int index = 0;  
  for (int i = 0; i < thisLayer; i++) {
    int ledsThisTab = ledsPerLayer[i];
    int betweenThisTab = ledsInBetween[i];
    index = index + ledsThisTab + betweenThisTab;
  }
  index = index + coord + ledsInBetween[thisLayer];
if (ledsPerLayer[15-tab] == 6) {
  if (coord == 1 || coord == 2){
    index = index + 1;
  }
  if (coord ==3){
    index = index + 2;
  }
}
if (ledsPerLayer[15-tab] == 5) {
  if (coord == 2 || coord == 3){
    index = index + 1;
  }
}
  return index;
}

void playNote(int index, int coord) {
  if (coord == 0) { 
     leds[index] = CRGB {0,128,0}  ;//green 
  }
  if (coord == 1) {
     leds[index] = CRGB {0,0,128} ;  //blue
  }
    if (coord == 2) {
     leds[index] = CRGB {128,0,0}  ; //red
  }
    if (coord == 3) {
     leds[index] = CRGB {128,128,0} ;  //yellow
  }
   FastLED.show();
   Serial.print("\n lighting up ");
   Serial.print(index);
}





void clearNotes(int index){
    leds[index] = CRGB {0,0,0} ;  //black
    FastLED.show();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
}

void loop() {
 // put your main code here, to run repeatedly:
  for (int i = 0; i < songLength; i++){
    note current = mySong[i];
    int thisCoord = current.coord;
    int thisTab = current.tab;
    int index = sumUp(thisCoord,thisTab);
    playNote(index,thisCoord);
    delay(tempo);
    clearNotes(index);
  }
}
