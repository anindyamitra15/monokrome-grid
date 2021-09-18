import paho.mqtt.client as mqtt
# import json  # required to parse FromBot/Error
import time
import atexit


# Enums
class enums:
    class motors:
        UNLOADER = 0
        MOTOR_LEFT = 1
        MOTOR_RIGHT = 2
        MOTOR_BOTH = 3

    class directions:
        Stop = 0
        Forward = 1
        Reverse = 2


# globals storing topics and credentials
class cred:
    bots = set()  # add all the bots at runtime
    broker = "192.168.1.10"  # "test.mosquitto.org"
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
        chip_id = int(message.payload)
        cred.bots.add(chip_id)  # add bots to set
        print("Updated list: " + str(cred.bots))

    elif message.topic == cred.topicSub.PARENT + '/' + cred.topicSub.ERROR:
        print(cred.topicSub.ERROR + " is selected")
        # TODO - handle error (if any)


def on_connect(client, userdata, flags, rc):
    print("Connected to: " + cred.broker + " at port: " + str(cred.port))


def on_disconnect(client, userdata, rc):
    print("Client disconnected, attempting to reconnect")
    # TODO- Logic to reconnect
    cred.bots.clear()  # clears the botlist on disconnection


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
def control(chip_id: int, motor: int, **kwargs):
    topic = cred.topicPub.PARENT + '/' + str(chip_id) + '/' + str(motor)
    if chip_id in cred.bots and \
            motor in range(enums.motors.UNLOADER, enums.motors.MOTOR_BOTH + 1):
        if motor == enums.motors.UNLOADER:
            for key, value in kwargs.items():
                if (key == 'logic') and value:
                    print("Unloading")
                    client.publish(topic, payload=1 if value else 0)
        else:  # if motors are selected
            for key, value in kwargs.items():
                if (key == 'direction') and \
                        (value in range(enums.directions.Stop, enums.directions.Reverse + 1)):
                    direction = int(value)
                    client.publish(topic + '/' + str(cred.topicPub.DIRECTION), payload=direction)
                    print("Published direction: " + str(direction) + " to " + str(motor))
                if (key == 'pwm') and \
                        (value in range(0, 1024)):
                    pwm = int(value)
                    client.publish(topic + '/' + str(cred.topicPub.PWM), payload=pwm)
                    print("Setting pwm: " + str(pwm) + " to " + str(motor))
    else:
        print("Bot not present in set")


def on_exit():
    client.loop_stop()


# test loop showing some usages for standalone testing (running only mqtt_router.py)
# instruction: just publish FromBot/Botlist=12936642 in mqtt explorer at the same IP
# and let the fun begin
if __name__ == '__main__':
    atexit.register(on_exit)
    while True:
        print("Alive")
        time.sleep(2)
        # demo 1: activating unloader
        control(7892874, enums.motors.UNLOADER, logic=True)
        time.sleep(2)
        # demo 2: setting left motor forward direction
        control(7892874, enums.motors.MOTOR_BOTH, direction=1, pwm=250)
        time.sleep(2)
        # demo 3: setting left motor to stop
        control(7892874, enums.motors.MOTOR_BOTH, direction=enums.directions.Stop, pwm=0)
        time.sleep(2)
        # demo 4: setting left motor reverse direction
        control(7892874, enums.motors.MOTOR_BOTH, direction=2, pwm=250)
        time.sleep(2)
        # demo 5: setting left motor pwm: 1023
        control(7892874, enums.motors.MOTOR_BOTH, pwm=1023)
        time.sleep(2)
        # demo 3: setting left motor to stop
        control(7892874, enums.motors.MOTOR_BOTH, direction=0, pwm=0)
        # # demo 6: setting both direction: reverse and pwm: 102 to left motor
        # control(7889076, enums.motors.MOTOR_LEFT, direction=2, pwm=102)
# TODO call client.loop_stop() from main.py whenever exit/end event occurs
