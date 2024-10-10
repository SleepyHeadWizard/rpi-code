import RPi.GPIO as GPIO
import time

# Define GPIO pins for Ultrasonic Sensor
TRIG = 23
ECHO = 24

# Define GPIO pins for LCD
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 12
LCD_D6 = 16
LCD_D7 = 20

# Define LCD constants
LCD_WIDTH = 16  # Max characters per line
LCD_CHR = True  # Sending data
LCD_CMD = False  # Sending command

# Timing constants for LCD
E_PULSE = 0.0005
E_DELAY = 0.0005

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

# Function to send byte to data pins (LCD)
def lcd_send_byte(bits, mode):
    # mode = True for data, False for command
    GPIO.output(LCD_RS, mode)
    
    # High bits
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()
    
    # Low bits
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    
    # Toggle 'Enable' pin
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

# Initialize LCD display
def lcd_init():
    lcd_send_byte(0x33, LCD_CMD)  # 110011 Initialize
    lcd_send_byte(0x32, LCD_CMD)  # 110010 Initialize
    lcd_send_byte(0x28, LCD_CMD)  # 101000 4-bit mode, 2-line, 5x8 font
    lcd_send_byte(0x0C, LCD_CMD)  # 001100 Display on, cursor off, blink off
    lcd_send_byte(0x06, LCD_CMD)  # 000110 Entry mode, move right, no shift
    lcd_send_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)

# Main program
try:
    # Initialize LCD
    lcd_init()

    # Set up the ultrasonic sensor
    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle")
    time.sleep(2)

    # Loop to read sensor and display on LCD
    while True:
        # Send ultrasonic pulse
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Wait for echo response
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        # Display distance on LCD
        lcd_send_byte(0x01, LCD_CMD)  # Clear display
        lcd_send_byte(ord('D'), LCD_CHR)
        lcd_send_byte(ord('i'), LCD_CHR)
        lcd_send_byte(ord('s'), LCD_CHR)
        lcd_send_byte(ord('t'), LCD_CHR)
        lcd_send_byte(ord('a'), LCD_CHR)
        lcd_send_byte(ord('n'), LCD_CHR)
        lcd_send_byte(ord('c'), LCD_CHR)
        lcd_send_byte(ord('e'), LCD_CHR)
        lcd_send_byte(ord(':'), LCD_CHR)
        lcd_send_byte(ord(' '), LCD_CHR)

        # Convert distance to string and display it
        for char in str(distance):
            lcd_send_byte(ord(char), LCD_CHR)

        # Pause for a moment
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
