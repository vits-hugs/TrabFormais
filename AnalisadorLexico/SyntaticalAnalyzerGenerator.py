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
    productions: dict
    follow_dict: dict
    #ordered_productions is a list of tuples, where the first element of the tuple
    #is the head of the production and the second is the body as a list of symbols.
    ordered_productions: list

    def __init__(self, alphabet: set, initial_symbol: str, non_terminals: str):
        self.alphabet = alphabet
        self.initial_symbol = initial_symbol
        self.non_terminals = non_terminals
        self.follow_dict = None

    def __orderProductions__(self):
        self.ordered_productions = []
        for head, body in self.productions.items():
            self.ordered_productions.push((head, body))

    def __augment__(self):
        initial_productions = self.productions[self.initial_symbol]
        if (len(initial_productions) != 1 or len(initial_productions[0]) != 1):
            initial_symbol = self.initial_symbol + "`"
            self.productions[initial_symbol] = [[self.initial_symbol]]
            self.initial_symbol = initial_symbol

    def addProduction(self, head: str, body: list):
        if (len(self.productions[head]) == 0):
            self.productions[head] = []
        self.productions[head].append(body)

    def getInitialItem(self):
        for i, production in enumerate(self.ordered_productions):
            if (production[0] is self.initial_symbol):
                return (i, 0)
    
    #Grammar must be non-left-recursive
    def __first__(self, symbol):
        if (symbol in self.alphabet):
            return set(symbol)
        elif(symbol in self.non_terminals):
            first_set = set()
            for production in self.productions[symbol]:
                if (production[0] is "&"):
                    first_set.add("&")
                else:
                    for production_symbol in production:
                        production_symbol_first = self.first(production_symbol)
                        first_set = first_set.union(production_symbol_first)
                        if ("&" not in production_symbol_first):
                            break
            return first_set
        elif (symbol is "&"):
            return set("&")
        else:
            return set()

    #Grammar must be non-left-recursive
    def first(self, sequence: list):
        first_set = set()
        for symbol in sequence:
            symbol_first = self.__first__(symbol)
            first_set = first_set.union(symbol_first.difference(set("&")))
            if ("&" not in symbol_first):
                return first_set
        return first_set.union("&")

    def __followDictLen__(self, follow_dict):
        count = 0
        for item in follow_dict.items():
            count += len(item[1])
        return count


    def __follow__(self):
        follow_dict = dict()
        for non_terminal in self.non_terminals:
            if (non_terminal == self.initial_symbol):
                follow_dict[non_terminal] = set("$")
            else:
                follow_dict[non_terminal] = set()
            for production in self.ordered_productions:
                if (non_terminal in production[1]):
                    for i, symbol in enumerate(production[1]):
                        if (symbol == non_terminal and i < len(production[1]) - 1):
                            follow_index = production[i] + 1
                            follow_dict[non_terminal] = follow_dict[non_terminal].union(self.first(production[follow_index:]).remove("&"))
        prev_dict_len = self.__followDictLen__(follow_dict)
        while (True):
            for non_terminal in self.non_terminals:
                for production in self.ordered_productions:
                    if (non_terminal in production[1]):
                        for i, symbol_iterator in enumerate(production[1]):
                            if (symbol_iterator == non_terminal):
                                if ("&" in self.first(production[1][i+1:])):
                                    follow_dict[non_terminal] = follow_dict[non_terminal].union(follow_dict[production[0]])
                                    break
            curr_dict_len = self.__followDictLen__(follow_dict)
            if (curr_dict_len == prev_dict_len):
                return follow_dict
            else:
                prev_dict_len = curr_dict_len

    def follow(self, non_terminal):
        if (non_terminal not in self.non_terminals):
            return
        if (not self.follow_dict):
            self.follow_dict = self.__follow__()
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
    stack: list
    action: dict
    goto: dict
    srl_parsing_table: dict

    def __init__(self, grammar: ContextFreeGrammar):
        self.grammar = grammar
        self.stack = ["$"]
        self.action = {}
        self.goto = {}
        self.srl_parsing_table = {}
        self.grammar.__augment__()
        self.grammar.__orderProductions__()
        self.canonical_collection = self.__getCanonicalCollection__()


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
            
    def __getCanonicalCollection__(self):
        cc = set()
        cc.add(self.__closure__(self.grammar.getInitialItem()))
        while (True):
            cc_len = len(cc)
            for set_of_items in cc:
                for symbol in self.grammar.alphabet:
                    goto_set = self.__goto__(set_of_items, symbol)
                    if (len(goto_set) > 0):
                        cc.add(goto_set)
            if (len(cc) == cc_len):
                return list(cc)
    
    def __constructSLRParsingTable__(self):
        for i, canonicalSet in enumerate(self.canonical_collection):
            for item in canonicalSet:
                if (item[1] == len(self.grammar.ordered_productions[item[0]][1])):
                    
                symbol = self.grammar.ordered_productions[item[0]][1][item[1]]
                if (symbol in self.grammar.alphabet):
                    j_set = self.__goto__(canonicalSet, symbol)
                    if (j_set in self.canonical_collection):
                        self.action[i, symbol] = ("s", self.canonical_collection.index(j_set))
                




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
    transition_table = {("i","a"): "i", ("i","b"): "1", ("1","a"): "f"}
    getToken = {"f": getTokenFun}
    lexemme_automaton = DeterministicAutomaton(alphabet = {"a","b"}, states = {"i", "1", "f"}, \
                                                accepting_states={"f"}, initial_state={"i"}, \
                                                transition_table=transition_table)
    pattern_matcher = LexicalPatternMatcher(lexemme_automaton=lexemme_automaton, lookahead_automaton=DeterministicAutomaton(), getToken=getToken)
    lexical_analyzer = LexicalAnalyzer(pattern_matcher=pattern_matcher)
    lexical_analyzer.loadSource("./in.txt")
