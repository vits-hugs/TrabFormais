import os
import ContextFreeGrammar

class GramarReader:

    def __init__(self):
        pass

    def get_production_list(self,production:str,tokens:set):
        production_list = []
        number = 0
        while number < len(production):
            for token in tokens:
                if token in production:
                    temp = 0
                    for i in token:
                        if (number+temp) < len(production) and i == production[number+temp]:
                            temp+=1
                    if temp == len(token):
                        production_list.append(production[number:number+temp])
                        number+=temp
            if number < len(production):
                production_list.append(production[number])
            number+=1
        return production_list

    def grammarfromFile(self,file,tokens):
        file = open(os.path.join('Grammar',file))
        grammar_text =  file.readlines()
        file.close()
        lista_trans = []
        non_terminal = set()
        alphabet = set()
        for line_index in range(len(grammar_text)):
            linha = grammar_text[line_index].replace('\n','')
            linha = linha.replace(' ','').split('->')
            if line_index == 0:
                initial_symbol = linha[0]
            for production in linha[1].split('|'):
                production_list = self.get_production_list(production,tokens)
                lista_trans.append((linha[0],production_list))
                non_terminal.add(linha[0])
                [alphabet.add(i) for i in production_list]
        
        gramar = ContextFreeGrammar(alphabet.difference(non_terminal),initial_symbol,non_terminal)
        for lista in lista_trans:
            gramar.addProduction(lista[0],lista[1])
            #print(lista[0],lista[1])
        return gramar
if __name__ == '__main__':
    reader = GrammarReader()
    grammar = reader.grammarfromFile('gram.txt',{'id','pastel'})
    print(grammar.alphabet)
    print(grammar.initial_symbol)
    print(grammar.non_terminals)