import paho.mqtt.client as mqtt
from enum import Enum
# globals, use these for connecting and sending messages
class glb_var:
    bots = []   # add all the bots
    broker = "test.mosquitto.org"
    port = 1883
    clientName = "COMPUTER"
    class sub_topic:
        PARENT = "FromBot"
        BOTLIST = "Botlist"
        ERROR = "Error"
    class pub:
        PARENT = "ToBot"
        class motors(Enum):
            UNLOADER = 0
            MOTOR_LEFT = 1
            MOTOR_RIGHT = 2
            MOTOR_BOTH = 3
        DIRECTION = "Direction"
        PWM = "PWM"

# initialise connection
client = mqtt.Client(glb_var.clientName)
client.connect(glb_var.broker)

'''
def comp(num):
    print(num)
    topic="MOVEMENT"
    if(num==5):
        topic="PACKAGE"
        mymess="5"
    elif(num==4):
        mymess="4"
    elif(num==3):
        mymess="3"
    elif(num==2):
        mymess="2"
    elif(num==1):
        mymess="1"
    else:
        mymess="0"



    client.publish(topic,mymess)
    print("just publish  "+str(mymess)+" to "+topic)
    #time.sleep(0.2)
'''