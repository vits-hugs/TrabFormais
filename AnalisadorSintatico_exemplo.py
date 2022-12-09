from LexicalAnalyser.LexicalAnalyserGenerator import LexicalAnalyserGenerator
from SyntacticalAnalyser.ContextFreeGrammar import ContextFreeGrammar
from SyntacticalAnalyser.LRParser import LRParser
from SyntacticalAnalyser.GrammarReader import GrammarReader

import os

################################################################
## ANALISADOR LÉXICO
################################################################

# Escolha da ER e string de teste
file_id = 3
name_files = ['detecto_texto','exemplo_aula','exemplo_trabalho', 'er.txt']

teste_string = ['A sou o Vitor tenho 19 anos, 173cm , nasci em 2022 , e gosto de escrever abaababbbbab em folhas A4',
                'abababbababba',
                'coisa2 a 2 aa23', 'er.txt']

ERs_file = open(os.path.join('ER', name_files[file_id]+'.txt'))
REs = ERs_file.read()
print("Expressões regulares: \n", REs, sep='')
ERs_file.close()

# Geração do analisador léxico
LA = LexicalAnalyserGenerator.getLexicalAnalyser(REs)

# Uso do analisador
tokens, symbolList = LA.exec(teste_string[file_id])

print("Tokens: ")
for token in tokens:
    print(token)
print()
print("SymbolList")
symbolList.print()

################################################################
## ANALISADOR SINTÁTICO
################################################################
'''
reader = GrammarReader()
grammar = reader.grammarfromFile('gram.txt',{'id','pastel'})
grammar.initialize()

parser = LRParser(grammar)

parsing_result = parser.parse(tokens)

print("input valid: {}".format(parsing_result))
parser.printParsingTable()
parser.printHistory()
'''
