import RPi.GPIO as GPIO
import time

PIR_PIN = 17
LED_PIN = 18
MOTOR_PIN1 = 23
MOTOR_PIN2 = 4

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)       # PIR sensor as input
GPIO.setup(LED_PIN, GPIO.OUT)      # LED as output
GPIO.setup(MOTOR_PIN1, GPIO.OUT)   # Motor as output
GPIO.setup(MOTOR_PIN2, GPIO.OUT)

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
            GPIO.output(MOTOR_PIN1, GPIO.HIGH)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
            time.sleep(5)  # Added correct indentation
        else:
            print("No motion detected, motor stopped, LED off")
            GPIO.output(MOTOR_PIN1, GPIO.LOW)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED
        
        time.sleep(1)  # Check every 1 second

except KeyboardInterrupt:
    print("Program terminated")
finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
