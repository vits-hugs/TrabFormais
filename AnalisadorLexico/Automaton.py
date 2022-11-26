class Automaton:
    class State:
        def __init__(self, name: str, transitions: dict(str, str), token_type: str):
            self.name = name
            self.transitions = transitions
            self.token_type = token_type

    def __init__(self, initial_state_name: str, transition_table: dict(str, State)):
        self.initial_state_name = initial_state_name
        self.transition_table = transition_table

    def readInput(self, chain: str):
        pass
