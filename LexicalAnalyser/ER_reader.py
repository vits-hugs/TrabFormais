import os
from Automaton import Automaton


class ER_parser:

    def __init__(self) -> None:
        self.definitions = dict()
        self.priority = []
    def parseEr(self,file):

        file = open(file,'r')
        Lines = file.readlines()
        file.close()

        for line in Lines:
            line = line.replace('\n','')
            if line != "":
                definition = line.split(":")
                self.priority.append(definition[0])
        
                self.definitions[definition[0]] = definition[1]
    
    def get_inner_parent(self,regex):
        pilha = []
        start = 0
        fim = len(regex)
        for i in range(len(regex)):
            if regex[i]=='(':
                start = i+1
            if regex[i]==')':
                fim = i
                break
        
        
        regex = regex[start:fim]
        return regex,start-1,fim+1


if __name__ == '__main__':
    obj = ER_parser()

    obj.parseEr(os.path.join('ER','er_teste.txt'))
    #obj.definitions_to_automata()