#include <Arduino.h>
#include <ArduinoMqttClient.h>
#include "config.h"
#include "PINS.h"

/*====Function Prototypes======*/
bool stop(int magnitude);
bool forward(int magnitude);

void setup() {
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
}

/*====Function Definitions======*/
//The bot (all the motors) stop when this function is called
bool stop(int magnitude)
{
  //logic to set motor outputs to 0
  return true;
}
//Motor moves forward with magnitude cm/s speed
bool forward(int magnitude)
{
  
  return true;
}