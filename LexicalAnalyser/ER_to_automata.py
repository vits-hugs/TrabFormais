import os
from ER_reader import ER_parser
from Automaton import Automaton,State


ESPECIAL_CARACTERS = ['?','*','+']
class Node:
    def __init__(self,type,node_left=None,node_right=None):
        self.type = type
        self.node_left = node_left
        self.node_right = node_right
        
    def __str__(self):
        return f'[({self.type})' + f'left:{str(self.node_left)}' + f'I right:{str(self.node_right)}]'



class ER_to_automata:


    def __init__(self):
        pass

    def search_char(self,regex,char :str):
        parenteses = 0
        for i in range(len(regex)):
            if regex[i] == ')':
                parenteses+=1
            if regex[i] == '(':
                parenteses-=1
            if regex[i] == char and parenteses == 0:
                return i
        return -1


    def get_sides(self,pos,regex : str):
        left = regex[pos+1:]
        right = regex[:pos]
        return left,right        

    def Er_to_tree(self,regex : str):
        #print(regex)
        regex = regex.strip()
        if len(regex) == 1:
            return regex
        
       
        if self.search_char(regex,'|') >= 0:
            l,r = self.get_sides(self.search_char(regex,'|'),regex)
            return Node('|',self.Er_to_tree(l),self.Er_to_tree(r))
        
        if self.search_char(regex,'.') >= 0:
            l,r = self.get_sides(self.search_char(regex,'.'),regex)
            return Node('o',self.Er_to_tree(l),self.Er_to_tree(r))

        if self.search_char(regex,'*')>= 0:
            l,r = self.get_sides(self.search_char(regex,'*'),regex)
            return Node('*',self.Er_to_tree(l))


        if regex[0] == ')' and regex[-1] == '(':
            return self.Er_to_tree(regex[1:-1])   




if __name__ == '__main__':
    obj = ER_parser()

    obj.parseEr(os.path.join('ER','er_teste.txt'))

    automata_conv = ER_to_automata()

    for key in obj.definitions:
        tree = print(automata_conv.Er_to_tree(obj.definitions[key][::-1]))
        tree = Node('o',tree,'#')
        print('-'*30)

    