class UnrecognizedToken(Exception):
    def __init__(self, lexeme, begin, end):
        message = 'UnrecognizedToken: {lexeme} at ({begin},{end})'.format(lexeme=lexeme, begin=begin, end=end)
        super().__init__(message)


class CharNotInAlfabet(Exception):
    def __init__(self, char):
        message = 'The char {char} is not in the defined alfabet.'.format(char=char)
        super().__init__(message)
