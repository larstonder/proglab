'''Helper for terminal control'''

import termios
import atexit
import sys
import os

def disable_echo():
    '''Turn off echo in the terminal for the duration of the program'''

    filedesc = sys.stdin.fileno()
    if not os.isatty(filedesc):
        return

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
