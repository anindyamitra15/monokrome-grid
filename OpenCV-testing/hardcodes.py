def hardcodes(chip_id):
    chip_id = int(chip_id)
    botlist = [7892874, 1234897, 1123457, 1132268]
    try:
        if chip_id in botlist:
            if chip_id == botlist[0]:
                pwm_left = 200
                pwm_right = 250
                print(pwm_left, pwm_right)
                return pwm_left, pwm_right
            elif chip_id == botlist[1]:
                pwm_left = 200
                pwm_right = 250
                return pwm_left, pwm_right
            elif chip_id == botlist[2]:
                pwm_left = 200
                pwm_right = 250
                return pwm_left, pwm_right
            else:
                pwm_left = 200
                pwm_right = 250
                return pwm_left, pwm_right
    except:
        print("chip id not in botlist")

a, b = hardcodes("7892874")
print(a, b)
