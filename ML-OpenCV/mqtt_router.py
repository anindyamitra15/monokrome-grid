import paho.mqtt.client as mqtt
import json  # required to parse FromBot/Error
import threading  # for mqtt loop
from enum import Enum
from numpy import uint16


# globals storing topics and credentials
class cred:
    bots = []  # add all the bots at runtime TODO replace with np.array
    broker = "test.mosquitto.org"
    port = 1883
    clientName = "COMPUTER"

    class topicSub:
        PARENT = "FromBot"
        BOTLIST = "Botlist"
        ERROR = "Error"

    class topicPub:
        PARENT = "ToBot"

        class motors(Enum):
            UNLOADER = 0
            MOTOR_LEFT = 1
            MOTOR_RIGHT = 2
            MOTOR_BOTH = 3

        class directions(Enum):
            Stop = 0
            Forward = 1
            Reverse = 2

        DIRECTION = "Direction"
        PWM = "PWM"


# on message handler, adds chip ids to list and handles errors
def on_message(client, userdata, message):
    print("message: " + message.payload + " arrives on " + message.topic)

    if message.topic == cred.topicSub.PARENT + '/' + cred.topicSub.BOTLIST:
        print(cred.topicSub.BOTLIST + " is selected")
        chip_id = message.payload

        # TODO - replace logic below with np.array for optimisation
        if chip_id not in cred.bots:
            cred.bots.append(chip_id)

    elif message.topic == cred.topicSub.PARENT + '/' + cred.topicSub.ERROR:
        print(cred.topicSub.ERROR + " is selected")
        # TODO - handle error (if any)


# initialise connection
client = mqtt.Client(cred.clientName)
client.connect(cred.broker, cred.port)
client.subscribe(topic=cred.topicSub.PARENT + '/+')  # single level wildcard for multiple topics

# handlers
client.on_connect = lambda: print("Connected to: " + cred.broker + " at port: " + str(cred.port))
client.on_disconnect = lambda: \
    print("Client disconnected, attempting to reconnect") \
    # TODO- Logic to reconnect
client.on_subscribe = lambda: print("listening to: " + cred.topicSub.PARENT + '/+')
client.on_message = on_message  # message handler binding


# Control (publisher) Methods, overloaded
# First definition for Unloader control
def control(chip_id, motor: cred.topicPub.motors = cred.topicPub.motors.UNLOADER, state: bool = False):
    print("servo")
    if state & \
            (motor == cred.topicPub.motors.UNLOADER) & \
            (str(chip_id) in cred.bots):
        # prepare topic
        topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor)
        # publish message
        client.publish(topic, payload=state)
        print(topic + " is set to " + state)


# Second overload, for motor Direction control
def control(chip_id,
            motor: cred.topicPub.motors,
            direction: cred.topicPub.directions):
    if str(chip_id) in cred.bots:
        topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor) + '/' + cred.topicPub.DIRECTION
        client.publish(topic, payload=direction)
        print(topic + "is set to " + direction)


# Third overload, for motor PWM control
def control(chip_id,
            motor: cred.topicPub.motors,
            pwm: uint16):
    if str(chip_id) in cred.bots:
        topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor) + '/' + cred.topicPub.PWM
        client.publish(topic, payload=pwm)
        print(topic + "is set to " + pwm)


# Final overload, for direction and PWM control
def control(chip_id,
            motor: cred.topicPub.motors,
            direction: cred.topicPub.DIRECTION,
            pwm: uint16):
    control(chip_id, motor, pwm)
    control(chip_id, motor, direction)

# TODO add MQTT loop logic in a thread
