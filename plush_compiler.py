import sys
import json
from ply import yacc, lex
from semantic import Context, verify
from tokens import *
from rules import *
import codeGen

# Error handling function
def yacc_error_handler(token):
    if token is not None:
        print("Syntax error in input!")
        print(token)
    else:
        print("Syntax error in input!")
    sys.exit(1)

# Define lexer
lexer = lex.lex()

# Build the parser with the error handling function
parser = yacc.yacc(errorlog=yacc.NullLogger())

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

def main():
    # Parsing command line arguments
    import argparse
    arg_parser = argparse.ArgumentParser(description='PLush compiler')
    arg_parser.add_argument('filename', help='The PLush file to parse')
    arg_parser.add_argument('--tree', action='store_true', help='Print JSON representation of the AST')

    args = arg_parser.parse_args()
    input_filename = args.filename
    tree_flag = args.tree

    data = get_input(input_filename)
    
    # Lexical and Parsing checking the input file
    try:
        ast = parser.parse(data, lexer=lexer)
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

    if ast is None:
        print("Syntax error detected")
        sys.exit(1)

    continuar = True
    while continuar:
        continuar = False
        new_main_block_sequence = []
        if ast.main_block_sequence is not None:
            for i in ast.main_block_sequence:
                if isinstance(i, ImportStatement):
                    continuar = True
                    input_filename = i.filepath
                    data = get_input(input_filename)
                    try:
                        importedAst = parser.parse(data, lexer=lexer)
                    except Exception as e:
                        print(f"Exception: {e}")
                        sys.exit(1)
                    if importedAst is None:
                        print("Syntax error detected in imported file")
                        sys.exit(1)
                    if i.functions[0] == "*":
                        importedAst.main_block_sequence = [block for block in importedAst.main_block_sequence if not isinstance(block, MainFunction)]
                        new_main_block_sequence.extend(importedAst.main_block_sequence)
                    else:
                        for function in i.functions:
                            for block in importedAst.main_block_sequence:
                                if isinstance(block, FunctionDeclaration) and block.id == function:
                                    new_main_block_sequence.append(block)
                                    i.functions.remove(function)
                        if len(i.functions) > 0:
                            print("ERROR: Function(s) not found: " + str(i.functions) + " in file " + i.filepath)
                            sys.exit(1)
                else:
                    new_main_block_sequence.append(i)
            ast.main_block_sequence = new_main_block_sequence

    print("OK! PARSER PASSED!")

    # Print the AST if tree_flag is set
    if tree_flag:
        ast_json = json.dumps(ast, default=lambda o: o.__dict__, indent=2)
        print(ast_json)

    # Semantic verification
    try:
        verify(Context(), ast)
    except TypeError as e:
        print(f"Semantic error: {e}")
        sys.exit(1)
    print("OK! TYPE CHECKING PASSED!")

    # Code generation
    try:
        code_lines = codeGen.verify(ast)
        code_string = '\n'.join(code_lines)
        with open("test.ll", "w") as file:
            file.write(code_string)
        print("llvm CODE GENERATED!")
    except Exception as e:
        print(f"Code generation error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
