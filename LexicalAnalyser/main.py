from LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os

file = open(os.path.join('ER', 'er_1.txt'))
string = file.read()
print(string)
file.close()
LA = LexicalAnalyserGenerator.getLexicalAnalyser(string)

tokens, symbolList = LA.exec("a dk cu bosta mijo 1 mijo2")

print("Tokens: ", tokens)

print("SymbolList")
symbolList.print()
