from machine import Pin, I2C
import utime
import time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


# I2C configuration
I2C_ADDR = 0x27  # Update this if the I2C scan shows a different address
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

#i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Adjust pins as needed
#lcd = I2C_LCD(i2c, 0x27)  # Use the correct address (0x27 is common)
#lcd = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)  # Set to 100 kHz
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)   

# Initialize the relay and LED
relay = Pin(16, Pin.OUT)
led = Pin(15, Pin.OUT)
led.value(0)  # Initialize LED to OFF
relayforswitch = Pin(18, Pin.OUT)

# Create a map between keypad buttons and characters
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
secret_pin = ['7', '8', '8', '4']

# Initialize row and column pins
for x in range(4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(0)  # Set rows to LOW initially
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
def idk():
    print("Enter the secret Pin")
    lcd.clear()
    lcd.putstr("Enter Pin:")
    scankeys()
    
def scankeys():
    for row in range(4):
        row_pins[row].value(1)  # Set current row HIGH
        for col in range(4):
            if col_pins[col].value() == 1:
                key_press = matrix_keys[row][col]
                print("You have pressed:", key_press)
                lcd.clear()
                lcd.putstr("You pressed:    " + key_press)
                lcd.putstr("".join(guess[-3:]))
                utime.sleep(0.3)  # Debounce delay
                guess.append(key_press)
                
                # Check if enough keys have been pressed
                if len(guess) == 4:
                    checkPin(guess)
                    guess.clear()  # Clear guess after checking
        
        row_pins[row].value(0)  # Set row back to LOW

def display_menu():
    lcd.clear()
    lcd.putstr("1: Start PC\n2: LED Toggle\n3: Exit")
    utime.sleep(1)

def scankeysformenu(timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        for row in range(4):
            row_pins[row].value(1)  # Set current row HIGH
            for col in range(4):
                if col_pins[col].value() == 1:
                    key_press = matrix_keys[row][col]
                    print("Menu Selection:", key_press)
                    lcd.clear()
                    lcd.putstr("Selected: " + key_press)
                    utime.sleep(0.3)  # Debounce delay
                    
                    if key_press == '1':
                        activate_relay()
                    elif key_press == '2':
                        toggle_led()
                    elif key_press == '3':
                        lcd.clear()
                        lcd.putstr("Exiting menu")
                        utime.sleep(2)
                        return
                    return  # Exit once a selection is made
            row_pins[row].value(0)  # Set row back to LOW
    lcd.clear()
    lcd.putstr("Menu timed out")
    utime.sleep(2)
    idk()

def activate_relay():
    relayforswitch(1)
    print("Activating relay...")
    lcd.clear()
    lcd.putstr("Starting PC")
    relay.value(1)  # Turn the relay ON
    time.sleep(3)
    relay.value(0)  # Turn the relay OFF
    led.value(1)  # Turn ON LED
    utime.sleep(3)
    led.value(0)  # Turn OFF 
    relayforswitch(0)
    idk()
    

def toggle_led():
    print("Toggling LED...")
    lcd.clear()
    lcd.putstr("Toggling LED")
    led.value(not led.value())  # Toggle LED state
    utime.sleep(1)
    idk()
    

def checkPin(guess):
    if guess == secret_pin:
        print("You got the secret pin correct")
        lcd.clear()
        lcd.putstr("Pin correct!")
        led.value(1)  # Turn ON LED
        utime.sleep(3)
        led.value(0)  # Turn OFF LED
        display_menu()
        scankeysformenu()
    else:
        print("Better luck next time")
        lcd.clear()
        lcd.putstr("Try again!")

print("Enter the secret Pin")
lcd.clear()
lcd.putstr("Enter Pin:")

while True:
    scankeys()
