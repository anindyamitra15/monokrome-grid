import paho.mqtt.client as mqtt
import json  # required to parse FromBot/Error
from enum import Enum
from numpy import uint16
import numpy as np
import time


# Enums
class enums:
    class motors(Enum):
        UNLOADER = 0
        MOTOR_LEFT = 1
        MOTOR_RIGHT = 2
        MOTOR_BOTH = 3

    class directions(Enum):
        Stop = 0
        Forward = 1
        Reverse = 2


# globals storing topics and credentials
class cred:
    bots = np.array([])  # add all the bots at runtime TODO replace with np.array
    broker = "192.168.0.10"  # "test.mosquitto.org"
    port = 1883
    clientName = "COMPUTER"

    class topicSub:
        PARENT = "FromBot"
        BOTLIST = "Botlist"
        ERROR = "Error"

    class topicPub:
        PARENT = "ToBot"
        DIRECTION = "Direction"
        PWM = "PWM"


# on message handler, adds chip ids to list and handles errors
def on_message(client, userdata, message):
    print("message: " + str(message.payload) + " arrives on " + message.topic)

    if message.topic == cred.topicSub.PARENT + '/' + cred.topicSub.BOTLIST:
        print(cred.topicSub.BOTLIST + " is selected")
        chip_id = message.payload

        # TODO - replace logic below with np.array for optimisation
        if str(chip_id) not in cred.bots:
            cred.bots = np.append(cred.bots, str(chip_id))  # check
            print("New Bot added: " + str(chip_id))
            print(cred.bots)

    elif message.topic == cred.topicSub.PARENT + '/' + cred.topicSub.ERROR:
        print(cred.topicSub.ERROR + " is selected")
        # TODO - handle error (if any)


def on_connect(client, userdata, flags, rc):
    print("Connected to: " + cred.broker + " at port: " + str(cred.port))


def on_disconnect(client, userdata, rc):
    print("Client disconnected, attempting to reconnect")
    # TODO- Logic to reconnect


def on_subscribe(client, userdata, mid, granted_qos):
    print("Listening to: " + cred.topicSub.PARENT + '/+')


# initialise client
client = mqtt.Client(cred.clientName)

# binding handlers
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message  # message handler binding

# connect and subscribe
client.connect(cred.broker, cred.port)
client.subscribe(topic=cred.topicSub.PARENT + '/+')  # single level wildcard for multiple topics
client.loop_start()  # threaded loop begins


# Control (publisher) Methods, overloaded
# First definition for Unloader control
def control(chip_id,
            motor: enums.motors = enums.motors.UNLOADER,
            state: bool = False):
    print("servo")
    if state & \
            (motor == enums.motors.UNLOADER) & \
            (chip_id in cred.bots):
        # prepare topic
        topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(0)  # enums.motors.UNLOADER does not work, so 0
        # publish message
        output = str(1 if state else 0)
        client.publish(topic, payload=output)
        print(topic + " is set to " + output)


# TODO redefine control() properly
# # Second overload, for motor Direction control
# def control(chip_id,
#             motor: enums.motors,
#             direction: enums.directions):
#     if str(chip_id) in cred.bots:
#         topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor) + '/' + cred.topicPub.DIRECTION
#         client.publish(topic, payload=direction)
#         print(topic + "is set to " + str(direction))
#
#
# # Third overload, for motor PWM control
# def control(chip_id,
#             motor: enums.motors,
#             pwm: uint16):
#     if str(chip_id) in cred.bots:
#         topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor) + '/' + cred.topicPub.PWM
#         client.publish(topic, payload=pwm)
#         print(topic + "is set to " + pwm)
#
#
# # Final overload, for direction and PWM control
# def control(chip_id,
#             motor: enums.motors,
#             direction: enums.directions,
#             pwm: uint16):
#     control(chip_id, motor, pwm)
#     control(chip_id, motor, direction)

# test loop
while True:
    print("Alive")
    time.sleep(5)

# TODO call client.loop_stop() from main.py whenever exit/end event occurs
