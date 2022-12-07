from LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os

ERs_file = open(os.path.join('ER', 'er_1.txt'))
REs = ERs_file.read()
print("Expressões regulares: \n", REs, sep='')
ERs_file.close()

LA = LexicalAnalyserGenerator.getLexicalAnalyser(REs)

tokens, symbolList = LA.exec("Sonim Blainim123 425 s sinim")

print("Tokens: ")
for token in tokens:
    print(token)
print()
print("SymbolList")
symbolList.print()
