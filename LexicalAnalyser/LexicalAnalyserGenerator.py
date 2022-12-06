from ER_to_automata import ER_to_automata
from Automaton import Automaton, State
from SymbolTable import SymbolTable, SymbolTableEntry
from PriorityTable import PriorityTable

WHITESPACES = {'\n', ' ', '\t'}

class LexicalAnalyser():
    def __init__(self, automaton: Automaton):
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
    def getLexicalAnalyser(ERs):
        automata, priority_table = ER_to_automata().getAutomata(ERs)
        automata: list[Automaton]
        priority_table: PriorityTable

        automata_1 = automata.pop(0)
        complete_AFND = automata_1.joinThroughEpsilon(automata)
        complete_AFD = complete_AFND.getDeterministic(priority_table)

        return LexicalAnalyser(complete_AFD)

if __name__ == '__main__':
    algo = LexicalAnalyserGenerator().getLexicalAnalyser('ER/er_teste.txt')