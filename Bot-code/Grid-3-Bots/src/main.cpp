#include <Arduino.h>
#include <WiFiManager.h>
#include <ArduinoMqttClient.h>
#include <Servo.h>
#include "config.h"
#include "PINS.h"

/*=============MACROS==============*/
#define BAUD 115200
#define SPEED_MAX 1000
#define SPEED_MIN 0
#define PWM_MAX 1023
#define PWM_MIN 0
#define ROTATION_SPEED 100
#define SERVO_HIGHEST_DEGREE 90
#define BOT_CONTROL_TOPIC "ToBot"
#define BOT_PUBLISH_TOPIC "FromBot"
#define set_A_PWM(pwm) \
  analogWrite(A_PWM, pwm);
#define set_B_PWM(pwm) \
  analogWrite(B_PWM, pwm);

/*=======Globals=======*/
typedef enum commands
{
  Stop,
  Forward,
  Reverse,
  Left_Turn,
  Right_Turn,
  Unload,
  Rotate_180
}command;

/** Enum for valid directions
 * NN = No direction/Stop
 * FF = Both motors forward
 * RR = Both motors reverse
 * FR = Left motor forward, right motor reverse (turn right)
 * RF = Left motor reverse, right motor forward (turn left)
*/
typedef enum directions{NN, FF, RR, RF, FR} direction;
const unsigned long us_per_degree = 1000;  //when motors rotate with 100cm/s
const unsigned long servo_unload_timing_ms = 500;
Servo unloader; //unloader servo object
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

/*==============Function Prototypes====================*/
void io_init(void);
void mqtt_init(void);
void wifi_init(void);

bool stop(void);
bool forward(int magnitude);
bool reverse(int magnitude);
bool turn(command direction, int degree);
void unload(void);
bool rotate(void);

bool publishChipId(void);
bool publishError(void);
bool subscribe_to_pc(void);

bool setDirection(direction dir);
direction interpret_direction(command);
void setMotorsDir(bool In1, bool In2, bool In3, bool In4);
uint16_t calculate_pwm_from_speed(unsigned int speed);
void configModeCallback(WiFiManager *wifi);
void commandHandler(int messageSize);
void magnitudeChangeHandler(int messageSize);

void setup() {
  Serial.begin(BAUD);
  Serial.setDebugOutput(true);
  io_init();
  stop();
  wifi_init();
  mqtt_init();
  Serial.printf("%s\n", subscribe_to_pc()?"subscribed":"not subscribed");
  mqttClient.onMessage(commandHandler);
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
bool turn(command cmd, int degree)
{
  bool flag = true;
  flag &= stop();
  set_A_PWM(calculate_pwm_from_speed(ROTATION_SPEED));
  set_B_PWM(calculate_pwm_from_speed(ROTATION_SPEED));
  flag &= setDirection(interpret_direction(cmd));
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
 * //TODO - debug
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
  uint32_t id = ESP.getChipId();
  String ap_name = "MQTTBot_" + id;
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
  Serial.println(id);
}

/**
 * publishes the chipId on first connection
 * and retains the message
 * //TODO
 */
bool publishChipId(void)
{
  String topic = BOT_PUBLISH_TOPIC;
  topic += "/Botlist";
  return false;
}

/**
 * Function to subscribe to
 * 1. Command
 * 2. Magnitude
 * topics
 * //TODO
*/
bool subscribe_to_pc(void)
{
  String topic = BOT_CONTROL_TOPIC ;
  topic += '/';
  topic += ESP.getChipId();
  topic += "/+";
  Serial.print("Subscribing to topics: ");
  Serial.println(topic);
  int ec = mqttClient.subscribe(topic);
  Serial.println(ec);
  return (ec);
}

void commandHandler(int messageSize)
{
  //TODO
  String msg = mqttClient.messageTopic();
  Serial.println(msg);

}
void magnitudeChangeHandler(int messageSize)
{
  //TODO - complete the message handler for ./Commands and ./Magnitude
  String msgTopic = mqttClient.messageTopic();
  int size = mqttClient.parseMessage();

}

/*=============Lower level functions============*/

/**
 * This functions takes in command and interprets the direction
 * \param command: typedef enum commands
 * \return direction (typedef enum directions)
 */
direction interpret_direction(command c)
{
  if(c == Left_Turn)
    return RF;
  if(c == Right_Turn)
    return FR;
  return NN;
}

/**
 * Set Direction from enum directions
 * \param direction: 0 to 4,
 * NN = No direction/Stop,
 * FF = Both motors forward,
 * RR = Both motors reverse,
 * FR = Left motor forward, right motor reverse (turn right),
 * RF = Left motor reverse, right motor forward (turn left)
 * \return true on success
*/
bool setDirection(direction dir)
{
  switch (dir)
  {
  case NN:
    setMotorsDir(LOW, LOW,   LOW, LOW);
  case FF:
    setMotorsDir(HIGH, LOW, HIGH, LOW);
    break;
  case RR:
    setMotorsDir(LOW, HIGH, LOW, HIGH);
    break;
  case RF:
    setMotorsDir(LOW, HIGH, HIGH, LOW);
    break;
  case FR:
    setMotorsDir(HIGH, LOW, LOW, HIGH);
    break;
  default:
    return false; //returns false on wrong input
  }
  return true;  //returns true on success
}

/**
 * set motors' direction directly/logically
 * \param In1 Boolean Logic for In1
 * \param In2 Boolean Logic for In2
 * \param In3 Boolean Logic for In3
 * \param In4 Boolean Logic for In4
*/
void setMotorsDir(bool In1, bool In2, bool In3, bool In4)
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

/**
 * used only by WiFiManager
 */
void configModeCallback(WiFiManager *wifi)
{
  Serial.println("Entered config mode: ");
  Serial.println(WiFi.softAPIP());
  Serial.println(wifi->getConfigPortalSSID());
}