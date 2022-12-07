from LexicalAnalyserGenerator import LexicalAnalyserGenerator
import os

files = ['er_1','er_pteste','er_teste','parser_texto']
lista = ['a 3 gatos comeram minha folha A4',
        ' a  a aa aaaa aaaaaaaaaaaa',
        'abababc cd ablm alm c d  ',
        'eu sou Enzo tenho 10cm e 180cm de altura , nasci em  2022 , sou amigo do Vitor e sim A4 e uma palavra abbababababababababbabaabb']
for name_file in files:
    file = open(os.path.join('ER', name_file + '.txt'))
    string = file.read()
    file.close()
    print(name_file)
    LA = LexicalAnalyserGenerator.getLexicalAnalyser(string)

    tokens, symbolList = LA.exec(lista.pop(0))
    print("SymbolList")
    symbolList.print()
    print()
    print('-'*30)
    print()

#print("Tokens: ", tokens)

