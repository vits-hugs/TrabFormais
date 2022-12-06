import unittest
from Automaton import Automaton, State


class TestAutomaton(unittest.TestCase):

    def test_e_closure(self):

        transition_table = {
            'q0': State('q0', {
                '0': ('q0', 'q2'),
                'epsilon': ('q1', )
            }),
            'q1': State('q1', {
                '1': ('q1', ),
                'epsilon': ('q2', )
            }),
            'q2': State('q2', {
                '2': ('q2', )
            }, ('OP', 'OP'))
        }

        automaton = Automaton('q0', ['0', '1', '2'] ,transition_table)

        q1_and_q2_e_closure = automaton.e_closure(('q1', 'q2'))
        expectedOutput = ('q1', 'q2')

        self.assertTupleEqual(q1_and_q2_e_closure, expectedOutput)

    def test_move(self):

        transition_table = {
            'q0': State('q0', {
                '0': ('q0', 'q2'),
                'epsilon': ('q1', )
            }),
            'q1': State('q1', {
                '1': ('q1', ),
                'epsilon': ('q2', )
            }),
            'q2': State('q2', {
                '2': ('q2', )
            }, ('OP', 'OP'))
        }

        automaton = Automaton('q0', ['0', '1', '2'] ,transition_table)

        reachable_states = automaton.move(('q1', 'q2'), '1')
        expectedOutput = ('q1', )

        self.assertTupleEqual(reachable_states, expectedOutput)

        reachable_states = automaton.move('q2', '2')
        expectedOutput = ('q2', )

        self.assertTupleEqual(reachable_states, expectedOutput)

    def test_getDeterministic(self):

        transition_table = {
            'q0': State('q0', {
                '0': ('q0', 'q2'),
                'epsilon': ('q1', )
            }),
            'q1': State('q1', {
                '1': ('q1', ),
                'epsilon': ('q2', )
            }),
            'q2': State('q2', {
                '2': ('q2', )
            }, ('OP', 'OP'))
        }

        automaton = Automaton('q0', ['0', '1', '2'] ,transition_table)
        automaton.printAsAFD()
        AFD = automaton.getDeterministic()
        AFD.printAsAFD()


if __name__ == '__main__':
    unittest.main()