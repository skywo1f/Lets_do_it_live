#include <Adafruit_LSM303DLH_Mag.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

float V1[3] = {0.5,-0.5,-0.5};
float V2[3] = {-0.5,0.5,-0.5};
float V3[3] = {-0.5,-0.5,0.5};
float V4[3] = {0.5,0.5,0.5};
float magV[3];


int V1_pin = 13 ;
int V2_pin = 12 ;
int V3_pin = 11 ;
int V4_pin = 10 ;


/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303DLH_Mag_Unified mag = Adafruit_LSM303DLH_Mag_Unified(12345);
 
void displaySensorDetails(void) {
  sensor_t sensor;
  mag.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print("Sensor:       ");
  Serial.println(sensor.name);
  Serial.print("Driver Ver:   ");
  Serial.println(sensor.version);
  Serial.print("Unique ID:    ");
  Serial.println(sensor.sensor_id);
  Serial.print("Max Value:    ");
  Serial.print(sensor.max_value);
  Serial.println(" uT");
  Serial.print("Min Value:    ");
  Serial.print(sensor.min_value);
  Serial.println(" uT");
  Serial.print("Resolution:   ");
  Serial.print(sensor.resolution);
  Serial.println(" uT");
  Serial.println("------------------------------------");
  Serial.println("");
  pinMode(V1_pin, OUTPUT);
  pinMode(V2_pin, OUTPUT);
  pinMode(V3_pin, OUTPUT);
  pinMode(V4_pin, OUTPUT);

  delay(500);
}

float dotProduct(float *first,float *second){
  float dot = first[0]*second[0] + first[1]*second[1] + first[2]*second[2];
  return dot;
}
 
void setup(void) {
#ifndef ESP8266
  while (!Serial)
    ; // will pause Zero, Leonardo, etc until serial console opens
#endif
  Serial.begin(115200);
  Serial.println("Magnetometer Test");
  Serial.println("");
 
  /* Enable auto-gain */
  mag.enableAutoRange(true);
 
  /* Initialise the sensor */
  if (!mag.begin()) {
    /* There was a problem detecting the LSM303 ... check your connections */
    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while (1)
      ;
  }
 
  /* Display some basic information on this sensor */
  displaySensorDetails();
}
 
void loop(void) {
  /* Get a new sensor event */
  sensors_event_t event;
  mag.getEvent(&event);
 
  /* Display the results (magnetic vector values are in micro-Tesla (uT)) */
  magV[0] = event.magnetic.x;
  magV[1] = event.magnetic.y;
  magV[2] = event.magnetic.z;
  float dot1 = dotProduct(magV,V1);
  if (dot1 < 0) {
    dot1 = 0;
  }
  float dot2 = dotProduct(magV,V2);
    if (dot2 < 0) {
    dot2 = 0;
  }
  float dot3 = dotProduct(magV,V3);
    if (dot3 < 0) {
    dot3 = 0;
  }
  float dot4 = dotProduct(magV,V4);
    if (dot4 < 0) {
    dot4 = 0;
  }

float  motor1 = map(dot1, 0, 80, 50, 255);
float  motor2 = map(dot2, 0, 80, 50, 255);
float  motor3 = map(dot3, 0, 80, 50, 255);
 float motor4 = map(dot4, 0, 80, 50, 255);

  analogWrite(V1_pin, motor1);
  analogWrite(V2_pin, motor2);
  analogWrite(V3_pin, motor3);
  analogWrite(V4_pin, motor4);    
  
  Serial.print("V1 ");
  Serial.print(dot1);
  Serial.print("  ");
  Serial.print("V2 ");
  Serial.print(dot2);
  Serial.print("  ");
  Serial.print("V3 ");
  Serial.print(dot3);
  Serial.print(" V4 ");
  Serial.println(dot4);
 
  /* Delay before the next sample */
  delay(5);
}
