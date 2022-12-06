import copy
from PriorityTable import PriorityTable
import sys

class State:
    def __init__(self, name, transitions=dict(), token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key):
        return self.transitions.get(key, tuple())

class Automaton:
    def __init__(self, initial_state_name: str | tuple[str], alfabet: list[str], transition_table: dict[str | tuple[str], State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table

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

    def e_closure(self, states: tuple[str] | str):
        if isinstance(states, tuple):
            stack = list(states)
            e_closure = set(states)
        else:
            stack = [states]
            e_closure = {states}

        while stack:
            t = stack.pop()
            if t in self.transition_table.keys():
                if 'epsilon' in self.transition_table[t].transitions.keys():
                    for u in self.transition_table[t]['epsilon']:
                        if u not in e_closure:
                            e_closure.add(u)
                            stack.append(u)

        e_closure_tuple = list(e_closure)
        e_closure_tuple.sort()
        e_closure_tuple = tuple(e_closure_tuple)
        return e_closure_tuple

    def move(self, states: tuple[str], char: str):
        reachable_states = set()
        if isinstance(states, tuple):
            for state in states:
                u_states = self.transition_table[state][char]
                reachable_states.update(u_states)
        else:
            u_states = self.transition_table[states][char]
            reachable_states.update(u_states)

        reachable_states_tuple = list(reachable_states)
        reachable_states_tuple.sort()
        reachable_states_tuple = tuple(reachable_states_tuple)
        return reachable_states_tuple

    def getDeterministic(self, priority_table: PriorityTable = None):
        initial_state_e_closure = self.e_closure(self.initial_state_name)
        new_AFD = Automaton(initial_state_e_closure, self.alfabet, {
                            initial_state_e_closure: State(initial_state_e_closure)})

        remaining_states = [initial_state_e_closure]
        while remaining_states:
            T = remaining_states.pop()
            for a in self.alfabet:
                U = self.e_closure(self.move(T, a))
                if U and U not in new_AFD.transition_table:
                    remaining_states.append(U)
                    new_AFD.transition_table[U] = State(U, {})
                new_AFD.transition_table[T].transitions[a] = U

        # Set tokens
        for state_name, state in new_AFD.transition_table.items():
            if isinstance(state_name, tuple):
                state_possible_tokens = []
                for u in state_name:
                    u_state = self.transition_table[u]
                    state_possible_tokens.append(u_state.token_type)

                if priority_table:
                    state.token_type = min(
                        state_possible_tokens, key=lambda x: priority_table[x])
                else:
                    for token_type in state_possible_tokens:
                        if token_type:
                            state.token_type = token_type
                            break

        return new_AFD

    def joinThroughEpsilon(self, automata: list):
        # Get a new transition table by merging all tables together
        automata.append(self)
        new_transition_table: dict[str | tuple[str], State] = {}
        for automaton in automata:
            new_transition_table = new_transition_table | automaton.transition_table

        # Get all epsilon transitions from the initial state
        initial_state_epsilon_transitions = []
        for automaton in automata:
            initial_state_epsilon_transitions.append(
                automaton.initial_state_name)
        initial_state_epsilon_transitions.sort()

        # Instantiate the initial_state
        initial_state_transitions = {
            'epsilon': tuple(initial_state_epsilon_transitions)}
        initial_state = State(
            'newNeverEverUsedStateName(Really no one would use this string as a name to a state. At least not a well intentioned person', initial_state_transitions, None)

        new_transition_table[initial_state.name] = initial_state
        new_automaton = Automaton(
            initial_state.name, self.alfabet, new_transition_table)

        return new_automaton

    def printAsAFD(self, file = sys.stdout):
        # Número de estados
        print(len(self.transition_table))

        # Estado inicial
        print(self.initial_state_name)

        # Estados finais
        end_states = []
        for _, state in self.transition_table.items():
            if state.token_type != None:
                end_states.append(state.name)
        for state in end_states[:-1]:
            print(state, end=',')
        print(end_states[-1])

        # Alfabeto
        for char in self.alfabet[:-1]:
            print(char, end=',')
        print(self.alfabet[-1])

        # Transições
        all_transitions = []
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions.append((key, char, dest_state))
        for transition in all_transitions:
            print(transition[0], transition[1], transition[2], sep=',')
    
    def printAsAFND(self, file = sys.stdout):
        # Número de estados
        print(len(self.transition_table))

        # Estado inicial
        print(self.initial_state_name)

        # Estados finais
        end_states = []
        for _, state in self.transition_table.items():
            if state.token_type != None:
                end_states.append(state.name)
        for state in end_states[:-1]:
            print(state, end=',')
        print(end_states[-1])

        # Alfabeto
        for char in self.alfabet[:-1]:
            print(char, end=',')
        print(self.alfabet[-1])

        # Transições
        all_transitions = []
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions.append((key, char, dest_state))
        for transition in all_transitions:
            print(transition[0], transition[1], sep=',', end=',')
            if isinstance(transition[2], tuple):
                for i in transition[2][:-1]:
                    print(i, end='-')
                print(transition[2][-1])

def test_joinThroughEpsilon():

    automaton_1 = Automaton('digit_q0', ['0', '1', '2'], {
        'digit_q0': State('digit_q0', {
            '0': ('digit_q0', 'digit_q2'),
            'epsilon': ('digit_q1', )
        }),
        'digit_q1': State('digit_q1', {
            '1': ('digit_q1', ),
            'epsilon': ('digit_q2', )
        }),
        'digit_q2': State('digit_q2', {
            '2': ('digit_q2', )
        }, ('OP', 'OP'))
    })

    automaton_2 = Automaton('id_q0', ['0', '1', '2'], {
        'id_q0': State('id_q0', {
            '0': ('id_q0', 'id_q2'),
            'epsilon': ('id_q1', )
        }),
        'id_q1': State('id_q1', {
            '1': ('id_q1', ),
            'epsilon': ('id_q2', )
        }),
        'id_q2': State('id_q2', {
            '2': ('id_q2', )
        }, ('OP', 'OP'))
    })

    automaton_3 = Automaton('letter_q0', ['0', '1', '2'], {
        'letter_q0': State('letter_q0', {
            '0': ('letter_q0', 'letter_q2'),
            'epsilon': ('letter_q1', )
        }),
        'letter_q1': State('letter_q1', {
            '1': ('letter_q1', ),
            'epsilon': ('letter_q2', )
        }),
        'letter_q2': State('letter_q2', {
            '2': ('letter_q2', )
        }, ('OP', 'OP'))
    })

    fuck_yeah = automaton_1.joinThroughEpsilon([automaton_2, automaton_3])

    automaton_1.printAsAFND()
    automaton_2.printAsAFND()
    automaton_3.printAsAFND()

    fuck_yeah.printAsAFD()

def test_getDeterministic():

    automaton_1 = Automaton('q0', ['0', '1', '2'], {
        'q0': State('q0', {
            '0': ('q0', 'q2'),
            'epsilon': ('q1', )
        }),
        'q1': State('q1', {
            '1': ('q1', ),
            'epsilon': ('q2', )
        }, ('OP', 'OP')),
        'q2': State('q2', {
            '2': ('q2', )
        })
    })

    automaton_2 = Automaton('q0', ['0', '1', '2'], {
        'q0': State('q0', {
            '0': ('q0', 'q2'),
            'epsilon': ('q1', )
        }, 'for'),
        'q1': State('q1', {
            '1': ('q1', ),
            'epsilon': ('q2', )
        }, 'OP'),
        'q2': State('q2', {
            '2': ('q2', )
        }, 'id')
    })


    automaton_1.printAsAFD()
    AFD_1 = automaton_1.getDeterministic()
    AFD_1.printAsAFD()

    automaton_2.printAsAFD()
    priority_table_1 = PriorityTable(['for', 'OP', 'id'])
    AFD_2 = automaton_2.getDeterministic(priority_table_1)
    AFD_2.printAsAFD()


if __name__ == '__main__':
    test_joinThroughEpsilon()
