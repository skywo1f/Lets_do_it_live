#include "FastLED.h"
// How many leds in your strip?
#define NUM_LEDS 300

#define DATA_PIN 3

// Rotary Encoder Inputs
#define CLK 4
#define DT 5
#define SW 6

CRGB leds[NUM_LEDS];

CRGB bGhostColor = CRGB(0,0,128);
CRGB bGhostNormal = CRGB(0,0,128);
CRGB bGhostSuper = CRGB(128,128,128);

CRGB rGhostColor = CRGB(0,128,0);
CRGB rGhostNormal = CRGB(0,128,0);
CRGB rGhostSuper = CRGB(128,128,128);

CRGB beanColor = CRGB(1,4,0);

int counter = 0;
int currentStateCLK;
int lastStateCLK;
String currentDir ="";
unsigned long lastButtonPress = 0;

int lastPacIdx;
int pacIdx;


typedef enum {
          pacman,bean,super,nothing,rGhost,bGhost
} fieldVals;


struct bGhost {
   int idx;
   int lastIdx;
   char gName[5] = "inky";
   fieldVals history;
};


struct rGhost {
   int idx;
   int lastIdx;
   char gName[7] = "blinky";
   fieldVals history;
};




//leds[cur] = CRGB (r, g, b);
int superTime = 1000;
int superCounter;
int superFreq = 10;
int gTick = 50;
//int gTick = 100000;
int ghostTimer = 0;
int stillGoing = true;
int rTimer = 0;
int bTimer = 0;
int deathReturn;
int rTimerFreeze = 1000;
int bTimerFreeze = 1000;
int path = 1;


fieldVals field[NUM_LEDS];

void initField(CRGB *leds,struct bGhost *inky,struct rGhost *blinky){
  for (int i = 0; i < NUM_LEDS; i++){
    leds[i] = CRGB(0,0,0);
    field[i] = super;
  }
      
  for (int i = 1; i < NUM_LEDS - 1; i++){
    field[i] = bean;
    leds[i] = beanColor;        //bean color
    if (i%superFreq == 0) {
      leds[i] = CRGB(16,128,0);
      field[i] = super;
    }
  }
  updatePacman(leds,0,0);
  field[blinky->idx] = rGhost;
  field[inky->idx] = bGhost;
  leds[blinky->idx] = rGhostColor;
  leds[inky->idx] = bGhostColor;
}

void clearCell(CRGB *leds,int idx){
  leds[idx] = CRGB(0,0,0);
  FastLED.show();
}

void putBack(int GhostLast, fieldVals GhostHist, CRGB *leds){
    if (GhostHist ==  bean){
      leds[GhostLast] = beanColor;
      field[GhostLast] = bean;
    }
    if (GhostHist == super){
      leds[GhostLast] = CRGB(16,128,0);
      field[GhostLast] = super;
    }
    if (GhostHist == nothing) {
      leds[GhostLast] = CRGB(0,0,0);
      field[GhostLast] = nothing;
    }
    if (GhostHist == bGhost){
      leds[GhostLast] = bGhostColor;
      field[GhostLast] = bGhost;       //should be bghost
    }
    if (GhostHist == rGhost){
      leds[GhostLast] = rGhostColor;
      field[GhostLast] = rGhost;       //should be rghost
    }
}

int updateRGhost(CRGB *leds,struct rGhost *blinky,CRGB rGhostColor){
  putBack(blinky->lastIdx , blinky->history,leds);
  blinky->lastIdx = blinky->idx; 


  if (blinky->idx < pacIdx){
    blinky->idx++;
  }
  else {
    blinky->idx--;
  }
  if (blinky->idx == 0) {
    blinky->idx = 1;
  }
  blinky->history  = field[blinky->idx ];
  leds[blinky->idx] = rGhostColor;
  field[blinky->idx] = rGhost;
}

void updateBGhost(CRGB *leds,struct bGhost *inky,CRGB bGhostColor){
  putBack(inky->lastIdx, inky->history,leds);     //put back the history of the last position

  inky->lastIdx = inky->idx;                      //record position before changing it
  if(inky->idx == 1) {
    path = (path+1)%2;
  }
  if(inky->idx == NUM_LEDS - 1) {
    path = (path+1)%2;
  }

  if(path){
    inky->idx = (inky->idx + 1);
  } else {
    inky->idx = (inky->idx - 1);
  }
  inky->history = field[inky->idx];           //save history of position before I go there
  leds[inky->idx] = bGhostColor;
  field[inky->idx] = bGhost;
  
}

void updatePacman(CRGB *leds,  int idx,int lastIdx){
  leds[idx] = CRGB(64,64,0);
  FastLED.show();
  clearCell(leds,lastIdx);
  field[lastIdx] = nothing;
  field[idx] = pacman;
}


int checkDeath(CRGB *leds,int superCounter,struct bGhost *inky,struct rGhost *blinky){
  if (blinky->idx == pacIdx || inky->idx == pacIdx){
    if (superCounter > 0){
      if (blinky->idx == pacIdx) {
        return 2;     //tagged red ghost
      } else {
        return 3;     //tagged blue ghost
      }
    } else {
      for (int i = 0; i < NUM_LEDS; i++){
        leds[i] = CRGB(0,64,0);     //lose the game
        
      }
      return 0;
    }

  } else {
    return 1;
  }
}

int checkWin(CRGB *leds){
  int anyBeanLeft = false;  
  for (int i = 0; i < NUM_LEDS; i++){
    if (field[i] == bean) {
      anyBeanLeft = true;
    }
  }
  if(anyBeanLeft == false){
          for (int i = 0; i < NUM_LEDS; i++){
        leds[i] = CRGB(64,0,0);
      }
  }
  return anyBeanLeft;
}
  
int checkSuper(int idx){

  if (field[idx] == super) {
    return 1;
  } else {
    return 0;
  }
  
}

void runLights(CRGB *leds){
  int counter = 0;
  int button = 1;
  double power;
  int iPower;
  delay(1000);
  while (button){
    for(int i =0; i < NUM_LEDS; i++){

      power = 32.0*cos(0.1*(float)i + 0.1*(float)counter);
            Serial.println(power);
      iPower = abs((int)power);
      leds[i] = CRGB(iPower,iPower,iPower);
          int btnState = digitalRead(SW);
          if (btnState == LOW) {
            button = 0;
          }
    }
          counter = (counter + 1)%(NUM_LEDS*1000);
    FastLED.show();
}

}

void setup() {
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  
  // Set encoder pins as inputs
  pinMode(CLK,INPUT);
  pinMode(DT,INPUT);
  pinMode(SW, INPUT_PULLUP);

  // Setup Serial Monitor
  Serial.begin(9600);

  // Read the initial state of CLK
  lastStateCLK = digitalRead(CLK);


}

void loop() {
  struct bGhost inky;  
  inky.idx = 15;
  inky.lastIdx = 16;
  inky.history = bean;
  struct rGhost blinky;
  blinky.idx = 25;
  blinky.lastIdx = 26;
  blinky.history = bean;
    
  initField(leds,&inky,&blinky);
  
  delay(1000);
  while (stillGoing){
    // Read the current state of CLK
    currentStateCLK = digitalRead(CLK);
  
    // If last and current state of CLK are different, then pulse occurred
    // React to only 1 state change to avoid double count
    if (currentStateCLK != lastStateCLK  && currentStateCLK == 1){
  
      // If the DT state is different than the CLK state then
      // the encoder is rotating CCW so decrement
      if (digitalRead(DT) != currentStateCLK) {
        counter --;
        currentDir ="CCW";
      } else {
        // Encoder is rotating CW so increment
        counter ++;
        currentDir ="CW";
      }
 
    }
  
    // Remember last CLK state
    lastStateCLK = currentStateCLK;
  
    // Read the button state
    int btnState = digitalRead(SW);

    //If we detect LOW signal, button is pressed
    if (btnState == LOW && (millis() - lastButtonPress > 5000)) {
      //if 50ms have passed since last LOW pulse, it means that the
      //button has been pressed, released and pressed again
      runLights(leds);
      // Remember last button press event
      lastButtonPress = millis();
        initField(leds,&inky,&blinky);
    }
  
    lastPacIdx = pacIdx;
    if (counter == -1){
      counter = NUM_LEDS -1;
    }
    if (counter == NUM_LEDS){
      counter = 0;
    }
    pacIdx = counter ;
//    Serial.println(counter);
    if (checkSuper(pacIdx))
    {
      superCounter = superTime;
      rGhostColor = rGhostSuper;
      bGhostColor = bGhostSuper;
    }
    updatePacman(leds,pacIdx,lastPacIdx);

    if (superCounter > 0 ){
      superCounter--;
//      Serial.println(superCounter);
    }
    if (rTimer > 0){
      rTimer--;
    }
    if (bTimer > 0){
      bTimer--;
    }
    if (superCounter == 1){
      rGhostColor = rGhostNormal;
      bGhostColor = bGhostNormal;

    }
    deathReturn = checkDeath(leds,superCounter,&inky,&blinky); 
    if (ghostTimer == gTick) {
      if(rTimer == 0){
        updateRGhost(leds,&blinky,rGhostColor);
      }
      if(bTimer == 0) {
        updateBGhost(leds, &inky,bGhostColor);
      }
      ghostTimer = 0;
        //0 lose , 1 nothing, 2 red , 3 blue
//      Serial.println(deathReturn);
      if ( deathReturn == 0){
        stillGoing = false;
        break;
      }
      if ( deathReturn == 2){
        rTimer = rTimerFreeze;
//        rGhostColor = rGhostSuper;
      }
      if (deathReturn == 3) {
        bTimer = bTimerFreeze;
//        bGhostColor = bGhostSuper;
      }
      
      stillGoing = checkWin(leds);
      
      for(int i = 0; i < NUM_LEDS;i++){
 //       Serial.print(field[i]);
      }
//      Serial.println(" ");
    }
    ghostTimer++;
    // Put in a slight delay to help debounce the reading
    delay(1);
  }
  delay(10000);
}
