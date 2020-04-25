#include <FastLED.h>
#define LED_PIN     7
#define NUM_LEDS    300
CRGB leds[NUM_LEDS];
int tempo = 500;
CRGBPalette16 currentPalette;
TBlendType    currentBlending;
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
#define UPDATES_PER_SECOND 100
#define BRIGHTNESS  64

extern CRGBPalette16 myRedWhiteBluePalette;
extern const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM;

typedef struct {
    int coord;
    int tab;
} note;    //  creates a struct type dataNode

const int songLength = 654;
//note mySong[songLength] =  {{0, 3},{0, 5}, {1,2},{1,3},{1,5},{2,2},{2,4},{2,5}};
note mySong[songLength] = {{0 , 3},{1 ,5 },{3 ,4 },{2 ,7 },{3 ,4 },{1 ,5 },{3 ,4 },{1 ,5 },{0 ,3 },{1 ,5 },{3 ,4 },{2 ,7 },{3 ,4 },{1 ,5 },{3 ,4 },{1 ,5 },{0 ,3 },{2 ,2 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,2 },{3 ,5 },{2 ,2 },{0 ,3 },{2 ,2 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,2 },{3 ,5 },{2 ,2 },
                           {0 ,3 },{2 ,4 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,4 },{3 ,5 },{2 ,4 },{0 ,3 },{2 ,4 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,4 },{3 ,5 },{2 ,4 },{0 ,3 },{2 ,5 },{3 ,4 },{2 ,7 },{3 ,4 },{2 ,5 },{3 ,4 },{2 ,5 },{0 ,3 },{2 ,5 },{3 ,4 },{2 ,7 },{3 ,4 },{2 ,5 },{3 ,4 },{2 ,4 },
                           {0 ,3 },{2 ,2 },{3 ,4 },{3 ,2 },{3 ,4 },{2 ,5 },{2 ,4 },{2 ,5 },{2 ,2 },{2 ,5 },{2 ,4 },{2 ,5 },{1 ,2 },{1 ,5 },{1 ,4 },{1 ,2 },{1 ,4 },{2 ,5 },{3 ,2 },{2 ,5 },{3 ,2 },{2 ,5 },{3 ,2 },{2 ,5 },{1 ,4 },{2 ,5 },{3 ,2 },{2 ,5 },{3 ,2 },{2 ,5 },{3 ,2 },{2 ,5 },
                           {2 ,4 },{2 ,7 },{3 ,7 },{3 ,6 },{3 ,7 },{2 ,7 },{2 ,5 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,5 },{2 ,7 },{1 ,5 },{2 ,4 },{1 ,7 },{1 ,5 },{0 ,0 },{1 ,2 },{2 ,5 },{2 ,4 },{2 ,5 },{1 ,2 },{2 ,5 },{1 ,2 },{0 ,0 },{2 ,2 },{2 ,5 },{2 ,4 },{2 ,5 },{2 ,2 },{2 ,5 },{2 ,2 },
                           {0 ,0 },{1 ,4 },{1 ,5 },{1 ,7 },{1 ,5 },{1 ,4 },{0 ,7 },{0 ,5 },{2 ,5 },{2 ,4 },{1 ,7 },{3 ,7 },{3 ,7 },{3 ,4 },{2 ,7 },{2 ,5 },{2 ,4 },{1 ,7 },{1 ,5 },{3 ,7 },{2 ,7 },{3 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{1 ,7 },{2 ,4 },{2 ,7 },{2 ,5 },{2 ,4 },{1 ,7 },{1 ,5 },
                           {2 ,6 },{1 ,5 },{1 ,8 },{1 ,7 },{1 ,8 },{1 ,5 },{2 ,6 },{1 ,5 },{3 ,4 },{1 ,5 },{1 ,8 },{1 ,7 },{1 ,8 },{1 ,5 },{2 ,6 },{1 ,5 },{1 ,3 },{2 ,2 },{3 ,2 },{3 ,4 },{3 ,5 },{3 ,2 },{2 ,2 },{1 ,5 },{1 ,3 },{2 ,2 },{3 ,2 },{3 ,4 },{3 ,5 },{3 ,2 },{2 ,4 },{2 ,2 },
                           {1 ,6 },{2 ,4 },{1 ,6 },{2 ,4 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,4 },{1 ,6 },{2 ,4 },{1 ,6 },{2 ,4 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,4 },{2 ,5 },{2 ,4 },{1 ,7 },{2 ,5 },{2 ,4 },{2 ,5 },{2 ,7 },{2 ,4 },{2 ,5 },{2 ,4 },{1 ,7 },{1 ,5 },{1 ,3 },{1 ,2 },{0 ,5 },{0 ,3 },
                           {0 ,2 },{1 ,3 },{1 ,5 },{1 ,3 },{1 ,5 },{1 ,3 },{1 ,5 },{1 ,3 },{0 ,2 },{1 ,3 },{1 ,5 },{1 ,3 },{1 ,5 },{1 ,3 },{1 ,5 },{1 ,3 },{0 ,3 },{1 ,2 },{2 ,3 },{2 ,2 },{2 ,3 },{1 ,2 },{2 ,3 },{1 ,2 },{0 ,3 },{1 ,2 },{2 ,3 },{2 ,2 },{2 ,3 },{1 ,2 },{2 ,3 },{1 ,2 },
                           {0 ,3 },{1 ,3 },{2 ,2 },{1 ,5 },{2 ,2 },{1 ,3 },{2 ,2 },{1 ,3 },{0 ,3 },{1 ,3 },{2 ,2 },{1 ,5 },{2 ,2 },{1 ,3 },{2 ,2 },{1 ,3 },{0 ,3 },{2 ,4 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,4 },{3 ,5 },{2 ,4 },{0 ,3 },{2 ,4 },{3 ,5 },{3 ,4 },{3 ,5 },{2 ,4 },{3 ,5 },{2 ,4 },
                           {0 ,3 },{1 ,5 },{3 ,4 },{3 ,2 },{3 ,4 },{2 ,5 },{2 ,4 },{2 ,2 },{1 ,5 },{1 ,3 },{1 ,2 },{0 ,5 },{0 ,3 },{0 ,2 },{1 ,0 },{1 ,5 },{1 ,4 },{0 ,5 },{1 ,7 },{2 ,4 },{2 ,5 },{1 ,7 },{2 ,4 },{2 ,5 },{1 ,4 },{0 ,5 },{1 ,7 },{2 ,4 },{2 ,5 },{1 ,7 },{2 ,4 },{2 ,5 },
                           {1 ,3 },{0 ,5 },{1 ,5 },{2 ,2 },{2 ,4 },{1 ,5 },{2 ,2 },{2 ,4 },{1 ,3 },{0 ,5 },{1 ,5 },{2 ,2 },{2 ,4 },{1 ,5 },{2 ,2 },{2 ,4 },{1 ,3 },{0 ,5 },{1 ,5 },{2 ,4 },{2 ,7 },{3 ,6 },{3 ,7 },{0 ,5 },{1 ,2 },{1 ,3 },{1 ,5 },{2 ,2 },{2 ,4 },{2 ,5 },    //short line           
                           {3 ,2 },{2 ,4 },{1 ,5 },{2 ,2 },{2 ,4 },{2 ,5 },{3 ,2 },{3 ,4 },{3 ,5 },{3 ,2 },{2 ,4 },{2 ,5 },{2 ,7 },{3 ,4 },{3 ,5 },{3 ,7 },{3 ,8 },{3 ,7 },{3 ,6 },{3 ,7 },{3 ,7 },{3 ,5 },{3 ,4 },{3 ,5 },{3 ,5 },{2 ,7 },{2 ,4 },{1 ,7 },{1 ,5 },{1 ,0 },{1 ,2 },{1 ,3 },  
                           {1 ,5 },{0 ,5 },{1 ,5 },{2 ,4 },{3 ,2 },{3 ,4 },{3 ,5 },{3 ,2 },{3 ,4 },{2 ,5 },{1 ,5 },{1 ,3 },{1 ,2 },{0 ,3 },{0 ,5 },{1 ,2 },{1 ,5 },{0 ,3 },{1 ,2 },{1 ,5 },{2 ,5 },{3 ,2 },{3 ,4 },{2 ,5 },{3 ,6 },{3 ,4 },{2 ,7 },{2 ,8 },{2 ,8 },{2 ,7 },{2 ,6 },{2 ,7 },  
                           {2 ,7 },{2 ,5 },{2 ,4 },{2 ,5 },{2 ,5 },{1 ,7 },{1 ,4 },{0 ,7 },{0 ,5 },{1 ,4 },{1 ,7 },{2 ,5 },{2 ,7 },{3 ,6 },{3 ,7 },{3 ,6 },{3 ,7 },{2 ,7 },{2 ,4 },{1 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{2 ,4 },{0 ,5 },{1 ,5 },{1 ,4 },{0 ,7 },{0 ,5 },{0 ,3 },{0 ,2 },{0 ,0 }, 
                           {1 ,5 },{3 ,5 },{3 ,4 },{3 ,2 },{2 ,5 },{2 ,4 },{2 ,2 },{1 ,5 },{3 ,5 },{3 ,4 },{3 ,2 },{2 ,5 },{2 ,4 },{2 ,2 },{1 ,5 },{1 ,3 },{3 ,4 },{3 ,2 },{2 ,5 },{2 ,4 },{2 ,2 },{1 ,5 },{1 ,3 },{1 ,2 },{3 ,2 },{2 ,5 },{2 ,4 },{2 ,2 },{1 ,5 },{1 ,3 },{1 ,2 }, //short line 
                           {0 ,5 },{2 ,5 },{2 ,4 },{1 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{2 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },{2 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{2 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },          
                           {2 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,5 },{2 ,7 },{2 ,7 },{2 ,7 },{3 ,4 },{2 ,7 },{1 ,5 },{2 ,7 },{2 ,7 },{2 ,7 },{3 ,4 },{2 ,7 },{3 ,5 },{2 ,7 },{1 ,5 },{2 ,7 },{3 ,4 },{2 ,7 },{3 ,5 },{2 ,7 },{3 ,7 },{2 ,7 },{3 ,4 },{2 ,7 },   
                           {3 ,5 },{2 ,7 },{3 ,4 },{2 ,7 },{3 ,5 },{2 ,7 },{2 ,7 },{2 ,7 },{3 ,4 },{2 ,7 },{2 ,7 },{2 ,7 },{3 ,4 },{2 ,7 },{2 ,5 },{2 ,7 },{2 ,7 },{2 ,7 },{2 ,5 },{2 ,7 },{2 ,7 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,5 },{2 ,7 },{2 ,4 },{2 ,7 },{2 ,5 },{2 ,7 },{1 ,7 },{2 ,7 },   
                           {2 ,4 },{2 ,7 },{1 ,5 },{1 ,7 },{2 ,3 },{1 ,5 },{2 ,4 },{1 ,5 },{2 ,5 },{1 ,5 },{2 ,6 },{1 ,5 },{2 ,7 },{1 ,5 },{2 ,8 },{1 ,5 },{3 ,4 },{2 ,0 },{3 ,5 },{2 ,0 },{3 ,6 },{2 ,0 },{3 ,7 },{2 ,0 },{3 ,8 },{2 ,0 },{3 ,9 },{2 ,0 },{3 ,10 },{2 ,0 },{3 ,11 },{2 ,0 },
                           {3 ,12 },{2 ,9 },{0 ,10 },{2 ,9 },{3 ,12 },{2 ,9 },{3 ,12 },{2 ,9 },{3 ,12 },{2 ,9 },{0 ,10 },{2 ,9 },{3 ,12 },{2 ,9 },{3 ,12 },{2 ,9 }, //short line
                           {3 ,12 },{1 ,12 },{0 ,10 },{1 ,12 },{3 ,12 },{1 ,12 },{3 ,12 },{1 ,12 },{3 ,12 },{1 ,12 },{0 ,10 },{1 ,12 },{3 ,12 },{1 ,12 },{3 ,12 },{1 ,12 }, //short line
                           {3 ,11 },{2 ,10 },{0 ,10 },{2 ,10 },{3 ,11 },{2 ,10 },{3 ,11 },{2 ,10 },{3 ,11 },{2 ,10 },{0 ,10 },{2 ,10 },{3 ,11 },{2 ,10 },{3 ,11 },{2 ,10 },{2 ,9 }   //short line
};



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

void playNote(int index, int coord,int strength) {
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





void clearNotes(int index){
    leds[index] = CRGB {0,0,0} ;  //black
    FastLED.show();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
//setup show
      delay( 3000 ); // power-up safety delay
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
    FastLED.setBrightness(  BRIGHTNESS );
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;
}

void loop() {
 // put your main code here, to run repeatedly:
  for (int i = 0; i < songLength; i++){
    note current = mySong[i];
    int thisCoord = current.coord;
    int thisTab = current.tab;
    int index = sumUp(thisCoord,thisTab);
    playNote(index,thisCoord,128);
    note next = mySong[(i+ 1)%songLength];
    int nextCoord = next.coord;
    int nextTab = next.tab;
    int nextIndex = sumUp(nextCoord,nextTab);
    playNote(nextIndex,nextCoord,4);
    
    delay(tempo);
    clearNotes(index);
    clearNotes(nextIndex);
  }
    for (int i = 0; i < 10000; i++){
    ChangePalettePeriodically();
    
    static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);
    }
}


void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}


// There are several different palettes of colors demonstrated here.
//
// FastLED provides several 'preset' palettes: RainbowColors_p, RainbowStripeColors_p,
// OceanColors_p, CloudColors_p, LavaColors_p, ForestColors_p, and PartyColors_p.
//
// Additionally, you can manually define your own color palettes, or you can write
// code that creates color palettes on the fly.  All are shown here.

void ChangePalettePeriodically()
{
    uint8_t secondHand = (millis() / 1000) % 60;
    static uint8_t lastSecond = 99;
    
    if( lastSecond != secondHand) {
        lastSecond = secondHand;
        if( secondHand ==  0)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND; }
        if( secondHand == 10)  { currentPalette = RainbowStripeColors_p;   currentBlending = NOBLEND;  }
        if( secondHand == 15)  { currentPalette = RainbowStripeColors_p;   currentBlending = LINEARBLEND; }
        if( secondHand == 20)  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND; }
        if( secondHand == 25)  { SetupTotallyRandomPalette();              currentBlending = LINEARBLEND; }
        if( secondHand == 30)  { SetupBlackAndWhiteStripedPalette();       currentBlending = NOBLEND; }
        if( secondHand == 35)  { SetupBlackAndWhiteStripedPalette();       currentBlending = LINEARBLEND; }
        if( secondHand == 40)  { currentPalette = CloudColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 45)  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND; }
        if( secondHand == 50)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = NOBLEND;  }
        if( secondHand == 55)  { currentPalette = myRedWhiteBluePalette_p; currentBlending = LINEARBLEND; }
    }
}

// This function fills the palette with totally random colors.
void SetupTotallyRandomPalette()
{
    for( int i = 0; i < 16; i++) {
        currentPalette[i] = CHSV( random8(), 255, random8());
    }
}

// This function sets up a palette of black and white stripes,
// using code.  Since the palette is effectively an array of
// sixteen CRGB colors, the various fill_* functions can be used
// to set them up.
void SetupBlackAndWhiteStripedPalette()
{
    // 'black out' all 16 palette entries...
    fill_solid( currentPalette, 16, CRGB::Black);
    // and set every fourth one to white.
    currentPalette[0] = CRGB::White;
    currentPalette[4] = CRGB::White;
    currentPalette[8] = CRGB::White;
    currentPalette[12] = CRGB::White;


    
}

// This function sets up a palette of purple and green stripes.
void SetupPurpleAndGreenPalette()
{
    CRGB purple = CHSV( HUE_PURPLE, 255, 255);
    CRGB green  = CHSV( HUE_GREEN, 255, 255);
    CRGB black  = CRGB::Black;
    
    currentPalette = CRGBPalette16(
                                   green,  green,  black,  black,
                                   purple, purple, black,  black,
                                   green,  green,  black,  black,
                                   purple, purple, black,  black );
}


// This example shows how to set up a static color palette
// which is stored in PROGMEM (flash), which is almost always more
// plentiful than RAM.  A static PROGMEM palette like this
// takes up 64 bytes of flash.
const TProgmemPalette16 myRedWhiteBluePalette_p PROGMEM =
{
    CRGB::Red,
    CRGB::Gray, // 'white' is too bright compared to red and blue
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Black,
    
    CRGB::Red,
    CRGB::Red,
    CRGB::Gray,
    CRGB::Gray,
    CRGB::Blue,
    CRGB::Blue,
    CRGB::Black,
    CRGB::Black
};
