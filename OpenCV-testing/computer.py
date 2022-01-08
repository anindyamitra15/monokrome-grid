import paho.mqtt.client as mqtt
# from random import randint, randrange, uniform
import time
import atexit
#from main import dict
#mqttBroker = "mqtt.eclipseprojects.io"
'''
mqttBroker = "192.168.1.10"
client= mqtt.Client("COMPUTER")
client.connect(mqttBroker)
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

        
                
        #client.publish(topic,mymess)
        print("just publish  "+str(mymess)+" to "+topic)
        #time.sleep(0.2)


        
