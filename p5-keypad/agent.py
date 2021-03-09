'''Agent module'''

from time import sleep
from rule import signal_is_digit

class Agent:
    """Agent class containing state"""

    def __init__(self, keypad, ledboard, pathname):
        '''Inititialize agent'''
        self.keypad = keypad
        self.ledboard = ledboard
        self.pathname = pathname
        self.override_signal = None
        self.passcode_buffer = ''
        self.selected_led = None
        self.led_time = '0'
        self.new_passcode_1 = ''
        self.new_passcode_2 = ''
    
    def get_next_signal(self):
        '''Returns the override signal, if it is non-blank; otherwise query the
        keypad for the next pressed key'''
        temp = self.override_signal
        self.override_signal = None
        return self.keypad.get_next_signal() if temp is None else temp
    
    def prepare_passcode_entry(self):
        '''Clear the passcode-buffer and initiate a “power up” lighting
        sequence on the LED Board.'''
        self.passcode_buffer = ''
        self.override_signal = None
        self.ledboard.power_on_animation()
    
    def append_next_passcode_digit(self, digit):
        """Appends next passcode digit"""
        assert signal_is_digit(digit)
        self.passcode_buffer += digit
        print(digit,end="",flush=True)
    
    def verify_login(self):
        '''Checks that the passcode just entered via the keypad matches that in the
        passcode file. Stores the result (Y or N) in the override signal. Calls the
        LED Board to initiate the appropriate lighting pattern for login success or failure'''
        with open(self.pathname) as passcode:
            passcode = passcode.readline().strip()
        
        self.override_signal = 'Y' if passcode == self.passcode_buffer else 'N'
        self.passcode_buffer = ''
    
    def fully_activate(self):
        """Fully activates agent"""
        self.twinkle_leds()

    def ready_led(self, led):
        """Ready led for lighting"""
        self.selected_led = int(led)
        self.led_time = '0'

    def append_led_time(self, digit):
        """Take duration for led"""
        self.led_time += digit

    def light_selected_led(self):
        """Light the selected led for selected duration seconds"""
        duration = int(self.led_time)
        self.ledboard.light_led(self.selected_led)
        sleep(duration)
        self.ledboard.clear_leds()

    def start_new_passcode(self):
        """Start passcode changing"""
        self.new_passcode_1 = ''
        self.new_passcode_2 = ''
    
    def append_new_passcode_1(self, digit):
        """Appends new digit to passcode 1"""
        self.new_passcode_1 += digit

    def append_new_passcode_2(self, digit):
        """Appends new digit to passcode 2"""
        self.new_passcode_2 += digit
    
    def apply_new_passcode(self):
        """Apply new passcode if passcode 1 and passcode 2 are equal"""
        if self.new_passcode_1 != self.new_passcode_2:
            self.fully_activate()
            return

        with open(self.pathname, "w") as passcode:
            passcode.write(self.new_passcode_1)
        self.flash_leds()
    
    def light_one_led(self, led):
        '''Using values stored in the Lid and Ldur slots, calls the LED Board and
        request that LED # Lid be turned on for Ldur seconds.'''
        self.ledboard.light_led(led)

    def flash_leds(self):
        '''Calls the LED Board and request the flashing of all LEDs'''
        self.ledboard.flash_all_leds(1)
    
    def twinkle_leds(self):
        '''Call the LED Board and request the twinkling of all LEDs.'''
        self.ledboard.twinkle_all_leds(1)
    
    def reset_keypad(self):
        '''Call the LED Board to initiate the “power down” lighting sequence.'''
        self.ledboard.power_off_animation()
