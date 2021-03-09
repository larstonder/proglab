"""Finite State Machine"""

class FSM:
    """Class for finite state machines"""

    def __init__(self, start_state, end_states, agent):
        self.rules = []
        self.start_state = start_state
        self.end_states = end_states
        self.agent = agent

    def add_rule(self, rule):
        """Add a rule to the FSM"""
        self.rules.append(rule)

    def get_next_signal(self):
        """Query the agent for the next signal"""
        return self.agent.get_signal()

    def run(self):
        """Runs the FSM until reaching the end state"""
        state = self.start_state
        while state not in self.end_states:
            signal = self.get_next_signal()

            for rule in self.rules:
                if rule.match(state, signal):
                    state = rule.fire(self.agent)
                    break
