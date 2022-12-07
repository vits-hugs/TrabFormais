import unittest
from AutomataManager import AutomataManager


class TestAutomaton(unittest.TestCase):

    def test_getStateName(self):
        state_set = {'2', '3', '1', '5'}
        state_name = AutomataManager.getStateName(state_set)
        self.assertEqual(state_name, '1235')


if __name__ == '__main__':
    unittest.main()