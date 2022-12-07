from dataclasses import dataclass

@dataclass
class SymbolTableEntry:
    token_type: str
    lexeme: str
    lexemeBegin: int
    lexemeEnd: int

class SymbolTable:

    def __init__(self):
        self.table: dict[str, SymbolTableEntry] = {}

    def __getitem__(self, key):
        return self.table[key]

    def addEntry(self, key, token_type, lexeme, lexemeBegin, lexemeEnd):
        self.table[key] = SymbolTableEntry(token_type, lexeme, lexemeBegin, lexemeEnd)

    def print(self):
        for key, value in self.table.items():
            print(key.ljust(10), '|', "token_type:", str(value.token_type).ljust(10), 'lexeme:', str(value.lexeme).ljust(10), 'lexemeBegin:', str(value.lexemeBegin).ljust(10), 'lexemeEnd:', str(value.lexemeEnd))