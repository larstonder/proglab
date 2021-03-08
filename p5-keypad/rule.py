'''Rule module'''

class Rule:
    '''Rule class'''
    signal = signal_is_digit

def signal_is_digit(signal):
    return 48 <= ord(signal) <= 57