from Automaton import Automaton, State
from SymbolTable import SymbolTable, SymbolTableEntry

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

def test_exec():
    AFD = Automaton((0, ), ['<', '=', '>'], {
        (0, ): State((0, ), {
            '<': (1, ),
            '=': (5, ),
            '>': (6, )
        }),

        (1, ): State((1, ), {
            '=': (2, ),
            '>': (3, )
        }, 'LT'),

        (2, ): State((2, ), {

        }, 'LE'),

        (3, ): State((3, ), {

        }, 'NE'),

        (5, ): State((5, ), {

        }, 'EQ'),

        (6, ): State((6, ), {
            '=': (7, ),
        }, 'GT'),

        (7, ): State((7 ), {

        }, 'GE'),
    })


    LA = LexicalAnalyser(AFD)

    tokenList, st = LA.exec('= <= >= < = >')

    print(tokenList)

    st.print()

if __name__ == '__main__':
    test_exec()