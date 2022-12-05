import os
from ER_reader import ER_parser
from Automaton import Automaton,State

ESPECIAL_CARACTERS = ['?','*','+']
class Node:
    def __init__(self,type,node_right=None,node_left=None):
        self.type = type
        self.node_1 = node_right
        self.node_2 = node_left
        


class ER_to_automata:


    def __init__(self):
        pass

    
    def reg_to(self,regex : str):
        pass

            

if __name__ == '__main__':
    obj = ER_parser()

    obj.parseEr(os.path.join('ER','er_teste.txt'))

    automata_conv = ER_to_automata()
    for key in obj.definitions:
        automaton = automata_conv.reg_to_tree(obj.definitions[key])
       

    