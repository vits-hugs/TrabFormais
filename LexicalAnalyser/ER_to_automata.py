from LexicalAnalyser.ER_reader import ER_parser
from LexicalAnalyser.PriorityTable import PriorityTable
from LexicalAnalyser.AFD import AFD, D_State
import string

ESPECIAL_CARACTERS = ['?', '*', '+', '.', '|']
global id
id = 1


class Node:
    def __init__(self, type, node_left=None, node_right=None):
        global id
        self.type = type
        self.node_left = node_left
        self.node_right = node_right
        self.followpos = set()
        self.id = -1
        if type not in ESPECIAL_CARACTERS:
            self.id = id
            id += 1

    def show_leafs(self):
        if self.node_left == None and self.node_right == None:
            print(self)
        else:
            if self.node_left:
                self.node_left.show_leafs()
            if self.node_right:
                self.node_right.show_leafs()

    def get_alphabet(self,alphabet=set()):
        if self.node_left == None and self.node_right == None:
            alphabet.add(self.type)
        else:
            if self.node_left:
                self.node_left.get_alphabet(alphabet)
            if self.node_right:
                self.node_right.get_alphabet(alphabet)
        return alphabet


    def get_leafs(self, leafs=[]):

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
        for leaf in self.get_leafs([]):
            dic[leaf.type+str(leaf.id)] = [i.id for i in list(leaf.followpos)]

        return dic

    def follow_pos_table(self):
        dic = dict()
        for leaf in self.get_leafs([]):
            dic[str(leaf.id)] = [i.id for i in list(leaf.followpos)]
        return dic
        # return {'1':[2],'2':[5],'3':[4],'4':[5],'5':[]}

    def accept_number(self):
        return max(node.id for node in self.get_leafs([]))

    def correspondence_table(self):
        dic = dict()
        for i in self.get_leafs([]):
            if i.type in dic:
                dic[i.type].append(i.id)
            else:
                dic[i.type] = [i.id]
        return dic

    def char_correspondence(self, char):
        dic = self.correspondence_table()
        if char not in dic:
            return []
        return dic[char]

    def __str__(self):
        if self.node_left == None and self.node_right == None:
            return f'{self.type}:{self.id} {[str(x.id) for x in self.followpos]}'

        return f'[({self.type}):{self.id}' + f'  left:{str(self.node_left)}' + f'I right:{str(self.node_right)}]'

    def nullable(self):
        if self.type == '|':
            return self.node_left.nullable() or self.node_right.nullable()
        elif self.type == '.':
            return self.node_left.nullable() and self.node_right.nullable()
        elif self.type == '+':
            return self.node_left.nullable() and self.node_right.nullable()
        elif self.type == '*':
            return True
        elif self.type == '?':
            return True
        else:
            return False

    def firstpos(self):
        if self.type == '|':
            return self.node_left.firstpos().union(self.node_right.firstpos())
        elif self.type == '.':
            if self.node_left.nullable():
                return self.node_left.firstpos().union(self.node_right.firstpos())
            else:
                return self.node_left.firstpos()
        elif self.type == '*':
            return self.node_left.firstpos()

        elif self.type == '+':
            return self.node_left.firstpos()

        elif self.type == '?':
            return self.node_left.firstpos()

        return set([self])

    def lastpos(self):
        if self.type == '|':
            return self.node_left.lastpos().union(self.node_right.lastpos())
        elif self.type == '.':
            if self.node_right.nullable():
                return self.node_left.lastpos().union(self.node_right.lastpos())
            else:
                return self.node_right.lastpos()
        elif self.type == '*':
            return self.node_left.lastpos()

        elif self.type == '+':
            return self.node_left.lastpos()

        elif self.type == '?':
            return self.node_left.lastpos()

        return set([self])

    def calculateFollowpos(self):
        if self.node_left:
            self.node_left.calculateFollowpos()
        if self.node_right:
            self.node_right.calculateFollowpos()
        if self.type == '.':
            for node in self.node_left.lastpos():
                node.followpos = node.followpos.union(self.node_right.firstpos())

        if self.type == '*':
            for node in self.lastpos():
                node.followpos = node.followpos.union(self.firstpos())

        if self.type == '+':
            for node in self.lastpos():
                node.followpos = node.followpos.union(self.firstpos())


class ER_to_Tree:
    def __init__(self):
        pass

    def search_char(self, regex, char: str):
        parenteses = 0
        for i in range(len(regex)):
            if regex[i] == ')':
                parenteses += 1
            if regex[i] == '(':
                parenteses -= 1
            if regex[i] == char and parenteses == 0:
                return i
        return -1

    def get_sides(self, pos, regex: str):
        left = regex[pos+1:]
        right = regex[:pos]
        return left, right

    def Er_to_tree(self, regex: str):
        regex = regex.strip()
        if len(regex) == 1:
            return Node(regex)

        if self.search_char(regex, '|') >= 0:
            l, r = self.get_sides(self.search_char(regex, '|'), regex)
            return Node('|', self.Er_to_tree(l), self.Er_to_tree(r))

        if self.search_char(regex, '.') >= 0:
            l, r = self.get_sides(self.search_char(regex, '.'), regex)
            return Node('.', self.Er_to_tree(l), self.Er_to_tree(r))

        if self.search_char(regex, '*') >= 0:
            l, r = self.get_sides(self.search_char(regex, '*'), regex)
            return Node('*', self.Er_to_tree(l))

        if self.search_char(regex, '+') >= 0:
            l, r = self.get_sides(self.search_char(regex, '+'), regex)
            return Node('+', self.Er_to_tree(l))

        if self.search_char(regex, '?') >= 0:
            l, r = self.get_sides(self.search_char(regex, '?'), regex)
            return Node('?', self.Er_to_tree(l))

        if regex[0] == ')' and regex[-1] == '(':
            return self.Er_to_tree(regex[1:-1])


class ER_to_automata:

    def is_in(self, U, automato, S):
        u = self.int_arr_to_name(U)
        if u in automato.transition_table:
            return True
        for i in S:
            if u == ''.join(list(map(str, sorted(i)))):
                return True
        return False

    def get_firtpos_int_array(self, firs_pos):
        i_array = []
        for i in firs_pos:
            i_array.append(i.id)
        return i_array

    def make_union(self, S, tree: Node, char):  # Uni??o do followpos dos estados em S, que est??o em a
        correspondenc_table = tree.char_correspondence(char)
        follow_pos_table = tree.follow_pos_table()
        U = set()
        for p in S:
            if p in correspondenc_table:
                U = U.union(follow_pos_table[str(p)])
        return U

    def array_to_state_name(self, array):
        list_nome = sorted(array)
        nome_id = '-'.join(list(map(str, list_nome)))
        if nome_id not in self.conf_estados:
            self.conf_estados[nome_id] = self.token+'_'+str(self.state_id)
            self.state_id += 1
        return self.conf_estados[nome_id]

    def is_in_Dstates(self, U_name, Dstates, usedDstates):
        for l_array in Dstates:
            if U_name == self.array_to_state_name(l_array):
                return True
        for l_array in usedDstates:
            if U_name == self.array_to_state_name(l_array):
                return True
        return False

    def tree_to_afd(self, tree: Node, token):
        initial_state = self.array_to_state_name(self.get_firtpos_int_array(tree.firstpos()))
        alphabet = tree.get_alphabet(set())
        alphabet.remove('#')
        automato = AFD(initial_state, alphabet, {})
        Dstates = [self.get_firtpos_int_array(tree.firstpos())]
        usedDstates = []
        while len(Dstates) > 0:
            S = Dstates.pop()
            usedDstates.append(S)

            for char in alphabet:
                U = self.make_union(S, tree, char)
                if U:
                    U_name = self.array_to_state_name(list(U))
                    if not self.is_in_Dstates(U_name, Dstates, usedDstates):
                        Dstates.append(U)
                    #print(f'{self.array_to_state_name(S)},{char}-> {U_name}')
                    # adiciona transi????o [S,a] -> U
                    estado_name = self.array_to_state_name(S)
                    if estado_name in automato.transition_table:
                        automato.transition_table[estado_name].transitions[char] = U_name
                    else:
                        if tree.accept_number() in S:
                            automato.transition_table[estado_name] = D_State(estado_name, {char: U_name}, token)
                        else:
                            automato.transition_table[estado_name] = D_State(estado_name, {char: U_name})
                    if U_name not in automato.transition_table:
                        if tree.accept_number() in U:
                            automato.transition_table[U_name] = D_State(U_name, {}, token)

        return automato

    def get_automato(self, obj, token, alphabet=list(string.ascii_lowercase)):
        automata_conv = ER_to_Tree()
        obj.definitions # ver se regex faz sentido
        tree = automata_conv.Er_to_tree(obj.definitions[token][::-1])
        tree = Node('.', tree, Node('#'))
        # print(tree)
        tree.calculateFollowpos()
        return self.tree_to_afd(tree,token)

    def getAutomata_fromFile(self, file):
        global id
        parser = ER_parser()
        parser.parseEr_fromFile(file)
        automato_List: list[AFD] = []
        for token in parser.definitions:
            id = 1
            self.conf_estados = dict()
            self.state_id = 0
            self.token = token
            automato_List.append(self.get_automato(parser, token))
        return automato_List, PriorityTable(parser.priority)

    def getAutomata(self, string):
        global id
        parser = ER_parser()
        parser.parseEr_fromString(string)
        automato_List: list[AFD] = []
        for token in parser.definitions:
            id = 1
            self.conf_estados = dict()
            self.state_id = 0
            self.token = token
            automato_List.append(self.get_automato(parser, token))
        return automato_List, PriorityTable(parser.priority)
