from LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os

LA = LexicalAnalyserGenerator.getLexicalAnalyser(os.path.join('ER', 'er_1.txt'))

tokens, symbolList = LA.exec("abc blm abbblm cd d")

print("Tokens: ", tokens)

print("SymbolList")
symbolList.print()
