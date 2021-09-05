#ifndef _MOTOR_H_
#define _MOTOR_H_
#include <Arduino.h>
#ifndef PWM_MAX
    #define PWM_MAX 1023
#endif


/** Enum for valid directions
 * Stop = 0
 * Forward = 1
 * Reverse = 2
*/
typedef enum direction
{
    Stop,
    Forward,
    Reverse
} direction;


class Motor
{
private:
    direction dir;
    uint16_t pwm;
    u8 ena, in_plus, in_minus;
public:
    Motor(u8 EnA, u8 In_plus, u8 In_minus);//constructor
    ~Motor();//destructor
    void begin();//initialise IOs
    void release();//stops and sets PWM 0
    bool setDirection(direction);
    bool setPWM(u16);
    bool setParam(direction, u16);
};
#endif