#imported libs
import time
import Audio_led
from rpi_ws281x import *


# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_BRIGHTNESS = 255


#color led strip functions-------------------------------------------------------------------------
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)




snail_len = 4
led_lst = [(0,0,0)] * (LED_COUNT+snail_len)

def start_colorSnale(strip, wait_ms=50):
    """wipes a snale across display len pixels at a time"""
    while True:
        for j in range(snail_len):
            #update the leds
            for i in range(snail_len,strip.numPixels()):
                strip.setPixelColor(i, led_lst[i])
            strip.show()

            #sleep
            time.sleep(wait_ms / 1000.0)

            #shift right the list
            for i in range(strip.numPixels()-1,0,-1):
                led_lst[i] = led_lst[i-1]

        add_colorsnale(get_color())

def add_colorsnale(color):
    """adds color to the snail"""
    r = color[0]
    g = color[1]
    b = color[2]

    for i in range(snail_len):
        led_lst[i] = (r,g,b)







#temp function
def get_color():
    return Audio_led.get_pitch()

def main():
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    start_colorSnale(strip)







if __name__ == '__main__':
    main()