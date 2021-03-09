#!/usr/bin/env python3

'''Main keypad module'''

from keypad import Keypad
from ledboard import LedBoard
from agent import Agent
from fsm import FSM
from rule import Rule, signal_is_digit
from terminal import disable_echo, TerminalDisplayer

from os.path import join, dirname, realpath

PASSCODE_FILE = join(dirname(realpath(__file__)), "passcode.txt")

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

    agent = Agent(keypad, ledboard, PASSCODE_FILE)

    fsm = FSM('S-Init', [], agent)

    any_signal = lambda signal: True
    signal_05 = lambda signal: signal in ['0','1','2','3','4','5']
    fsm.add_rule(Rule('S-Init', 'S-Read', any_signal, lambda agent, _: agent.prepare_passcode_entry()))
    fsm.add_rule(Rule('S-Read', 'S-Read', signal_is_digit, lambda agent, signal: agent.append_next_passcode_digit(signal)))
    fsm.add_rule(Rule('S-Read', 'S-Verify', '*', lambda agent, _: agent.verify_login()))
    fsm.add_rule(Rule('S-Read', 'S-Init', any_signal, lambda agent, _: agent.reset_keypad()))
    fsm.add_rule(Rule('S-Verify', 'S-Active', 'Y', lambda agent, _: agent.fully_activate()))
    fsm.add_rule(Rule('S-Verify', 'S-Init', any_signal, lambda agent, _: agent.reset_keypad()))

    # Logging out
    fsm.add_rule(Rule('S-Active', 'S-Logout', '#'))
    fsm.add_rule(Rule('S-Logout', 'S-Init', '#', lambda agent, _: agent.reset_keypad()))
    fsm.add_rule(Rule('S-Logout', 'S-Active', any_signal, lambda agent, _: agent.fully_activate()))

    # Lighting a single LED
    fsm.add_rule(Rule('S-Active', 'S-Led', signal_05, lambda agent, signal: agent.ready_led(signal)))
    fsm.add_rule(Rule('S-Led', 'S-Time', '*'))
    fsm.add_rule(Rule('S-Led', 'S-Active', any_signal, lambda agent, _: agent.fully_activate()))
    fsm.add_rule(Rule('S-Time', 'S-Time', signal_is_digit, lambda agent, signal: agent.append_led_time(signal)))
    fsm.add_rule(Rule('S-Time', 'S-Active', '#', lambda agent, _: agent.fully_activate()))
    fsm.add_rule(Rule('S-Time', 'S-Active', '*', lambda agent, _: agent.light_selected_led()))

    # Changing password
    fsm.add_rule(Rule('S-Active', 'S-Read2', '*', lambda agent, _: agent.start_new_passcode()))
    fsm.add_rule(Rule('S-Read2', 'S-Read2', signal_is_digit, lambda agent, signal: agent.append_new_passcode_1(signal)))
    fsm.add_rule(Rule('S-Read2', 'S-Read3', '*'))
    fsm.add_rule(Rule('S-Read2', 'S-Active', any_signal, lambda agent, _: agent.fully_activate()))
    fsm.add_rule(Rule('S-Read3', 'S-Read3', signal_is_digit, lambda agent, signal: agent.append_new_passcode_2(signal)))
    fsm.add_rule(Rule('S-Read3', 'S-Active', '*', lambda agent, _: agent.apply_new_passcode()))
    fsm.add_rule(Rule('S-Read3', 'S-Active', any_signal, lambda agent, _: agent.fully_activate()))

    
    fsm.run()
    
    if COOL_TERMINAL:
        displayer.stop_display_loop_thread()


if __name__ == "__main__":
    main()
