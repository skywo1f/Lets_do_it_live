#include <FastLED.h>
#define LED_PIN     7
#define NUM_LEDS    300
CRGB leds[NUM_LEDS];          //led info
int tempo = 1000;             //speed of song

typedef struct {
    int coord;
    int tab;
} note;    //  note class requires "x and y coordinates"

//const int songLength = 8;
//note mySong[songLength] =  {{0, 3},{0, 5}, {1,2},{1,3},{1,5},{2,2},{2,4},{2,5}};

const int songLength = 35;        //song length and copied over song
note mySong[songLength] = {{0, 1}, {0, 1}, {0, 1}, {0, 2}, {30, 5}, {3, 2}, {2, 2}, {0, 2}, {2, 2}, {30, 5}, {30, 5}, {0, 1}, {0, 2}, {30, 5}, {3, 2}, {2, 2}, {0, 2}, {5, 2}, {30, 5}, {30, 5}, {0, 1}, {0, 2}, {30, 5}, {3, 2}, {2, 2}, {0, 2}, {2, 2}, {30, 5}, {2, 2}, {30, 5}, {3, 2}, {2, 2}, {3, 1}};

//note mySong[songLength] =  {{3, 15},{3, 14}, {3,13},{3,12},{3,11},{3,10},{3,9},{3,8},{3, 7},{3, 6}, {3,5},{3,4},{3,3},{3,2},{3,1},{3,0}};

int ledsPerLayer[] =  {6,6 ,5,5,5,5,5,5,5,5,5,4,4,4,4,4};                   //guitar specific info
int ledsInBetween[] = {6,10,9,9,9,9,9,3,9,9,8,9,9,9,9,2};                   //since lights are one long loop

int sumUp(int coord, int tab){                                              //find which number a specific led is
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

void playNote(int index, int coord,int strength) {                            //select which color to turn on
  if (coord == 0) { 
     leds[index] = CRGB {0,strength,0}  ;//green 
  }
  if (coord == 1) {
     leds[index] = CRGB {0,0,strength} ;  //blue
  }
    if (coord == 2) {
     leds[index] = CRGB {strength,0,0}  ; //red
  }
    if (coord == 3) {
     leds[index] = CRGB {strength,strength,0} ;  //yellow
  }
   FastLED.show();
   Serial.print("\n lighting up ");
   Serial.print(index);
}





void clearNotes(int index){                                           //clear note 
    leds[index] = CRGB {0,0,0} ;  //black
    FastLED.show();
}

void setup() {                      
  // put your setup code here, to run once:
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);          //prepare led module
}

void loop() {
 // put your main code here, to run repeatedly:
  for (int i = 0; i < songLength; i++){
    note current = mySong[i];
    int thisCoord = current.coord;
    int thisTab = current.tab;


      int index = sumUp(thisCoord,thisTab);                         //find index of light
      playNote(index,thisCoord,128);                                //play that index
      note next = mySong[(i+ 1)%songLength];
      int nextCoord = next.coord;
      int nextTab = next.tab;
      int nextIndex = sumUp(nextCoord,nextTab);                     //get the next index ready
      playNote(nextIndex,nextCoord,4);                              //dim the following note
    if(thisCoord < 3){                                              //if this note is real wait the normal time
      delay(tempo);
    } else {                                                        //if there is a break, wait double
      delay(2*tempo);
    }
    
    clearNotes(index);                                              //clear notes
    clearNotes(nextIndex);
  }

  delay(10000);                                                     //dont start over right away after song
}
