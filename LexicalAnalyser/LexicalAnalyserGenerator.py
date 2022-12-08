from LexicalAnalyser.ER_to_automata import ER_to_automata
from LexicalAnalyser.SymbolTable import SymbolTable
from LexicalAnalyser.PriorityTable import PriorityTable
from LexicalAnalyser.AutomataManager import AutomataManager
from LexicalAnalyser.AFD import AFD
from LexicalAnalyser.AFND import AFND
from LexicalAnalyser.LexicalAnalyser import LexicalAnalyser
from LexicalAnalyser.Errors import CharNotInAlfabet, UnrecognizedToken
import LexicalAnalyser.config as config
import os

class LexicalAnalyserGenerator:

    @staticmethod
    def getLexicalAnalyser(string):
        automata, priority_table = ER_to_automata().getAutomata(string)

        print("Automatos gerados a partir das ERs: ")
        for AFD in automata:
            AFD.print()
            print()

        for index, afd in enumerate(automata):
            automata[index] = AutomataManager.getNondeterministic(afd)

        complete_AFND = AutomataManager.joinThroughEpsilon(automata)

        print("AFND da união por epsilon: ")
        complete_AFND.print()
        print()

        complete_AFD = AutomataManager.getDeterministic(complete_AFND, priority_table)

        print("AFD completo, determinizado: ")
        complete_AFD.print()
        print()

        return LexicalAnalyser(complete_AFD)
