/**
 * 10-bit speed control
*/

/**
 * PWM frequency can be adjusted on ESP core for Arduino
 * Minimum frequency = 100Hz
 * Maximum frequency = 60000Hz
 */
#define PWM_FREQ 120    //Hz
/*MOTOR L*/
//Left Motor PWM
#define L_PWM 12 //(D6)
/*MOTOR R*/
//Right Motor PWM
#define R_PWM 0 //(D3)


/*Two bits for setting the direction*/
/*MOTOR L*/
//Out1 connects to Left Motor +ve
#define L_PLUS 4 //connects to In1 (D2)
//Out2 connects to Left Motor -ve
#define L_MINUS 0//5 //connects to In2 (D1)

/*MOTOR R*/
//Out3 connects to Right Motor +ve
#define R_PLUS 13 //connects to In3 (D7)
//Out4 connects to Right Motor -ve
#define R_MINUS 14 //connects to In4 (D5)

/*Servo output pin*/
#define SERVO_PIN 15    //(D8)

#define UNLOAD_DEGREE 90
#define SERVO_RESTING_DEGREE 0

/*Onboard LED on ESP8266*/
#define LED 2

#define CONFIG_PIN 5
/**
 * refer to Bot-code/README for ESP-12E pin configurations
 * TODO - revert all the pins carefully
*/