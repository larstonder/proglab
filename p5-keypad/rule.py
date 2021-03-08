"""Rule module"""


class Rule:
    """Rule class"""
    signal = signal_is_digit


def signal_is_digit(signal):
    """Just checking if a signal is a digit or not"""
    return 48 <= ord(signal) <= 57