//Alternate implementation
//obsolete functions commented out, will be removed

#include <Arduino.h>
#include <WiFiManager.h>
#include <ArduinoMqttClient.h>
#include <Servo.h>
#include "config.h"
#include "PINS.h"

/*=============MACROS==============*/

#define BAUD 76800

#define PWM_MAX 1023

#define UNLOAD_DEGREE 90

/*====Topics Macros====*/
#define TOPIC_SUB "ToBot"
#define TOPIC_PUB "FromBot"
/*====Topics Macros====*/

#define SLASH String('/')
//macro functions
#define set_L_PWM(pwm)\
  analogWrite(L_PWM, pwm);
#define set_R_PWM(pwm)\
  analogWrite(R_PWM, pwm);

/*=======Globals=======*/

/**
 * enum for valid motor selection
 * Unloader = 0
 * Left = 1
 * Right = 2
 * Both = 3
 */
typedef enum motor {Unloader, Left, Right, Both} motor;

/** Enum for valid directions
 * Stop = 0
 * Forward = 1
 * Reverse = 2
*/
typedef enum direction{Stop, Forward, Reverse} direction;

typedef struct motor_param
{
  direction dir;
  uint16_t pwm;
}motor_param;

typedef struct route
{
  String topic;
  String message;
} route;
typedef struct topic_subscribe
{
  String parent;
  String direction;
  String pwm;
} topic_subscribe;
typedef struct topic_publish
{
  String parent;
  String botlist;
  String error;
} topic_publish;


topic_subscribe sub;
topic_publish   pub;

motor_param left;
motor_param right;

const unsigned long servo_unload_tick = 500;
Servo unloader; //unloader servo object
WiFiClient wifiClient;
MqttClient mqttClient (wifiClient);

/*==============Function Prototypes====================*/

void io_init(void);
bool mqtt_init(void);
void wifi_init(void);
void topics_init(void);

void stop(void);  //improve definition
void unload(void); //improve definition

bool publishChipId(void);
bool publishError(String);  //Change definition
bool subscribe_to_pc(void);
bool publishUnloader (bool);

void controlMotor(motor, direction, uint16_t);
void setMotorsDir(bool In1, bool In2, bool In3, bool In4);

void configModeCallback(WiFiManager *wifi);
void mqttMessageHandler(int messageSize); //Change definition
direction parseDirection(String);
uint16_t parsePWM(String);
String getLastTopic(String);

/*=========Setup=========*/
void setup () {
  Serial.begin(BAUD);
  Serial.setDebugOutput(true);
  io_init();
  stop();
  wifi_init();
  
  bool flag;
  do
  {
    flag = true;
    flag &= mqtt_init();
    flag &= publishChipId();
    //flag &= publishError("Hi");
    flag &= subscribe_to_pc();
  }while(!flag && Serial.println("Something failed"));
  mqttClient.onMessage(mqttMessageHandler);
}
/*=========Setup=========*/

/*=========Loop=========*/
void loop () {
  mqttClient.poll();

  //on disconnection behavior
  static uint8_t fire = 0;
  if (wifiClient.status() == WL_CONNECTION_LOST)
  {
    fire++;
    if (fire > 3)
    {
      wifi_init();
      mqtt_init();
      fire = 0;
    }
  }
}
/*=========Loop=========*/

/*====Function Definitions======*/

/**
 * The bot (all the motors) stop when this function is called
 * TODO - improve definition
 */
void stop (void)
{
  //logic to set all motor outputs to 0
  setMotorsDir(LOW, LOW, LOW, LOW);//change
  set_L_PWM(0);
  set_R_PWM(0);
}

/**
 * Unloads the load
 * and resets servo to position
 */
void unload (void)
{
  stop();
  unloader.write(0);
  for(int i = 0; i <= UNLOAD_DEGREE; i++)
  {
    unloader.write(i);//slowly increases slope
    delayMicroseconds(servo_unload_tick);
  }
  unloader.write(0);
}

/**
 * Input Output Initialiser function
 */
void io_init (void)
{
  pinMode(LED,      OUTPUT);
  pinMode(L_PLUS,   OUTPUT);
  pinMode(L_MINUS,  OUTPUT);
  pinMode(R_PLUS,   OUTPUT);
  pinMode(R_MINUS,  OUTPUT);
  pinMode(L_PWM,    OUTPUT);
  pinMode(R_PWM,    OUTPUT);
  analogWriteFreq (PWM_FREQ);
  unloader.attach(SERVO_PIN);
}

/**
 * MQTT initialising function
 * //TODO - debug
*/
bool mqtt_init ()
{
  topics_init();
  //attempt to connect to mqtt broker
  if (!mqttClient.connect(broker, mqtt_port))
  {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    return false;
  }
  Serial.println("You're connected to the MQTT broker!");
  return true;
}

/**
 * Run everything needed to initialise WiFi
 * Uses WiFiManager to connect to AP
 * if AP is not found, ESP will become an AP
 * where you can put wifi credentials on
 * 192.168.4.1
*/
void wifi_init (void)
{
  WiFiManager wifi;
  wifi.setDebugOutput(false);
  wifi.setTimeout(300);
  wifi.setAPCallback(configModeCallback);
  uint32_t id = ESP.getChipId();
  Serial.print("\n\nChip ID: ");
  Serial.println(id);
  String ap_name = "MQTTBot_" + String(id);
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
 * prepares all the topic strings
 */
void topics_init(void)
{
  //Subscribe topics Struct initialise
  sub.parent = TOPIC_SUB + SLASH + String(ESP.getChipId());
  sub.direction = "Direction";
  sub.pwm = "PWM";

  //Publish topics Struct initialise
  pub.parent = TOPIC_PUB;
  pub.botlist = pub.parent + SLASH + "Botlist";
  pub.error = pub.parent + SLASH + "Error";
}

/**
 * publishes the chipId on first connection
 * and retains the message
 * \return true on success
 * //TODO - track changes
 */
bool publishChipId (void)
{
  bool flag = true;
  Serial.print("Publishing ChipId to: ");
  Serial.println(pub.botlist);
  flag &= mqttClient.beginMessage(pub.botlist);
  mqttClient.print(ESP.getChipId());
  flag &= mqttClient.endMessage();
  return flag;
}

/**
 * Function can be called to publish
 * any error to pub.error in String format
 * \param message the error message in string format
 * \return true on success
 */
bool publishError (String msg)

{
  bool flag = true;
  Serial.print("Publishing Error to: ");
  Serial.println(pub.error);
  flag &= mqttClient.beginMessage(pub.error);
  mqttClient.printf("{\"id\":\"%s\",\"msg\":\"%s\"}",
    String(ESP.getChipId()).c_str(), 
    msg.c_str());
  flag &= mqttClient.endMessage();
  return flag;
}

/**
 * Function to subscribe to
 * Control topics
*/
bool subscribe_to_pc (void)
{
  String topic = sub.parent + SLASH + '#';//multilevel wild card
  Serial.print("Subscribing to topics: ");
  Serial.println(topic);
  int ec = mqttClient.subscribe(topic);
  //Serial.println(ec);
  return (bool)(ec);
}

/**
 * Function only used by MQTT message Handler
 * \param state true/false
 * \return true on success
 */
bool publishUnloader(bool state)
{
  bool flag = true;
  String topic = sub.parent + SLASH + '0';
  Serial.println(topic);
  flag &= mqttClient.beginMessage(topic);
  mqttClient.print(state);
  flag &= mqttClient.endMessage();
  return flag;
}

/**
 * Handles incoming messages from TOPIC_SUB
 * it's a callback used by onMessage of mqttClient
 * binded in setup()
 * \param messageSize
 */
void mqttMessageHandler (int messageSize)
{
  String msgTopic = mqttClient.messageTopic();

  //subtracts the subscribe parent topic to reduce length
  msgTopic = msgTopic.substring(sub.parent.length(), msgTopic.length());

  Serial.printf("\n%s\n",msgTopic.c_str());

  String msg = mqttClient.readString();
  int topic =  ((int)msgTopic.charAt(1) - '0');
  //if topic is unloader
  if(topic == Unloader)
    if (msg.toInt() == 1 || msg.equals("true"))
    {
      unload();
      publishUnloader(false); //deactivate unloader
      Serial.println("unloaded");
    }
    else
      Serial.println("unloader deactivated");
  else
  {
    Serial.println("Motor Commands Incoming");
    bool isDirection = (getLastTopic(msgTopic).equals(sub.direction));
    Serial.print(isDirection ? "Direction = " : "PWM = ");
    Serial.println(isDirection ? parseDirection(msg) : parsePWM(msg));
    //selects the motor from topic
    switch (topic)
    {
    case Left:
      Serial.println("To left motor");
      if (isDirection)
        left.dir = parseDirection(msg);
      else
        left.pwm = parsePWM(msg);
        controlMotor(Left, left.dir, left.pwm);
      break;
    case Right:
      Serial.println("To right motor");
      if (isDirection)
        right.dir = parseDirection(msg);
      else
        right.pwm = parsePWM(msg);
      controlMotor(Right, right.dir, right.pwm);
      break;
    case Both:
      Serial.println("To both motors");
      if(isDirection)
        left.dir = right.dir = parseDirection(msg);
      else
        left.pwm = right.pwm = parsePWM(msg);
      controlMotor(Both, min(left.dir, right.dir), min(left.pwm, right.pwm));
      break;

    default:
      Serial.println("bad topic selection");
      break;
    }
  }
}

/*=============Lower level functions============*/

/**
 * handles all the control signals
 * \param motor Left/Right/Both
 * \param direction Stop/Forward/Reverse
 * \param pwm unsigned integer from 0 to 1023
 */
void controlMotor(motor m, direction d, uint16_t pwm)
{
  bool plus_val = false;
  bool minus_val = false;
  //direction handler
  switch(d)
  {
    case Forward:
      plus_val = HIGH;
      minus_val = LOW;
      break;
    case Reverse:
      plus_val = LOW;
      minus_val = HIGH;
      break;
    default:
      plus_val = LOW;
      minus_val = LOW;
      break;
  }
  //motor selector logic
  switch (m)
  {
  case Left:
    //Serial.printf("Left PWM: %u\n", pwm);
    set_L_PWM(pwm);
    digitalWrite(L_PLUS, plus_val);
    digitalWrite(L_MINUS, minus_val);
    break;
  case Right:
    //Serial.printf("Right PWM: %u\n", pwm);
    set_R_PWM(pwm);
    digitalWrite(R_PLUS, plus_val);
    digitalWrite(R_MINUS, minus_val);
    break;
  case Both:
    set_L_PWM(pwm);
    set_R_PWM(pwm);
    setMotorsDir(plus_val, minus_val, plus_val, minus_val);
    break;
  default:
    stop();
    break;
  }
}

/**
 * set motors' direction directly/logically
 * \param In1 Boolean Logic for In1
 * \param In2 Boolean Logic for In2
 * \param In3 Boolean Logic for In3
 * \param In4 Boolean Logic for In4
*/
void setMotorsDir (bool In1, bool In2, bool In3, bool In4)
{
  digitalWrite(L_PLUS, In1);
  digitalWrite(L_MINUS,In2);
  digitalWrite(R_PLUS, In3);
  digitalWrite(R_MINUS,In4);
}

/**
 * used only by wifi_init()
 */
void configModeCallback (WiFiManager *wifi)
{
  Serial.println("Entered config mode: ");
  Serial.println(WiFi.softAPIP());
  Serial.println(wifi->getConfigPortalSSID());
}

/**
 * returns the last topic string from the full topic string
 * used by mqttMessageHandler()
 */
String getLastTopic(String s)
{
  return s.substring( s.lastIndexOf(SLASH)+1, s.length());
}

direction parseDirection(String msg)
{
  //bounds to stop and returns enum direction
  switch (msg.toInt())
  {
  case Forward:
    return Forward;
  case Reverse:
    return Reverse;
  default:
    return Stop;
  }
}

uint16_t parsePWM(String msg)
{
  int val = msg.toInt();
  //bounds the value from 0 to PWM_MAX and returns
  return (val < 0) ? 0 : ((val > PWM_MAX) ? PWM_MAX : msg.toInt());
}