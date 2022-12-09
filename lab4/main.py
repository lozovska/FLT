import sys
from antlr4 import *
from gens.RegExGramLexer import RegExGramLexer
from gens.RegExGramParser import RegExGramParser

def main(argv):
    data = InputStream(input(": "))
    stream = CommonTokenStream(RegExGramLexer(data))
    parser = RegExGramParser(stream)
    parser.s()


if __name__ == "__main__":
    main(sys.argv)