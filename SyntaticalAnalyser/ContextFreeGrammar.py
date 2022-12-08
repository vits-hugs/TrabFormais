class ContextFreeGrammar:
    alphabet: set
    initial_symbol: str
    non_terminals: set
    '''
        ordered_productions is a list of tuples, where the first element of the tuple
        is the head of the production and the second is the body as a list of symbols.
    '''
    ordered_productions: list

    def __init__(self, alphabet: set, initial_symbol: str, non_terminals: set):
        self.alphabet = alphabet
        self.initial_symbol = initial_symbol
        self.non_terminals = non_terminals
        self.__productions = {}
        self.ordered_productions = []
        self.__first_dict = dict
        self.__follow_dict = dict

    def __orderProductions__(self):
        self.ordered_productions = []
        for head in self.non_terminals:
            if (head == self.initial_symbol):
                self.ordered_productions.insert(0, (head, self.__productions[head][0] if self.__productions[head] else []))
            else:
                for body in self.__productions[head]:
                    self.ordered_productions.append((head, body))

    def __augment__(self):
        initial_productions = self.__productions[self.initial_symbol]
        if (len(initial_productions) != 1 or len(initial_productions[0]) != 1):
            initial_symbol = "*" + self.initial_symbol
            self.non_terminals.add(initial_symbol)
            self.__productions[initial_symbol] = [[self.initial_symbol]]
            self.initial_symbol = initial_symbol

    def __eliminateImidiateLeftRecursion__(self, head):
        alphas = []
        betas = []
        for production in self.__productions[head]:
            if (production[0] == head):
                if (not production[1:]):
                    self.__productions[head].remove(production)
                    return
                alphas.append(production[1:])
            else:
                betas.append(production)
        if (not alphas):
            return
        new_symbol = head + "`"
        head_productions = []
        for beta in betas:
            head_productions.append(beta + [new_symbol])
        new_symbol_productions = [["&"]]
        for alpha in alphas:
            new_symbol_productions.append(alpha + [new_symbol])
        self.non_terminals.add(new_symbol)
        self.__productions[head] = head_productions
        self.__productions[new_symbol] = new_symbol_productions

    def __eliminateLeftRecursion__(self):
        non_terminals = list(self.non_terminals)
        for i in range(len(non_terminals)):
            head = non_terminals[i]
            new_productions = []
            for production_body in self.__productions[head]:
                if (production_body[0] == head or production_body[0] not in self.non_terminals or production_body[0] not in non_terminals[:i]):
                    new_productions.append(production_body)
                    continue
                for handle in non_terminals[:i]:
                    if (handle == production_body[0]):
                        gamma = production_body[1:]
                        for delta in self.__productions[handle]:
                            new_productions.append(delta + gamma)
            self.__productions[head] = new_productions
            self.__eliminateImidiateLeftRecursion__(head)

    def initialize(self):
        self.__eliminateLeftRecursion__()
        self.__augment__()
        self.__orderProductions__()
        #self.first_dict = self.__calculateFirsts__()
        #self.follow_dict = self.__calculateFollows__()

    def addProduction(self, head: str, body: list):
        if (head not in self.__productions.keys()):
            self.__productions[head] = []
        self.__productions[head].append(body)
        self.ordered_productions.append((head, body))

    def getInitialItem(self):
        for i, production in enumerate(self.ordered_productions):
            if (production[0] is self.initial_symbol):
                return (i, 0)

    def __dictLen__(self, d: dict):
        count = 0
        for item in d.items():
            count += len(item[1])
        return count
    
    #Grammar must be non-left-recursive
    def __calculateFirsts__(self):
        __first_dict = {"&": {"&"}}
        for symbol in self.alphabet:
            __first_dict[symbol] = {symbol}
        prev_dict_len = self.__dictLen__(__first_dict)
        while (True):
            for head in self.non_terminals:
                fset = {}
                for pbody in self.__productions[head]:
                    if (pbody == ["&"]):
                        fset.add("&")
                    else:
                        for symbol in pbody:
                            symbol_first = __first_dict[symbol].copy() if __first_dict[symbol] else {}
                            fset = fset.union(symbol_first)
                            if ("&" not in symbol_first):
                                break
                __first_dict[head] = __first_dict[head].union(fset)
            curr_dict_len = self.__dictLen__(__first_dict)
            if (curr_dict_len == prev_dict_len):
                return __first_dict
            else:
                prev_dict_len = curr_dict_len

    def __calculateFollows__(self):
        __follow_dict = {self.initial_symbol: "$"}
        for non_terminal in self.non_terminals.remove(self.initial_symbol):
            __follow_dict[non_terminal] = set()
            for production in self.ordered_productions:
                if (non_terminal in production[1]):
                    for i, symbol in enumerate(production[1]):
                        if (symbol == non_terminal and i < len(production[1]) - 1):
                            follow_index = production[i] + 1
                            __follow_dict[non_terminal] = __follow_dict[non_terminal].union(self.first(production[follow_index:]).remove("&"))
        prev_dict_len = self.__dictLen__(__follow_dict)
        while (True):
            for non_terminal, production in [(nt,p) for nt in self.non_terminals for p in self.ordered_productions]:
                if (non_terminal in production[1]):
                    for i, symbol_iterator in enumerate(production[1]):
                        if (symbol_iterator == non_terminal \
                                and "&" in self.first(production[1][i+1:])):
                            __follow_dict[non_terminal] = __follow_dict[non_terminal].union(__follow_dict[production[0]])
                            break
            curr_dict_len = self.__dictLen__(__follow_dict)
            if (curr_dict_len == prev_dict_len):
                return __follow_dict
            else:
                prev_dict_len = curr_dict_len

    #Grammar must be non-left-recursive
    def first(self, sequence: list):
        first_set = set()
        for symbol in sequence:
            symbol_first = self.first_dict[symbol]
            first_set = first_set.union(symbol_first.difference(set("&")))
            if ("&" not in symbol_first):
                return first_set
        return first_set.union("&")

    def follow(self, non_terminal):
        return self.__follow_dict[non_terminal]