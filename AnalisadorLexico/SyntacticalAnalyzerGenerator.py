from io import StringIO

class EndOfFileException(Exception):
    pass

class MatchingException(Exception):
    pass

class UnrecognizedSymbolExeption(Exception):
    pass

class LexicalException(Exception):
    pass

class RegularExpression:
    pass

class ContextFreeGrammar:
    alphabet: set
    initial_symbol: str
    non_terminals: set
    first_dict: dict
    follow_dict: dict
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
        self.first_dict = None
        self.follow_dict = None

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
        print(self.__productions[head])
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
        print(self.__productions)
        self.__eliminateLeftRecursion__()
        self.__augment__()
        self.__orderProductions__()
        self.first_dict = self.__first__()
        #self.follow_dict = self.__follow__()

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
    def __first__(self):
        first_dict = {"&": set("&")}
        for symbol in self.alphabet:
            first_dict[symbol] = set(symbol)
        prev_dict_len = self.__dictLen__(first_dict)
        while (True):
            for head in self.non_terminals:
                first_set = set()
                for production_body in self.__productions[head]:
                    if (production_body[0] == "&"):
                        first_set.add("&")
                    else:
                        for symbol in production_body:
                            symbol_first = first_dict[symbol].copy()
                            first_set = first_set.union(symbol_first)
                            if ("&" not in symbol_first):
                                break
                first_dict[head] = first_dict[head].union(first_set)
            curr_dict_len = self.__dictLen__(first_dict)
            if (curr_dict_len == prev_dict_len):
                return first_dict
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

    def __follow__(self):
        follow_dict = {self.initial_symbol: "$"}
        for non_terminal in self.non_terminals.remove(self.initial_symbol):
            follow_dict[non_terminal] = set()
            for production in self.ordered_productions:
                if (non_terminal in production[1]):
                    for i, symbol in enumerate(production[1]):
                        if (symbol == non_terminal and i < len(production[1]) - 1):
                            follow_index = production[i] + 1
                            follow_dict[non_terminal] = follow_dict[non_terminal].union(self.first(production[follow_index:]).remove("&"))
        prev_dict_len = self.__dictLen__(follow_dict)
        while (True):
            for non_terminal, production in [(nt,p) for nt in self.non_terminals for p in self.ordered_productions]:
                if (non_terminal in production[1]):
                    for i, symbol_iterator in enumerate(production[1]):
                        if (symbol_iterator == non_terminal \
                                and "&" in self.first(production[1][i+1:])):
                            follow_dict[non_terminal] = follow_dict[non_terminal].union(follow_dict[production[0]])
                            break
            curr_dict_len = self.__dictLen__(follow_dict)
            if (curr_dict_len == prev_dict_len):
                return follow_dict
            else:
                prev_dict_len = curr_dict_len

    def follow(self, non_terminal):
        return self.follow_dict[non_terminal]
        
class SyntaxTree:
    pass

class SymbolTable:
    pass

class FiniteStateAutomaton:
    alphabet: set()
    states: set()
    accepting_states: set()
    initial_state: str
    transition_table: dict()

    def __init__(self, alphabet = set(), states = set(), accepting_states = set(), initial_state = set(), transition_table = dict()):
        self.alphabet = alphabet
        self.states = states
        self.accepting_states = accepting_states
        self.initial_state = initial_state
        self.transition_table = transition_table

class DeterministicAutomaton(FiniteStateAutomaton):
    transition_table: dict

class NonDeterministicAutomaton(FiniteStateAutomaton):
    transition_table: dict

class LexicalPatternMatcher:
    lexemme_automaton: DeterministicAutomaton
    lookahead_automaton: DeterministicAutomaton
    current_state: str
    looking_ahead: bool
    lookahed_count: int
    idle: bool
    getToken: dict

    def __init__(self, lexemme_automaton: DeterministicAutomaton, lookahead_automaton: DeterministicAutomaton, getToken: dict):
        self.lexemme_automaton = lexemme_automaton
        self.lookahead_automaton = lookahead_automaton
        self.getToken = getToken
        self.__reset__()

    def __reset__(self):
        self.looking_ahead = False
        self.lookahed_count = 0
        self.current_state = self.lexemme_automaton.initial_state
        self.idle = True

    def __lookahead_transition__(self, symbol):
        transition_state = self.lookahead_automaton.transition_table[(self.current_state, symbol)]
        if (transition_state):
            self.current_state = transition_state
            self.lookahed_count += 1
            return None
        elif (self.current_state in self.lookahead_automaton.accepting_states):
            return (self.getToken[self.current_state](), self.lookahed_count)
        else:
            return False

    def transition(self, symbol: str):
        if (symbol in self.lexemme_automaton.alphabet):
            if (not self.looking_ahead):
                transition_state = self.lexemme_automaton.transition_table[(self.current_state, symbol)]
                if (transition_state):
                    self.current_state = transition_state
                    return None
                elif (self.current_state in self.lexemme_automaton.accepting_states):
                    lookahead_result = self.__lookahead_transition__(symbol)
                    if (lookahead_result is None):
                        self.looking_ahead = True
                        return True
                    else:
                        self.__reset__()
                        return (self.getToken[self.current_state](), 0)
                else:
                    self.__reset__()
                    return False
            else:
                lookahead_result = self.__lookahead_transition__(symbol)
                if (lookahead_result):
                    self.__reset__()
                    return lookahead_result
                elif (lookahead_result is None):
                    return None
                else:
                    self.__reset__()
                    return False
        else:
            raise UnrecognizedSymbolExeption()

class LexicalAnalyzer:
    source_reader: StringIO
    white_spaces: list
    pattern_matcher: LexicalPatternMatcher
    #symbol_table: SymbolTable

    def __init__(self, pattern_matcher: LexicalPatternMatcher, white_spaces = [' ', '\t', '\n']):
        self.source_reader = StringIO()
        self.white_spaces = white_spaces
        self.pattern_matcher = pattern_matcher
        #self.symbol_table = symbol_table

    def loadSource(self, source):
        self.source_reader.open(source, "r", encoding="utf-8")

    def getNextToken(self):
        lexem_buffer = ""
        while (True):
            c = self.source_reader.read(1)
            if (c is None):
                return None
            elif (self.pattern_matcher.idle):
                if (c in self.white_spaces):
                    continue
                else:
                    self.pattern_matcher.idle = False
            matching_result = self.pattern_matcher.transition(c)
            if (matching_result is False):
                raise LexicalException()
            elif (matching_result is None and not self.pattern_matcher.looking_ahead):
                lexem_buffer += c
            elif (c in self.white_spaces):
                continue
            else:
                self.source_reader.seek(self.source_reader.tell() - matching_result[1])
                return matching_result[0]

class LRParser:
    #symbol_table: SymbolTable
    #lexical_analyser: LexicalAnalyzer
    grammar: ContextFreeGrammar
    canonical_collection: list
    inital_state: int
    action: dict
    goto: dict

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar
        self.stack = ["$"]
        self.action = {}
        self.goto = {}
        self.canonical_collection = self.__setCanonicalCollection__()
        self.inital_state = self.canonical_collection.index(self.grammar.getInitialItem())

    def __closure__(self, set_of_items: set):
        closure_set = set_of_items.copy()
        new_items = set()
        while (True):
            prev_items = new_items.copy()
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
        for i, canonicalSet in enumerate(self.canonical_collection):
            for item in canonicalSet:
                production = self.grammar.ordered_productions[item[0]]
                if (production[0] is self.grammar.initial_symbol \
                        and item[1] == len(production[1])):
                    self.action[(i,"$")] = True
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
        input_buffer.append("$")
        stack = [self.inital_state]
        while (True):
            action = self.action[(stack[0],input_buffer[0])]
            if (action == True):
                break #parsing finished
            elif (action[0] == "s"):
                stack.insert(0, action[1])
                input_buffer.pop()
            elif (action[0] == "r"):
                production = action[1]
                del stack[:len(production[1])]
                stack.insert(0, self.goto[(stack[0], production[0])])
                #
            else:
                pass #error
            

class LexicalAnalyzerGenerator:
    lexemme_automaton: DeterministicAutomaton
    lookahead_automaton: DeterministicAutomaton
    re_parser: LRParser

    def __init__(self):
        pass

    def __createAutomatons__(self, alphabet: set()):
        self.lexemme_automaton = DeterministicAutomaton(alphabet)
        self.lookahead_automaton = DeterministicAutomaton(alphabet)

    def readLexicalDefinition(self, source: StringIO):
        pass

class SyntacticalAnalyzerGenerator:
    
    class GrammarDefinitionReader:
        pass

def getTokenFun():
    print("ok")


if (__name__ == "__main__"):
    grammar = ContextFreeGrammar({"id", "+", "*", "(", ")"}, "E", {"E", "T", "F"})
    grammar.addProduction("E", ["E","+","T"])
    grammar.addProduction("E", ["T"])
    grammar.addProduction("T", ["T","*","F"])
    grammar.addProduction("T", ["F"])
    grammar.addProduction("F", ["(","E",")"])
    grammar.addProduction("F", ["id"])
    grammar.initialize()
    print(grammar.ordered_productions)