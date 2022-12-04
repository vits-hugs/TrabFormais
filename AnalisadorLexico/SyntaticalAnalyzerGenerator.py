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
    pass

class SyntaxTree:
    pass

class SymbolTable:
    pass

class FiniteStateAutomaton:
    alphabet: set(str)
    states: set(str)
    accepting_states: set(str)
    initial_state: str
    transition_table: dict((str,str))

    def __init__(self, alphabet):
        self.alphabet = alphabet

class DeterministicAutomaton(FiniteStateAutomaton):
    transition_table: dict((str,str),str)

class NonDeterministicAutomaton(FiniteStateAutomaton):
    transition_table: dict((str,str),set(str))

class LexicalPatternMatcher:
    lexemme_automaton: DeterministicAutomaton
    lookahead_automaton: DeterministicAutomaton
    current_state: str
    looking_ahead: bool
    lookahed_count: int
    idle: bool
    getToken: dict(str,function)

    def __init__(self, lexemme_automaton: DeterministicAutomaton, lookahead_automaton: DeterministicAutomaton):
        self.lexemme_automaton = lexemme_automaton
        self.lookahead_automaton = lookahead_automaton
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
    white_spaces: list[chr]
    pattern_matcher: LexicalPatternMatcher
    symbol_table: SymbolTable

    def __init__(self, pattern_matcher: LexicalPatternMatcher, white_spaces = [' ', '\t', '\n'], symbol_table: SymbolTable):
        self.source_reader = StringIO()
        self.white_spaces = white_spaces
        self.pattern_matcher = pattern_matcher
        self.symbol_table = symbol_table

    def loadSource(self, source):
        self.source_reader.open(source, "r", encoding="utf-8")

    def getNextToken(self):
        lexem_buffer = ""
        while (True):
            c = self.source_reader.read()
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

class SyntacticalAnalyzer:
    lexical_analyser: LexicalAnalyzer

class LexicalAnalyzerGenerator:
    lexemme_automaton: DeterministicAutomaton
    lookahead_automaton: DeterministicAutomaton
    re_parser: SyntacticalAnalyzer

    def __init__(self):
        pass

    def __createAutomatons__(self, alphabet: set(str)):
        self.lexemme_automaton = DeterministicAutomaton(alphabet)
        self.lookahead_automaton = DeterministicAutomaton(alphabet)

    def readLexicalDefinition(self, source: StringIO):
        pass

class SyntacticalAnalyzerGenerator:
    
    class GrammarDefinitionReader:
        pass