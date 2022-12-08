from LexicalAnalyser.Errors import CharNotInAlfabet
import LexicalAnalyser.config as config


class D_State:
    def __init__(self, name: str, transitions: dict[str, str] = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key):
        return self.transitions.get(key, None)

class AFD:
    def __init__(self, initial_state_name: str, alfabet: set[str], transition_table: dict[str, D_State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table

    def getToken(self, string, begin: int):
        reading_index = begin
        foward = begin
        token = None
        current_state_name = self.initial_state_name
        while current_state_name:

            current_state = self.transition_table[current_state_name]
            if current_state.token_type != None:
                foward = reading_index
                token = current_state.token_type

            if reading_index >= len(string):
                foward = reading_index + 1
                break

            char = string[reading_index]
            if char not in self.alfabet and char not in config.WHITESPACES:
                raise CharNotInAlfabet(char)
            current_state_name = self.transition_table[current_state_name][char]
            reading_index += 1

        if foward == begin: foward += 1
        return token, foward

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
            print(transition[0], transition[1], transition[2], sep=',')
            