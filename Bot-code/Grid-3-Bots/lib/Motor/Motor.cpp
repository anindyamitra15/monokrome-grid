#include "Motor.h"
#include <Arduino.h>

//Constructor
Motor::Motor(u8 Enable, u8 In_plus, u8 In_minus)
{
    ena = Enable;
    in_plus = In_plus;
    in_minus = In_minus;
}

void Motor::begin()
{
    pinMode(ena,        OUTPUT);
    pinMode(in_plus,    OUTPUT);
    pinMode(in_minus,   OUTPUT);
}

void Motor::release()
{
    setDirection(Stop);
    setPWM(0);
}

bool Motor::setDirection(direction d)
{
    switch (d)
    {
        case Forward:
            digitalWrite(in_plus, HIGH);
            digitalWrite(in_minus, LOW);
            break;
        case Reverse:
            digitalWrite(in_minus, HIGH);
            digitalWrite(in_plus,   LOW);
            break;
        case Stop:
            digitalWrite(in_plus, LOW);
            digitalWrite(in_minus, LOW);
            break;
        default:
            return false;
    }
    return true;
}

bool Motor::setPWM(u16 pwm)
{
    if(pwm < 0 || pwm > PWM_MAX)
        return false;
    analogWrite(ena, pwm);
    return true;
}



bool Motor::setParam(direction d, u16 pwm)
{
    bool flag = true;
    flag &= setDirection(d);
    flag &= setPWM(pwm);
    return flag;
}

Motor::~Motor()
{
    release();
}