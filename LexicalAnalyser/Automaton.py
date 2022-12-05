class State:
    def __init__(self, name, transitions = dict(), token: tuple[str, str] = None):
        self.name = name
        self.transitions = transitions
        self.token = token
    
    def __getitem__(self, key):
        return self.transitions.get(key, tuple())

class Automaton:
    def __init__(self, initial_state_name: str | tuple[str], alfabet: list[str], transition_table: dict[str | tuple[str], State] = {}):
        self.initial_state_name = initial_state_name
        self.alfabet = alfabet
        self.transition_table = transition_table

    def e_closure(self, states: tuple[str] | str):
        if isinstance(states, tuple):
            stack = list(states)
            e_closure = set(states)
        else:
            stack = [states]
            e_closure = {states}

        while stack:
            t = stack.pop()

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

    def getDeterministic(self):
        initial_state_e_closure = self.e_closure(self.initial_state_name)
        new_AFD = Automaton(initial_state_e_closure, self.alfabet, {initial_state_e_closure: State(initial_state_e_closure)})

        remaining_states = [initial_state_e_closure]
        while remaining_states:
            T = remaining_states.pop()
            for a in self.alfabet:
                U = self.e_closure(self.move(T, a))
                if U and U not in new_AFD.transition_table:
                    remaining_states.append(U)
                    new_AFD.transition_table[U] = State(U, {})
                new_AFD.transition_table[T].transitions[a] = U

        return new_AFD

    def print(self):
        for state_name, state in self.transition_table.items():
            print(str(state_name).ljust(20), end=' ')
            print("Transitions: ", str(state.transitions).ljust(70), end=' ')
            print("Token: ", state.token)
        print()
