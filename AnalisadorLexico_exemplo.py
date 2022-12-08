from LexicalAnalyser.LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os

################################################################
## ANALISADOR LÉXICO
################################################################

# Escolha da ER e string de teste
file_id = 2
name_files = ['detecto_texto','exemplo_aula','exemplo_trabalho']

teste_string = [
                'A sou o Vitor tenho 19 anos, 173cm , nasci em 2022 , e gosto de escrever abaababbbbab em folhas A4',
                'abababbababba',
                'Sonim123 e blainim e 80'
                ]

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
