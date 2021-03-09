#!/usr/bin/env python3

'''Main keypad module'''

from keypad import Keypad
from ledboard import LedBoard
from agent import Agent
from fsm import FSM
from terminal import disable_echo, TerminalDisplayer

COOL_TERMINAL = True


def main():
    """main function for keypad program"""

    # Turn off repeating input
    disable_echo()

    keypad = Keypad()
    keypad.setup()

    if COOL_TERMINAL:
        displayer = TerminalDisplayer(led_count = 6)
        ledboard = LedBoard(displayer.set_led_states)
        displayer.start_display_loop_thread()
    else:
        ledboard = LedBoard()
    ledboard.setup()

    agent = Agent(keypad, ledboard, 'password.txt')

    fsm = FSM('start', 'end', agent)

    fsm.run()
    
    if COOL_TERMINAL:
        displayer.stop_display_loop_thread()


if __name__ == "__main__":
    main()
