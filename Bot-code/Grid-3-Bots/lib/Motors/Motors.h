#ifndef _MOTORS_H_
#define _MOTORS_H_
#include <Arduino.h>
#define set_L_PWM(pwm) \
    analogWrite(L_PWM, pwm);
#define set_R_PWM(pwm) \
    analogWrite(R_PWM, pwm);

/**
 * enum for valid motor selection
 * Unloader = 0
 * Left = 1
 * Right = 2
 * Both = 3
 */
typedef enum motor
{
    Unloader,
    Left,
    Right,
    Both
} motor;

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


class Motors
{
private:
    direction dir;
    uint16_t pwm;
public:
    Motors(u8 EnA, u8 In1, u8 In2, u8 In3, u8 In4, u8 EnB);
    ~Motors();
};

Motors::Motors(/* args */)
{

}

Motors::~Motors()
{
}

#endif