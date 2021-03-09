'''Helper for terminal control'''

import sys
from threading import Thread, Lock
from time import sleep
from os import isatty
from importlib.util import find_spec


def disable_echo():
    '''Turn off echo in the terminal for the duration of the program'''

    filedesc = sys.stdin.fileno()
    if find_spec("termios") is None:
        return

    if not isatty(filedesc):
        return

    import termios
    import atexit

    def enable_echo(enabled):
        '''Set echo state for the given file descriptor'''
        (iflag, oflag, cflag, lflag, ispeed, ospeed, ccvalue) = termios.tcgetattr(filedesc)

        if enabled:
            lflag |= termios.ECHO
        else:
            lflag &= ~termios.ECHO

        new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, ccvalue]
        termios.tcsetattr(filedesc, termios.TCSANOW, new_attr)

    enable_echo(False)
    atexit.register(enable_echo, True)


class TerminalDisplayer:
    """Class for writing LEDs to the terminal, with double buffering"""

    def __init__(self, led_count, time_per_frame=0.1):
        self.led_count = led_count
        self.time_per_frame = time_per_frame
        self.running = False
        self.currentbuffer = None
        self.framebuffer = [False]*led_count
        self.current_state = [False]*led_count
        self.buffer_lock = Lock()

    def __cool_led_output(self):
        offchar = "\033[37m*"
        onchar = "\033[31m*"
        reset = "\033[0m"
        chars = [(onchar if led else offchar) for led in self.currentbuffer]
        print("\r", *chars, sep="   ", end=reset, flush=True)

    def __display_loop(self):
        print()
        while True:
            with self.buffer_lock:
                if not self.running:
                    break
                if self.framebuffer != self.currentbuffer:
                    self.currentbuffer = self.framebuffer
                    self.__cool_led_output()
                self.framebuffer = self.current_state
            sleep(self.time_per_frame)
        print()
        print()

    def set_led_states(self, state):
        """Update what LEDs are currently being powered"""
        assert len(state) == self.led_count
        with self.buffer_lock:
            self.current_state = state
            self.framebuffer = [prev or new for prev, new in zip(self.framebuffer, state)]

    def start_display_loop_thread(self):
        """Start the display update loop"""
        if self.running:
            return

        self.running = True
        Thread(target=TerminalDisplayer.__display_loop, args=(self,)).start()

    def stop_display_loop_thread(self):
        """Stop the display update loop"""
        with self.buffer_lock:
            self.running = False
