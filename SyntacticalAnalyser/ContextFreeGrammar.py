import logging

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

        logging.basicConfig(format='%(name) -24s %(funcName) -40s %(levelname) -8s %(message)s',
                        level=logging.WARNING)
        # note the `logger` from above is now properly configured
        self.logger = logging.getLogger(__name__)
        self.logger.debug("started")


    def __augment__(self):
        initial_productions = self.__productions[self.initial_symbol]
        if (len(initial_productions) != 1 or len(initial_productions[0]) != 1):
            initial_symbol = "*" + self.initial_symbol
            self.non_terminals.add(initial_symbol)
            self.__productions[initial_symbol] = [[self.initial_symbol]]
            self.initial_symbol = initial_symbol

    def __eliminateImidiateLeftRecursion__(self, head):
        self.logger.info("initiating {} imidiate left recursion elimination".format(head))
        alphas = []
        betas = []
        for production in self.__productions[head]:
            self.logger.debug("for {} in {}".format(production, self.__productions[head]))
            if (production[0] == head):
                if (not production[1:]):
                    self.__productions[head].remove(production)
                    self.logger.debug("removed {} from {} productions".format(production, head))
                    continue
                alphas.append(production[1:])
                self.logger.debug("{} appended to {} alphas".format(production[1:], head))
            else:
                betas.append(production)
                self.logger.debug("{} appended to {} betas".format(production, head))
        if (not alphas):
            self.logger.debug("alphas empty, nothing needs to be done for {}".format(head))
            return
        new_symbol = head + "`"
        head_productions = []
        self.logger.debug("new non-terminal created: {}".format(new_symbol))
        for beta in betas:
            head_productions.append(beta + [new_symbol])
        new_symbol_productions = [["&"]]
        for alpha in alphas:
            new_symbol_productions.append(alpha + [new_symbol])
        self.non_terminals.add(new_symbol)
        self.__productions[head] = head_productions
        self.logger.debug("registered {} -> {}".format(head, head_productions))
        self.__productions[new_symbol] = new_symbol_productions
        self.logger.debug("registered {} -> {}".format(new_symbol, new_symbol_productions))
        self.logger.info("finished imidiate left recursion elimination for {}".format(head))

    def __eliminateLeftRecursion__(self):
        self.logger.info("initiating left recursion elimination")
        non_terminals = list(self.non_terminals)
        for i in range(len(non_terminals)):
            head = non_terminals[i]
            new_productions = []
            self.logger.info("avaliating {} productions".format(head))
            for production_body in self.__productions[head]:
                self.logger.info("for {} -> {}".format(head, production_body))
                if (production_body[0] == head or production_body[0] not in self.non_terminals or production_body[0] not in non_terminals[:i]):
                    new_productions.append(production_body)
                    self.logger.info("{} added to new productions list".format(production_body))
                    continue
                for handle in non_terminals[:i]:
                    if (handle == production_body[0]):
                        gamma = production_body[1:]
                        for delta in self.__productions[handle]:
                            new_productions.append(delta + gamma)
                            self.logger.info("{} added to new productions list".format(delta + gamma))
            self.__productions[head] = new_productions
            self.logger.debug("{} productions set to {}".format(head, new_productions))
            self.__eliminateImidiateLeftRecursion__(head)
            self.logger.debug("finished {} productions avaliation".format(head))

    def __orderProductions__(self):
        self.ordered_productions = []
        for head in self.non_terminals:
            if (head == self.initial_symbol):
                self.ordered_productions.insert(0, (head, self.__productions[head][0] if self.__productions[head] else []))
            else:
                for body in self.__productions[head]:
                    self.ordered_productions.append((head, body))

    def initialize(self):
        self.__eliminateLeftRecursion__()
        self.__augment__()
        self.__orderProductions__()
        self.__first_dict = self.__calculateFirsts__()
        self.__follow_dict = self.__calculateFollows__()

    def addProduction(self, head: str, body: list):
        if (head not in self.__productions.keys()):
            self.__productions[head] = []
        self.__productions[head].append(body)
        self.ordered_productions.append((head, body))

    def getProductions(self):
        return self.__productions

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
        #__first_dict = {"&": {"&"}}
        __first_dict = dict()
        for symbol in self.alphabet:
            __first_dict[symbol] = set()
            __first_dict[symbol].add(symbol)
        prev_dict_len = self.__dictLen__(__first_dict)
        while (True):
            for head in self.non_terminals:
                if (head not in __first_dict.keys()):
                    __first_dict[head] = set()
                fset = set()
                for i in range(2):
                    for pbody in self.__productions[head]:
                        if (pbody == ["&"]):
                            fset.add("&")
                        else:
                            for symbol in pbody:
                                if symbol not in __first_dict.keys():
                                    __first_dict[symbol] = set()
                                symbol_first = __first_dict[symbol]
                                fset = fset.union(symbol_first)
                                if ("&" not in symbol_first):
                                    break
                    __first_dict[head] = fset.union(__first_dict[head])
            curr_dict_len = self.__dictLen__(__first_dict)
            if (curr_dict_len == prev_dict_len):
                return __first_dict
            else:
                prev_dict_len = curr_dict_len

    def __calculateFollows__(self):
        # Place $ in FOLLOW(S), where S is the start symbol and $ is th einput right endmarker.
        __follow_dict = {self.initial_symbol: set("$")}
        # If there is a production A -> a B b , then everything in FIRST(b) except & is in FOLLOW (B).
        for head in self.non_terminals:
            if (head not in __follow_dict.keys()):
                __follow_dict[head] = set()
            for production_body in self.__productions[head]:
                for j, symbol in enumerate(production_body):
                    if (symbol in self.non_terminals and j + 1 < len(production_body)):
                        if (symbol not in __follow_dict.keys()):
                            __follow_dict[symbol] = set()
                        if (production_body[j + 1] not in __follow_dict.keys()):
                            __follow_dict[production_body[j + 1]] = set()
                        __follow_dict[symbol] = __follow_dict[symbol].union(set("&").difference(self.__first_dict[production_body[j + 1]]))
        # If there is a production A -> a B, or a production A -> a B b, where FIRST(b) contains &, then everything in FOLLOW (A) is in FOLLOW (B).
        prev_dict_len = self.__dictLen__(__follow_dict) 
        while (True):
            for head in self.non_terminals:
                for production_body in self.__productions[head]:
                    for j, symbol in enumerate(production_body):
                        if ((symbol in self.non_terminals) \
                                and (j + 1 < len(production_body) and "&" in self.__first_dict[production_body[j + 1]])):
                            if (symbol not in __follow_dict.keys()):
                                __follow_dict[symbol] = set()
                            __follow_dict[symbol] = __follow_dict[symbol].union(self.__first_dict[head])
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
