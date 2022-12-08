from LexicalAnalyserGenerator import LexicalAnalyserGenerator
from Grammar_reader import Gramar_reader
import os


name_file = 'er_teste.txt'
file = open(os.path.join('ER', name_file))
string = file.read()
file.close()

LA,toke_types = LexicalAnalyserGenerator.getLexicalAnalyser(string)
tokens, symbolList = LA.exec("") #executa o analisador lexico sobre string
print('Tokens',toke_types)

gramar = Gramar_reader().grammarfromFile('gram.txt',toke_types)
print('GRAMAR')
print(gramar.alphabet)
print(gramar.initial_symbol)
print(gramar.non_terminals)
print("SymbolList")
symbolList.print()
print()
print('-'*30)
print()

#print("Tokens: ", tokens)

