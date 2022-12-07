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
    def __init__(self, initial_state_name: str, alfabet: set[str], transition_table: dict[str, N_State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table

    def print(self):
        for state_name, state in self.transition_table.items():
            print(str(state_name).ljust(20), end=' ')
            print("Transitions: ", str(state.transitions).ljust(70), end=' ')
            print("Token: ", state.token_type)
        print()

    def print(self):
        # Número de estados
        print(len(self.transition_table))

        # Estado inicial
        print(self.initial_state_name)

        # Estados finais
        end_states = []
        for _, state in self.transition_table.items():
            if state.token_type != None:
                end_states.append(state.name)
        print(','.join(end_states))

        # Alfabeto
        print(','.join(self.alfabet))

        # Transições
        all_transitions = []
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions.append((key, char, dest_state))
        for transition in all_transitions:
            print(transition[0], transition[1], sep=',', end=',')
            print('-'.join(transition[2]))
