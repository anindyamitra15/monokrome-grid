#include <Arduino.h>
#include <WiFiManager.h>
#include <ArduinoMqttClient.h>
#include <Servo.h>
#include "config.h"
#include "PINS.h"

/*=============MACROS==============*/
#define SPEED_MAX 1000
#define SPEED_MIN 0
#define PWM_MAX 1023
#define PWM_MIN 0
#define ROTATION_SPEED 100
#define SERVO_HIGHEST_DEGREE 90
#define BOT_CONTROL_TOPIC "Bot"
#define set_A_PWM(pwm) \
  analogWrite(A_PWM, pwm);
#define set_B_PWM(pwm) \
  analogWrite(B_PWM, pwm);
/*==============Function Prototypes====================*/
void io_init(void);
void mqtt_init(void);
void wifi_init(void);

bool stop(void);
bool forward(int magnitude);
bool reverse(int magnitude);
bool turn (int direction, int degree);
void unload(void);
bool rotate(void);

bool subscribe_to_pc(void);


bool setDirection(uint8_t dir);
void setMotorDir(bool In1, bool In2, bool In3, bool In4);
uint16_t calculate_pwm_from_speed(int speed);
void configModeCallback(WiFiManager *wifi);
void messageHandler(int messageSize);

/*=======Globals=======*/
enum commands
{
  Stop,
  Forward,
  Reverse,
  Left_Turn,
  Right_Turn,
  Unload,
  Rotate_180
};
/** Enum for valid directions
 * NN = No direction/Stop
 * FF = Both motors forward
 * RR = Both motors reverse
 * FR = Left motor forward, right motor reverse (turn right)
 * RF = Left motor reverse, right motor forward (turn left)
*/
enum directions{NN, FF, RR, RF, FR};
const unsigned long us_per_degree = 1000;  //when motors rotate with 100cm/s
const unsigned long servo_unload_timing_ms = 500;
Servo unloader; //unloader servo object
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  io_init();
  stop();
  mqtt_init();
  wifi_init();
  subscribe_to_pc();
  mqttClient.onMessage(messageHandler);
}

void loop() {
  mqttClient.poll();
}

/*====Function Definitions======*/

/**
 * The bot (all the motors) stop when this function is called
 */
bool stop(void)
{
  //logic to set all motor outputs to 0
  return setDirection(NN);
}

/**
 * Motor moves forward with magnitude cm/s speed
 * \param magnitude (Speed)
 * \return true on success
*/
bool forward(int magnitude)
{
  //logic to set the PWM from the magnitude and to move the bot forward
  bool flag = true;
  flag &= stop();
  set_A_PWM(calculate_pwm_from_speed(magnitude));
  set_B_PWM(calculate_pwm_from_speed(magnitude));
  flag &= setDirection(FF);
  return flag;
}

/**
 * Motor moves backwards with magnitude cm/s speed
 * \param magnitude (Speed)
 * \return true on success
*/
bool reverse(int magnitude)
{
  bool flag = true;
  flag &= stop();
  set_A_PWM(calculate_pwm_from_speed(magnitude));
  set_B_PWM(calculate_pwm_from_speed(magnitude));
  flag &= setDirection(RR);
  return flag;
}

/**
 * Motor turns in a direction by certain degree
 * \param direction (left/right) from command
 * \param degree (degree of rotation)
 * \return true on success
*/
bool turn(int direction, int degree)
{
  bool flag = true;
  flag &= stop();
  set_A_PWM(calculate_pwm_from_speed(ROTATION_SPEED));
  set_B_PWM(calculate_pwm_from_speed(ROTATION_SPEED));
  flag &= setDirection(direction);
  delayMicroseconds(degree * us_per_degree);
  flag &= stop();
  return flag;
}

/**
 * Unloads the load
 * and resets servo to position
 */
void unload(void)
{
  stop();
  unloader.write(0);
  unloader.write(SERVO_HIGHEST_DEGREE);
  delay(servo_unload_timing_ms);
  unloader.write(0);
}
/**
 * Rotates the bot by 180 degrees
 * \return true if it succeeds
*/
bool rotate()
{
  return turn(Left_Turn, 180);
}

/**
 * Input Output Initialiser function
 * Set all the input-outputs
 */
void io_init(void)
{
  pinMode(LED, OUTPUT);
  pinMode(A_PLUS, OUTPUT);
  pinMode(A_MINUS, OUTPUT);
  pinMode(B_PLUS, OUTPUT);
  pinMode(B_MINUS, OUTPUT);
  pinMode(A_PWM, OUTPUT);
  pinMode(B_PWM, OUTPUT);
  unloader.attach(SERVO_PIN);
}
/**
 * MQTT initialising function
*/
void mqtt_init()
{
  //attempt to connect to mqtt broker
  if (!mqttClient.connect(broker, mqtt_port))
  {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1);//wait for watchdog to bite
  }
  Serial.println("You're connected to the MQTT broker!");
}

/**
 * Run everything needed to initialise WiFi
 * Uses WiFiManager to connect to AP
 * if AP is not found, ESP will become an AP
 * where you can put wifi credentials on
 * 192.168.1.1
*/
void wifi_init()
{
  WiFiManager wifi;
  wifi.setDebugOutput(false);
  wifi.setTimeout(300);
  wifi.setAPCallback(configModeCallback);
  String ap_name = "MQTTBot_" + ESP.getChipId();
  if (!wifi.autoConnect(ap_name.c_str(), "12345678"))
  {
    Serial.println("Couldn't Connect to remote AP");
    ESP.restart();
    digitalWrite(LED, LOW);
    delay(2500);
    digitalWrite(LED, HIGH);
    delay(2500);
  } else
  { // blink thrice on connection
    for (int i = 0; i < 3; i++)
    {
      digitalWrite(LED, LOW);
      delay(200);
      digitalWrite(LED, HIGH);
      delay(200);
    }
  }
}
/**
 * Function to subscribe to
 * 1. Command
 * 2. Magnitude
 * topics
*/
bool subscribe_to_pc(void)
{
  String topic = BOT_CONTROL_TOPIC + ESP.getChipId();
  int ec = mqttClient.subscribe(topic + "Command");
  ec += mqttClient.subscribe(topic + "Magnitude");
  return (ec == 0);
}

void messageHandler(int messageSize)
{
  String msg = mqttClient.messageTopic();
}

/*=============Lower level functions============*/

/**
 * Set Direction from enum directions
 * \param dir (direction) 0 to 4,
 * NN = No direction/Stop,
 * FF = Both motors forward,
 * RR = Both motors reverse,
 * FR = Left motor forward, right motor reverse (turn right),
 * RF = Left motor reverse, right motor forward (turn left)
*/
bool setDirection(uint8_t dir)
{
  switch (dir)
  {
  case NN:
    setMotorDir(LOW, LOW,   LOW, LOW);
  case FF:
    setMotorDir(HIGH, LOW, HIGH, LOW);
    break;
  case RR:
    setMotorDir(LOW, HIGH, LOW, HIGH);
    break;
  case RF:
    setMotorDir(LOW, HIGH, HIGH, LOW);
    break;
  case FR:
    setMotorDir(HIGH, LOW, LOW, HIGH);
    break;
  default:
    return false; //returns false on wrong input
  }
  return true;  //returns true on success
}

/**
 * set motor directions directly
 * \param In1 Boolean Logic for In1
 * \param In2 Boolean Logic for In2
 * \param In3 Boolean Logic for In3
 * \param In4 Boolean Logic for In4
*/
void setMotorDir(bool In1, bool In2, bool In3, bool In4)
{
  digitalWrite(A_PLUS, In1);
  digitalWrite(A_MINUS,In2);
  digitalWrite(B_PLUS, In3);
  digitalWrite(B_MINUS,In4);
}

/**
 * Function to calculate PWM from Speed
 * \param speed as unsigned integer
 * \return PWM value, unsigned 16-bit integer
*/
uint16_t calculate_pwm_from_speed(unsigned int speed)
{
  return map(speed, SPEED_MIN, SPEED_MAX, PWM_MIN, PWM_MAX);
}

void configModeCallback(WiFiManager *wifi)
{
  Serial.println("Entered config mode: ");
  Serial.println(WiFi.softAPIP());
  Serial.println(wifi->getConfigPortalSSID());
}