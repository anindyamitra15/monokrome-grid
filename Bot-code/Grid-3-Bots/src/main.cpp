#include <Arduino.h>
#include<WiFiManager.h>
#include <ArduinoMqttClient.h>
#include "config.h"
#include "PINS.h"

/*====Function Prototypes======*/
bool stop(void);
bool forward(int magnitude);

void setup() {
  // put your setup code here, to run once:
}

void loop() {
  // put your main code here, to run repeatedly:
}

/*====Function Definitions======*/
//The bot (all the motors) stop when this function is called
bool stop(void)
{
  //logic to set motor outputs to 0
  return true;
}
//Motor moves forward with magnitude cm/s speed
bool forward(int magnitude)
{
  //logic to set the PWM from the magnitude and to move the bot forward
  return true;
}