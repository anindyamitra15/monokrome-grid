/**
 * 10-bit speed control
*/

/**
 * PWM frequency can be adjusted on ESP core for Arduino
 * Minimum frequency = 100Hz
 * Maximum frequency = 60000Hz
 */
#define PWM_FREQ 200    //Hz
/*MOTOR L*/
//Left Motor PWM
#define L_PWM 12
/*MOTOR R*/
//Right Motor PWM
#define R_PWM 13


/*Two bits for setting the direction*/
/*MOTOR L*/
//Out1 connects to Left Motor +ve
#define L_PLUS 4 //connects to In1
//Out2 connects to Left Motor -ve
#define L_MINUS 5 //connects to In2

/*MOTOR R*/
//Out3 connects to Right Motor +ve
#define R_PLUS 0 //connects to In3
//Out4 connects to Right Motor -ve
#define R_MINUS 14 //connects to In4

/*Servo output pin*/
#define SERVO_PIN 15
/*Onboard LED on ESP8266*/
#define LED 2
/**
 * refer to Bot-code/README for ESP-12E pin configurations
 * 
*/