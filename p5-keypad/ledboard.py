"""Charlieplexed LED Board"""

from time import sleep, time
from GPIOSimulator_v5 import *
GPIO = GPIOSimulator()

# Aliases
P0 = PIN_CHARLIEPLEXING_0
P1 = PIN_CHARLIEPLEXING_1
P2 = PIN_CHARLIEPLEXING_2

PINS = [P0, P1, P2]
# What pins to set HIGH and LOW respectivly for the kth LED
CHARLIEPLEXING_LEDS = [(P0, P1), (P1, P0), (P1, P2), (P2, P1), (P0, P2), (P2, P0)]
LED_COUNT = len(CHARLIEPLEXING_LEDS)

# When simulating several LEDs being on at once, how long to flash each LED for
PARALLEL_LIGHT_TIME = 0.006

class LedBoard:
    """Class for controlling a Charlieplexed LED Board"""

    def __init__(self, output_function=None):
        if output_function is None:
            output_function = lambda x: GPIO.show_leds_states()
        self.output_function = output_function

    def show_leds_states(self, led=None):
        """Prints the state of the LEDs in the terminal"""
        self.output_function([i==led for i in range(LED_COUNT)])

    def setup(self):
        """Initialize GPIO pins"""
        for pin in PINS:
            GPIO.setup(pin, GPIO.IN)
        self.show_leds_states()

    def clear_leds(self):
        """Turns off all LEDs"""
        for pin in PINS:
            GPIO.setup(pin, GPIO.IN)
        self.show_leds_states()

    def light_led(self, led):
        """Turns on a single LED"""
        output = CHARLIEPLEXING_LEDS[led]
        for pin in PINS:
            GPIO.setup(pin, GPIO.OUT if pin in output else GPIO.IN)
        high, low = output
        GPIO.output(high, GPIO.HIGH)
        GPIO.output(low, GPIO.LOW)
        self.show_leds_states(led)

    def light_in_series(self, leds, time_per):
        """Turns on the given leds in series, with the given time per LED"""
        for led in leds:
            self.light_led(led)
            sleep(time_per)

    def flash_all_leds(self, k, flash_speed=2):
        """Flash all LEDs for k seconds"""
        endtime = time() + k
        time_left = k
        while time_left > 0:
            cleartime = time_left % flash_speed - flash_speed/2
            if cleartime > 0:
                self.clear_leds()
                sleep(cleartime)
            self.light_in_series(range(LED_COUNT), PARALLEL_LIGHT_TIME)
            time_left = endtime - time()

    def twinkle_all_leds(self, k, time_per=0.2):
        """Twinkle all LEDs in sequence for k seconds"""
        for _ in range(int(k / (time_per*LED_COUNT))):
            self.light_in_series(range(LED_COUNT), time_per)
