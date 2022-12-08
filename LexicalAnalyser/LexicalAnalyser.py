from LexicalAnalyser.ER_to_automata import ER_to_automata
from LexicalAnalyser.SymbolTable import SymbolTable
from LexicalAnalyser.PriorityTable import PriorityTable
from LexicalAnalyser.AutomataManager import AutomataManager
from LexicalAnalyser.AFD import AFD
from LexicalAnalyser.AFND import AFND
from LexicalAnalyser.Errors import CharNotInAlfabet, UnrecognizedToken
import LexicalAnalyser.config as config
import os

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
            if string[self.lexemeBegin] in config.WHITESPACES:
                self.lexemeBegin += 1
                continue

            tokenType, self.foward = self.automaton.getToken(string, self.lexemeBegin)
            lexeme = string[self.lexemeBegin:self.foward]
            if tokenType == None:
                raise UnrecognizedToken(lexeme, self.lexemeBegin, self.foward)

            tokenList.append((tokenType, lexeme))
            symbolTable.addEntry(lexeme, tokenType, lexeme, self.lexemeBegin, self.foward)
            self.lexemeBegin = self.foward

        return tokenList, symbolTable