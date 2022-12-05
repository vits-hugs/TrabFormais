import os
from ER_reader import ER_parser
from Automaton import Automaton,State


ESPECIAL_CARACTERS = ['?','*','+','o','|']
global id
id = 1
class Node:
    def __init__(self,type,node_left=None,node_right=None):
        global id
        self.type = type
        self.node_left = node_left
        self.node_right = node_right
        self.followpos = set()
        self.id = -1
        if type not in ESPECIAL_CARACTERS:
            self.id = id
            id+=1
    
    def show_leafs(self):
        if self.node_left == None and self.node_right == None:
            print(self)
        else:
            if self.node_left:
                self.node_left.show_leafs()
            if self.node_right:
                self.node_right.show_leafs()
    
    def get_leafs(self, leafs = []):
      
        if self.node_left == None and self.node_right == None:
            leafs.append(self)  
        else:
            if self.node_left:
                self.node_left.get_leafs(leafs)
            if self.node_right:
                self.node_right.get_leafs(leafs)
        return list(set(leafs))
    

    def tree_to_table(self):
        dic = dict()
        for leaf in self.get_leafs():
            dic[leaf.type+str(leaf.id)] = [i.id for i in list(leaf.followpos)]

        return dic

    def char_num(self):
        dic =dict()
        for i in tree.get_leafs():
            if i.type in dic.keys():
                dic[i.type].append(i.id)
            else:
                dic[i.type] = [i.id]
        return dic
    

    def __str__(self):
        if self.node_left == None and self.node_right == None:
            return f'{self.type}:{self.id} {[str(x.id) for x in self.followpos]}'

        return f'[{self.type}:{self.id}' + f' I left:{str(self.node_left)}' + f'I right:{str(self.node_right)}]'

    def nullable(self):
        if self.type == '|':
            return self.node_left.nullable() or self.node_right.nullable()
        elif self.type == 'o':
            return self.node_left.nullable() and self.node_right.nullable()
        elif self.type == '*':
            return True
        else:
            return False
    
    def firstpos(self):
        if self.type == '|':
            return self.node_left.firstpos().union(self.node_right.firstpos())
        elif self.type == 'o':
            if self.node_left.nullable():
                return self.node_left.firstpos().union(self.node_right.firstpos())
            else:
                return self.node_left.firstpos()
        elif self.type == '*':
            return self.node_left.firstpos()

        elif not self.nullable():
            return set([self])

    def lastpos(self):
        if self.type == '|':
            return self.node_left.firstpos().union(self.node_right.firstpos())
        elif self.type == 'o':
            if self.node_right.nullable():
                return self.node_left.firstpos().union(self.node_right.firstpos())
            else:
                return self.node_right.firstpos()
        elif self.type == '*':
            return self.node_left.firstpos()

        elif not self.nullable():
            return set([self])


    def calculateFollowpos(self):   
        if self.node_left:
           self.node_left.calculateFollowpos()
        if self.node_right:
           self.node_right.calculateFollowpos()
        if self.type == 'o':
            for node in self.node_left.lastpos():
                node.followpos = node.followpos.union(self.node_right.firstpos())

        if self.type == '*':
            for node in self.lastpos():
                node.followpos = node.followpos.union(self.firstpos())
    
     

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
            return Node(regex)
        
       
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

def to_name(set_of):

    list_nome = sorted([i.id for i in set_of])
    nome = ''.join(list(map(str,list_nome)))
    return nome

def make_union(char,S,char_to):
    ret = set()
    for i in S:
        for x in char_to[char] :
            if i == x:
                ret = ret.union(i)
    return ret

def is_in(U,automato,S):
    u = to_name(U)
    if u in automato.transition_table.keys():
        return True
    for i in S:
        if u == to_name(i):
            return True
    return False


def get_firtpos():

def tree_to_afd(tree,inputs):
    initial_state = to_name(tree.firstpos())
    
    automato = Automaton(initial_state,['a','b'])
    
    S = [tree.firstpos()]
  
    while len(S) > 0:
        S.pop()
        for i in automato.alfabet:
            U = make_union(i,S,tree.char_num())
            if not is_in(U,automato,S):
               S.append(U)
            automato.transition_table[to_name(U)] = (i,State(to_name(U)))
    return automato




if __name__ == '__main__':
    obj = ER_parser()
    obj.parseEr(os.path.join('ER','er_teste.txt'))

    automata_conv = ER_to_automata()

    for key in obj.definitions:
        tree = automata_conv.Er_to_tree(obj.definitions[key][::-1])
        tree = Node('o',tree,Node('#'))
        tree.calculateFollowpos()
        print('-'*30)
        table = tree.tree_to_table()
        tree.show_leafs()
        
        print(tree.char_num())
        auto = tree_to_afd(tree,['a,b'])
        print()
        print(auto.transition_table)