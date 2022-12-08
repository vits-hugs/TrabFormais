from SyntaticalAnalyser.ContextFreeGrammar import ContextFreeGrammar
from SyntaticalAnalyser.SyntaticalAnalyser import LRParser
from SyntaticalAnalyser.GrammarReader import GrammarReader
from LexicalAnalyser.LexicalAnalyserGenerator import LexicalAnalyserGenerator
from LexicalAnalyser.LexicalAnalyser import LexicalAnalyser

if __name__ == '__main__':

    ers = "id: id\npastel: pastel"
    lexical_analyser = LexicalAnalyserGenerator.getLexicalAnalyser(ers)
    
    tokens, symbolList = lexical_analyser.exec("id pastel pastel id")

    reader = GrammarReader()
    grammar = reader.grammarfromFile('gram.txt',{'id','pastel'})
    grammar.initialize()

    parser = LRParser(grammar)

    parsing_result = parser.parse(tokens)

    print("input valid: {}".format(parsing_result))
    parser.printParsingTable()
    parser.printHistory()
