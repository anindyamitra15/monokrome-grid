//Final implementation
#include <Arduino.h>
#include <WiFiManager.h>
#include <ArduinoMqttClient.h>
#include <Servo.h>
#include "config.h"
#include "PINS.h"
#include "Motor.h"
/*=============MACROS==============*/

#define BAUD 76800

/*====Topics Macros====*/
#define TOPIC_SUB "ToBot"
#define TOPIC_PUB "FromBot"
#define SLASH String('/')
/*====Topics Macros======*/

/*=======Globals=======*/

/**
 * enum for valid motor selection
 * Unloader = 0
 * Left = 1
 * Right = 2
 * Both = 3
 */
typedef enum motor {Unloader, Left, Right, Both} motor;


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

const unsigned long servo_unload_wait = 40;
Servo unloader; //unloader servo object
Motor left(L_PWM, L_PLUS, L_MINUS);
Motor right(R_PWM, R_PLUS, R_MINUS);
WiFiClient wifiClient;
MqttClient mqttClient (wifiClient);

/*==============Function Prototypes====================*/

void io_init(void);
bool mqtt_init(void);
void wifi_init(void);
void topics_init(void);

void stop(bool);  //improve definition
void unload(void); //improve definition

bool publishChipId(void);
bool publishError(String);  //Change definition
bool subscribe_to_pc(void);
bool publishUnloader (bool);

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
  stop(false);
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
 * \param brake on true, braking action occurs on the motors
 * TODO - improve definition
 */
void stop (bool brake)
{
  left.release();
  right.release();
  if(brake)
  {
    left.setPWM(PWM_MAX);
    right.setPWM(PWM_MAX);
  }
}

/**
 * Unloads the load
 * and resets servo to position
 */
void unload (void)
{
  stop(true);//stop and brake

  for(int i = 0; i <= UNLOAD_DEGREE; i+=5)
  {
    unloader.write(i);
    delay(servo_unload_wait);
  }
  unloader.write(SERVO_RESTING_DEGREE);

  stop(false);//disable braking
}

/**
 * Input Output Initialiser function
 */
void io_init (void)
{
  left.begin();
  right.begin();
  pinMode(LED, OUTPUT);
  analogWriteFreq (PWM_FREQ);
  unloader.attach(SERVO_PIN);
  unloader.write(SERVO_RESTING_DEGREE);
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
    Serial.print(F("MQTT connection failed! Error code = "));
    Serial.println(mqttClient.connectError());
    return false;
  }
  Serial.println(F("You're connected to the MQTT broker!"));
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
  sub.direction = F("Direction");
  sub.pwm = F("PWM");

  //Publish topics Struct initialise
  pub.parent = TOPIC_PUB;
  pub.botlist = pub.parent + SLASH + F("Botlist");
  pub.error = pub.parent + SLASH + F("Error");
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
  Serial.print(F("Publishing ChipId to: "));
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
  Serial.print(F("Publishing Error to: "));
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
  Serial.print(F("Subscribing to topics: "));
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
      Serial.println(F("unloader deactivated"));
  else
  {
    Serial.println(F("Motor Commands Incoming"));
    bool isDirection = (getLastTopic(msgTopic).equals(sub.direction));
    Serial.print(isDirection ? "Direction = " : "PWM = ");
    Serial.println(isDirection ? parseDirection(msg) : parsePWM(msg));
    //selects the motor from topic
    switch (topic)
    {
    case Left:
      Serial.println(F("To left motor"));
      if (isDirection)
        left.setDirection(parseDirection(msg));
      else
        left.setPWM(parsePWM(msg));
      break;
    case Right:
      Serial.println(F("To right motor"));
      if (isDirection)
        right.setDirection(parseDirection(msg));
      else
        right.setPWM(parsePWM(msg));
      break;
    case Both:
      Serial.println(F("To both motors"));
      if(isDirection)
      {
        direction d = parseDirection(msg);
        left.setDirection(d);
        right.setDirection(d);
      }
      else
      {
        uint16_t pwm = parsePWM(msg);
        left.setPWM(pwm);
        right.setPWM(pwm);
      }
      break;
    default:
      Serial.println(F("bad topic selection"));
      break;
    }
  }
}

/*=============Lower level functions============*/


/**
 * used only by wifi_init()
 */
void configModeCallback (WiFiManager *wifi)
{
  Serial.println(F("Entered config mode: "));
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
