from LexicalAnalyser.AFD import AFD, D_State
from LexicalAnalyser.AFND import AFND, N_State
from LexicalAnalyser.PriorityTable import PriorityTable
from copy import copy


class AutomataManager:
    
    @staticmethod
    def e_closure(states: set[str], transition_table: dict[str, N_State]):
        stack = list(states)
        e_closure = copy(states)
        while stack:
            t = stack.pop()

            for u in transition_table[t]['&']:
                if u not in e_closure:
                    e_closure.add(u)
                    stack.append(u)
        
        return e_closure

    @staticmethod
    def move(states: set[str], char: str, transition_table: dict[str, N_State]):
        reachable_states: set[str] = set()
        for state in states:
            u_states = transition_table[state][char]
            reachable_states.update(u_states)
        
        return reachable_states
            
    @staticmethod
    def getStateName(state_set: set[str]):
        state_set_list = list(state_set)
        state_set_list.sort()

        state_set_name = ''
        for state in state_set_list:
            state_set_name += state
        return state_set_name

    @staticmethod
    def getDeterministic(afnd: AFND, priority_table: PriorityTable):
        state_group_table: dict[str, set[str]] = {}
        for state in afnd.transition_table.keys():
            state_group_table[state] = {state}

        initial_state_e_closure = AutomataManager.e_closure(state_group_table[afnd.initial_state_name], afnd.transition_table)
        initial_state_name = AutomataManager.getStateName(initial_state_e_closure)
        if initial_state_name not in state_group_table:
            state_group_table[initial_state_name] = initial_state_e_closure

        new_AFD = AFD(initial_state_name, afnd.alfabet, {initial_state_name: D_State(initial_state_name)})

        remaining_states = [initial_state_name]
        while remaining_states:
            T_name = remaining_states.pop()
            for a in new_AFD.alfabet:
                T_group = state_group_table[T_name]
                U_set = AutomataManager.e_closure(AutomataManager.move(T_group, a, afnd.transition_table), afnd.transition_table)
                if not U_set:
                    continue
                U = AutomataManager.getStateName(U_set)
                
                # The translation table is also being used to know if a state has been seen before
                if U not in new_AFD.transition_table:
                    remaining_states.append(U)
                    new_AFD.transition_table[U] = D_State(U, {})

                    state_group_table[U] = U_set

                new_AFD.transition_table[T_name].transitions[a] = U

        # Set tokens
        for state_name, state in new_AFD.transition_table.items():
            state_group = state_group_table[state_name]

            state_possible_tokens = []
            for u in state_group:
                u_state = afnd.transition_table[u]
                state_possible_tokens.append(u_state.token_type)

            if priority_table:
                state.token_type = min(
                    state_possible_tokens, key=lambda x: priority_table[x])

        return new_AFD

    @staticmethod
    def getNondeterministic(afd: AFD):
        new_AFD = AFND(afd.initial_state_name, afd.alfabet, afd.transition_table)

        for key, state in new_AFD.transition_table.items():
            new_AFD.transition_table[key] = N_State(state.name, state.transitions, state.token_type)
            for char, dest_state in state.transitions.items():
                state.transitions[char] = {dest_state}

        return new_AFD

    @staticmethod
    def joinThroughEpsilon(automata: list[AFD]):
        new_alfabet = set()
        for afd in automata:
            new_alfabet.update(afd.alfabet)

        new_transition_table: dict[str, N_State] = {}
        for automaton in automata:
            new_transition_table = new_transition_table | automaton.transition_table

        # Get list of initial states names
        initial_states: set[str] = set()
        for automaton in automata:
            initial_states.add(automaton.initial_state_name)

        # Instantiate the initial_state
        initial_state_transitions = {
            '&': initial_states
        }
        initial_state = N_State('Initial_State', initial_state_transitions, None)

        new_transition_table[initial_state.name] = initial_state
        new_automaton = AFND(initial_state.name, new_alfabet, new_transition_table)

        return new_automaton
