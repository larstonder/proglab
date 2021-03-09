'''Agent module'''

class Agent:

    def __init__(self, keypad, ledboard, pathname, override_signal):
        '''Inititialize agent'''
        self.keypad = keypad
        self.ledboard = ledboard
        self.pathname = pathname
        self.override_signal = override_signal
    
    def reset_passcode_entry(self):
        '''Clear the passcode-buffer and initiate a “power up” lighting
        sequence on the LED Board.'''
