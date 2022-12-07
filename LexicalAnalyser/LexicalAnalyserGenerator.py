from ER_to_automata import ER_to_automata
from SymbolTable import SymbolTable
from PriorityTable import PriorityTable
from AutomataManager import AutomataManager
from AFD import AFD
from AFND import AFND
import os

WHITESPACES = {'\n', ' ', '\t'}

class LexicalAnalyser():
    def __init__(self, automaton: AFD):
        self.automaton = automaton
        self.lexemeBegin = 0
        self.foward = 0
    
    def reset(self):
        self.lexemeBegin = 0
        self.foward = 0

    def exec(self, string: str):
        self.reset()

        tokenList = []
        symbolTable = SymbolTable()

        while self.lexemeBegin < len(string):
            if string[self.lexemeBegin] in WHITESPACES:
                self.lexemeBegin += 1
                continue

            tokenType, self.foward = self.automaton.getToken(string, self.lexemeBegin)
            lexeme = string[self.lexemeBegin:self.foward]

            tokenList.append((tokenType, lexeme))
            symbolTable.addEntry(lexeme, tokenType, lexeme, self.lexemeBegin, self.foward)
            self.lexemeBegin = self.foward

        return tokenList, symbolTable

class LexicalAnalyserGenerator:
    
    @staticmethod
    def getLexicalAnalyser(path_to_ER_file):
        automata, priority_table = ER_to_automata().getAutomata(path_to_ER_file)

        print("Fresquinhos")
        for AFD in automata:
            AFD.print()

        for index, afd in enumerate(automata):
            automata[index] = AutomataManager.getNondeterministic(afd)

        print("AFNDzados")
        for AFD in automata:
            AFD.print()

        complete_AFND = AutomataManager.joinThroughEpsilon(automata)

        print("AFND completo após união")
        complete_AFND.print()

        complete_AFD = AutomataManager.getDeterministic(complete_AFND, priority_table)

        print("AFD completo, determinizado")
        complete_AFND.print()

        return LexicalAnalyser(complete_AFD)

if __name__ == '__main__':
    
    algo = LexicalAnalyserGenerator().getLexicalAnalyser('ER/er_teste.txt')