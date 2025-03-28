# this is the V1 script with out the remote conection


from machine import Pin, I2C
import utime
import time
from I2C_LCD import I2C_LCD  # Ensure this matches your library file

# Setup I2C for the LCD (SDA on Pin 0, SCL on Pin 1)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Adjust pins as needed
lcd = I2C_LCD(i2c, 0x27)  # Use the correct address (0x27 is common) to find out the address use the i2cscan.py file

# Initialize the relay and LED
relay = Pin(16, Pin.OUT)
led = Pin(15, Pin.OUT)
led.value(0)  # Initialize LED to OFF

# Create a map between keypad buttons and characters 
# You may have to edit this if you use a diverent keypad
matrix_keys = [['1', '4', '7', 'A'],
               ['2', '5', '8', 'B'],
               ['3', '6', '9', '#'],
               ['*', '0', '#', 'D']]

# Define PINs according to cabling
keypad_rows = [9, 8, 7, 6]
keypad_columns = [5, 4, 3, 2]

col_pins = []
row_pins = []

# The keys entered by the user
guess = []
# Our secret pin, shhh do not tell anyone
secret_pin = ['x', 'x', 'x', 'x'] #the pin (change it now)

# Initialize row and column pins
for x in range(4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(0)  # Set rows to LOW initially
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))

def scankeys():
    for row in range(4):
        row_pins[row].value(1)  # Set current row HIGH
        for col in range(4): 
            if col_pins[col].value() == 1:
                key_press = matrix_keys[row][col]
                print("You have pressed:", key_press)
                lcd.clear()
                lcd.message("You pressed: " + key_press)  # Display pressed key
                utime.sleep(0.3)  # Debounce delay
                guess.append(key_press)
                
                # Check if enough keys have been pressed
                if len(guess) == 4: # if u have more or less than four Digits then change it
                    checkPin(guess)
                    guess.clear()  # Clear guess after checking
                    
        row_pins[row].value(0)  # Set row back to LOW

def checkPin(guess):
    if guess == secret_pin:
        print("You got the secret pin correct")
        lcd.clear()
        lcd.message("Pin correct!")
        relay.value(0)  # Turn the relay ON
        time.sleep(1)
        relay.value(1)  # Turn the relay OFF
        time.sleep(1)
        led.value(1)  # Turn ON LED
        utime.sleep(3)
        led.value(0)  # Turn OFF LED
    else:
        print("Better luck next time")
        lcd.clear()
        lcd.message("Try again!")

print("Enter the secret Pin")
lcd.clear()
lcd.message("Enter Pin:")

while True:
    scankeys()
