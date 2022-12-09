from SyntacticalAnalyser.ContextFreeGrammar import ContextFreeGrammar

class LRParser:
    grammar: ContextFreeGrammar
    canonical_collection: list #[(state, dot_pos)]
    inital_state: int
    action: dict
    goto: dict

    history: list

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar
        self.stack = ["$"]
        self.action = {}
        self.goto = {}
        self.canonical_collection = self.__setCanonicalCollection__()
        self.inital_state = self.canonical_collection.index(self.grammar.getInitialItem())
        self.history = []

    def __closure__(self, set_of_items: set):
        closure_set = set_of_items.copy() #{(state, dot_pos)}
        new_items = {}
        while (True):
            prev_items = new_items.copy() #{(state, dot_pos)}
            for item in closure_set:
                if (item[1] == len(self.grammar.ordered_productions[item[0]][1])):
                    #The above comparison means that the dot is after the whole body of the production
                    continue
                next_symbol = self.grammar.ordered_productions[item[0]][1][item[1]]
                if (next_symbol in self.grammar.non_terminals):
                    for i, production_tuple in enumerate(self.grammar.ordered_productions):
                        if (production_tuple[0] == next_symbol):
                            new_items.add((i,0))
            if (prev_items == new_items):
                return closure_set
            else:
                closure_set.add(new_items)
                prev_items = new_items.copy()

    def __goto__(self, set_of_items: set, symbol: str):
        goto_set = set()
        for item in set_of_items:
            if (item[1] == len(self.grammar.ordered_productions[item[0]][1])):
                #The above comparison means that the dot is after the whole body of the production
                continue
            if (self.grammar.ordered_productions[item[0]][1][item[1]] is symbol):
                goto_set.add((item[0], item[1] + 1))
        return self.__closure__(goto_set)
            
    def __setCanonicalCollection__(self):
        '''
            Returns and ordered list of sets of items
            where each item is a tuple (a,b)
            where 'a' is the index of a production in grammar.ordered_productions
            and 'b' is position of the dot in the production's body
        '''
        cc = set()
        cc.add(self.__closure__(self.grammar.getInitialItem()))
        while (True):
            cc_len = len(cc)
            for set_of_items in cc:
                for symbol in self.grammar.alphabet:
                    goto_set = self.__goto__(set_of_items, symbol)
                    if (goto_set):
                        cc.add(goto_set)
            if (len(cc) == cc_len):
                return list(cc)
    
    def __constructSLRParsingTable__(self):
        # para cado estado canonico i, as funções de parsing são definidas tal que:
        for i, canonicalSet in enumerate(self.canonical_collection):
            for item in canonicalSet: # item: (prod_pos, dot_pos)
                production = self.grammar.ordered_productions[item[0]]
                if (production[0] is self.grammar.initial_symbol \
                        and item[1] == len(production[1])):
                    self.action[(i,"$")] = "acc"
                    continue
                if (item[1] == len(production[1])):
                    for symbol in self.grammar.follow(production[0]):
                        self.action[(i,symbol)] = ("r", production)
                else:
                    symbol = production[1][item[1]]
                    if (symbol in self.grammar.alphabet):
                        j_set = self.__goto__(canonicalSet, symbol)
                        if (j_set in self.canonical_collection):
                            self.action[(i, symbol)] = ("s", self.canonical_collection.index(j_set))
            for non_terminal in self.grammar.non_terminals:
                self.goto[(i, non_terminal)] = self.canonical_collection.index(self.__goto__(canonicalSet, non_terminal))

    def parse(self, input_buffer: list):

        input_buffer.append(("$", None))
        stack = [self.inital_state]

                         #stack   symbols  input        action
        self.history = [[stack.copy(), [], input_buffer, "shift"]]

        while (True):

            __action = self.action[(stack[0], input_buffer[0][0])]

            if (__action == "acc"):
                self.history.append([stack.copy(), [], input_buffer, "acc"])
                return True
            elif (__action[0] == "s"):
                stack.insert(0, __action[1])
                input_buffer.pop()
            elif (__action[0] == "r"):
                production = __action[1]
                del stack[:len(production[1])]
                stack.insert(0, self.goto[(stack[0], production[0])])
                #
            else:
                return False
            self.history.append([stack.copy(), [], input_buffer, __action])

    def printParsingTable(self):
        print("ACTION")
        print(self.action)
        print("\n")
        print("GOTO")
        print(self.goto)
        print("\n")

    def printHistory(self):
        print("stack\t\t\taction")
        for moment in self.history:
            stack = moment[0]
            symbols = moment[1]
            input = moment[2]
            action = moment[3]

            if (action == "acc"):
                action = "acc"
            elif (action[0] == "s"):
                action = "shift {}".format(action[1])
            elif (action[0] == "r"):
                action = "reduce {} -> {}".format(action[1][0], action[1][1])

            print("{}\t\t\t{}".format(stack, action))