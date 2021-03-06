'''Keypad module'''

from time import time, sleep
from GPIOSimulator_v5 import *
GPIO = GPIOSimulator()

# We output on rows, input on columns
ROWS = [PIN_KEYPAD_ROW_0, PIN_KEYPAD_ROW_1, PIN_KEYPAD_ROW_2, PIN_KEYPAD_ROW_3]
COLS = [PIN_KEYPAD_COL_0, PIN_KEYPAD_COL_1, PIN_KEYPAD_COL_2]

# The key matrix, rows first
KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']

# How long to press the key for
PRESS_DURATION = 0.02
REPEAT_KEY_DURATION = 1

# How long to delay between each poll
POLL_DELAY = 0.04


class Keypad:
    '''Keypad class'''

    def __init__(self):
        self.press_end = [None] * len(ROWS) * len(COLS)

    @staticmethod
    def setup():
        """Initializes the GPIO pins"""
        for row in ROWS:
            GPIO.setup(row, GPIO.OUT)
        for col in COLS:
            GPIO.setup(col, GPIO.IN, state=GPIO.LOW)

    def do_polling(self):
        """Checks the keypad for pressed buttons, returns key or None"""
        press = None

        now = time()
        for rowindex, row in enumerate(ROWS):
            GPIO.output(row, GPIO.HIGH)
            for colindex, col in enumerate(COLS):
                index = colindex + rowindex * len(COLS)
                if GPIO.input(col) == GPIO.HIGH:
                    if self.press_end[index] is None:
                        self.press_end[index] = now + PRESS_DURATION
                    if now >= self.press_end[index]:
                        press = KEYS[index]
                        self.press_end[index] = now + REPEAT_KEY_DURATION
                else:
                    self.press_end[index] = None
            GPIO.output(row, GPIO.LOW)

        return press

    def get_next_signal(self):
        """Polls until a key is pressed"""
        while True:
            press = self.do_polling()
            if press is not None:
                return press
            sleep(POLL_DELAY)
