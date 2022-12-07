import copy
from PriorityTable import PriorityTable
import sys


class D_State:
    def __init__(self, name: str, transitions: dict[str, str] = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key):
        return self.transitions.get(key, tuple())



class AFD:
    def __init__(self, initial_state_name: str, alfabet: list[str], transition_table: dict[str, D_State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table


    def print(self):
        for state_name, state in self.transition_table.items():
            print(str(state_name).ljust(20), end=' ')
            print("Transitions: ", str(state.transitions).ljust(70), end=' ')
            print("Token: ", state.token_type)
        print()

    def getToken(self, string, begin: int):
        foward = begin
        token = None
        current_state_name = self.initial_state_name
        while current_state_name != ():

            current_state = self.transition_table[current_state_name]
            if current_state.token_type != None:
                token = current_state.token_type

            if foward >= len(string):
                foward += 1
                break

            current_state_name = self.transition_table[current_state_name][string[foward]]
            foward += 1

        return token, foward - 1