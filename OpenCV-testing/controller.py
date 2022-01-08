import sys

from mqtt_router import *

def killjoy_bot_controller(chip_id, instruction):
    chip_id = int(chip_id)
    try:
        if instruction == "up":
            control(chip_id=chip_id, motor=3, direction=1, pwm=800)
        elif instruction == "down":
            control(chip_id=chip_id, motor=3, direction=2, pwm=800)
        elif instruction == "stop":
            control(chip_id=chip_id, motor=3, direction=0, pwm=0)
        elif instruction == "left":     #use angle checker func to detect instantaneous angle and stop line 13 and 18 at that point
            control(chip_id=chip_id, motor=3, direction='0', pwm='0')    #can either call stop and then use left or call stop directly
            control(chip_id=chip_id, motor=2, direction='1', pwm='650')  # calibrate pwm
            control(chip_id=chip_id, motor=1, direction='0', pwm='0')  # calibrate pwm if req
            control(chip_id=chip_id, motor=3, direction='0', pwm='0')
        elif instruction == "right":
            control(chip_id=chip_id, motor=3, direction='0', pwm='0')  # can either call stop and then use left or call stop directly
            control(chip_id=chip_id, motor=1, direction='1', pwm='650')  # calibrate pwm
            control(chip_id=chip_id, motor=2, direction='0', pwm='0')  # calibrate pwm if req
            control(chip_id=chip_id, motor=3, direction='0', pwm='0')

        elif instruction == "unload":
            control(chip_id=chip_id, motor=0)
        else:
            print("Wrong Instruction")
    except ValueError:
        print("Quitting program, done successfully")
        sys.exit()
