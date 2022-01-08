from mqtt_router import control
from utils import checker

def start(dist1,dist2,pwm):

    if (not checker(dist1,dist2)) or pwm != 500 :
        control(id, 3, direction=1, pwm=pwm)
        pwm +=1
    else:
        control(id,3,direction=0,pwm=0)





    
