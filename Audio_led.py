#this class communicates with the audio and gives us back volume
#and pitch so we could set the color on the led strip

#import libs
import random
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

class asdf:
    color_led = (0,0,0)

def get_pitch():

    b = asdf.color_led
    asdf.color_led = (0,0,0)
    return b


def button_callback(channel):
    asdf.color_led = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    print("Button was pushed!")


def setup():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(21,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
