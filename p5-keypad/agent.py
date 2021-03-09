'''Agent module'''

from rule import signal_is_digit
class Agent:

    def __init__(self, keypad, ledboard, pathname):
        '''Inititialize agent'''
        self.keypad = keypad
        self.ledboard = ledboard
        self.pathname = pathname
        self.override_signal = None
        self.passcode_buffer = ''
    
    def reset_passcode_entry(self):
        '''Clear the passcode-buffer and initiate a “power up” lighting
        sequence on the LED Board.'''
        self.reset_password_accumulator()
        self.ledboard.power_on_animation()
    
    def get_next_signal(self):
        '''Returns the override signal, if it is non-blank; otherwise query the
        keypad for the next pressed key'''
        temp = self.override_signal
        self.override_signal = None
        return self.keypad.get_next_signal() if temp is None else temp
    
    def reset_password_accumulator(self):
        """Resets password accumulator"""
        self.passcode_buffer = ''
        self.override_signal = None
    
    def append_next_password_digit(self, digit):
        """Appends next password digit"""
        assert signal_is_digit(digit)
        self.passcode_buffer += digit
    
    def verify_login(self):
        '''Checks that the password just entered via the keypad matches that in the
        password file. Stores the result (Y or N) in the override signal. Calls the
        LED Board to initiate the appropriate lighting pattern for login success or failure'''
        # self.passcode_buffer
    
    def validate_passcode_change(self, new_password):
        '''Checks that the new password is legal. Writes the new
        password in the password file. Uses the LED
        Board to signal success or failure in changing the password'''
    
    def light_one_led(self, led):
        '''Using values stored in the Lid and Ldur slots, calls the LED Board and
        request that LED # Lid be turned on for Ldur seconds.'''
        self.ledboard.light_led(led)

    def flash_leds(self):
        '''Calls the LED Board and request the flashing of all LEDs'''
        self.ledboard.flash_all_leds()
    
    def twinkle_leds(self):
        '''Call the LED Board and request the twinkling of all LEDs.'''
        self.ledboard.twinkle_all_leds()
    
    def exit_action(self):
        '''Call the LED Board to initiate the “power down” lighting sequence.'''
        self.ledboard.power_off_animation()