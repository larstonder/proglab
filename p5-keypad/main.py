#!/usr/bin/env python3

'''Main keypad module'''

from time import sleep
from keypad import Keypad
from terminal import disable_echo

def main():
    '''main function for keypad program'''

    # Turn off repeating input
    disable_echo()
    keypad = Keypad()

    while True:
        press = keypad.poll()
        if press is not None:
            print(press)
        sleep(0.016)

if __name__ == "__main__":
    main()
