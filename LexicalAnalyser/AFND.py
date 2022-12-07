import copy
from PriorityTable import PriorityTable
import sys


class N_State:
    def __init__(self, name: str, transitions: dict[str, set] = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key: str):
        return self.transitions.get(key, set())


class AFND:
    def __init__(self, initial_state_name: str, alfabet: list[str], transition_table: dict[str, N_State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table

    def print(self):
        for state_name, state in self.transition_table.items():
            print(str(state_name).ljust(20), end=' ')
            print("Transitions: ", str(state.transitions).ljust(70), end=' ')
            print("Token: ", state.token_type)
        print()