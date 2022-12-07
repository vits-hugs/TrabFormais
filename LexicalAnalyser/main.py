from LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os


# # LA = LexicalAnalyserGenerator.getLexicalAnalyser(os.path.join('..', 'ER', 'Teste_all_cases.txt'))
# LA = LexicalAnalyserGenerator.getLexicalAnalyser(os.path.join('ER', 'er_1.txt'))

# tokens, symbolList = LA.exec("sonim a blainim 7 sonim23")

file = open(os.path.join('ER', 'er_1.txt'))
string = file.read()
print(string)
file.close()
LA = LexicalAnalyserGenerator.getLexicalAnalyser(string)

tokens, symbolList = LA.exec("a dk cu bosta mijo 1 mijo2")

print("Tokens: ", tokens)

print("SymbolList")
symbolList.print()
