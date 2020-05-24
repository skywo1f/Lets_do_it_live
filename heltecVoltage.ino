#include "heltec.h"

void setup() {
  Serial.begin(115200);
  Heltec.begin(true /*DisplayEnable Enable*/, false /*LoRa Disable*/, true /*Serial Enable*/);
  Heltec.display->setFont(ArialMT_Plain_10);
//  Heltec.display->clear();
  adcAttachPin(13);

}

void loop() {
   int analog = analogRead(13);
   Serial.print(analog);
   Serial.print("  ");
   Heltec.display->clear();
   Heltec.display->drawString(0, 0, String(100.0*float(analog-4096.0*0.7)/(4096.0*0.3)));
   Heltec.display->display();
   delay(500);
}
