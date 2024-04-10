from ply import yacc, lex
from tokens import *
from rules import *
import sys

def get_input(file=False):
    if file:
        with open(file, "r") as f:
            data = f.read()
    else:
        data = ""
        while True:
            try:
                data += input() + "\n"
            except EOFError:
                break
    return data

def main(options={}, filename=False):
    # lexer = lex.lex()
    # parser = yacc.yacc(debug=False, errorlog=yacc.NullLogger(), returnnig=True)
    # data = get_input(filename)
    # ast = parser.parse(data, lexer=lexer)
    logger = yacc.NullLogger()
    yacc.yacc(debug = logger, errorlog= logger )
    data = get_input(filename)
    ast =  yacc.parse(data,lexer = lex.lex(nowarn=1))
    return ast

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_filename = sys.argv[1]
    ast = main(filename=input_filename)
    print(ast)