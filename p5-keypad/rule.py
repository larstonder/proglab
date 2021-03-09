"""Rule module"""

from inspect import isfunction


def match(matcher, value):
    """Checks if the value matches the matcher, matcher can be a function"""
    if isfunction(matcher):
        return matcher(value)
    return value == matcher


class Rule:
    """Rule class"""
    def __init__(self, state1, state2, signal, action):
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action

    def match(self, current_state, current_signal):
        """Returns true if the rule matches with the current state if applicable"""
        return match(self.state1, current_state) and match(self.signal, current_signal)


def signal_is_digit(signal):
    """Just checking if a signal is a digit or not"""
    return ord('0') <= ord(signal) <= ord('9')
