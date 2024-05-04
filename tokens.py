tokens = (
    'COMMENT', 'VAL', 'VAR', 'FUNCTION', 'ID',
    'INT_TYPE','FLOAT_TYPE','STRING_TYPE','VOID_TYPE', 'BOOL_TYPE', 'CHAR_TYPE',
    'INTEGER_LITERAL','FLOAT_LITERAL','STRING_LITERAL', 'BOOL_LITERAL', 'CHAR_LITERAL',
    # 'ARRAY_TYPE',
    'AND','OR','EQUAL','NOT_EQUAL',
    'GREATER_THAN','GREATER_THAN_EQUAL','LESS_THAN_EQUAL','LESS_THAN',
    'PLUS','MINUS','TIMES','DIVIDE','MOD', 'POWER',
    'ASSIGN','NOT',
    'LPAREN','RPAREN','LBRACE','RBRACE','LSQUARE','RSQUARE',
    'SEMICOLON','COMMA','COLON', 
    'IF','ELSE','WHILE',
    # 'TRUE','FALSE',
    'MAIN'
)

# Reserved keywords
reserved_keywords = {
    'val': 'VAL',
    'var': 'VAR',
    'function': 'FUNCTION',
    'int': 'INT_TYPE',
    'float': 'FLOAT_TYPE',
    'string': 'STRING_TYPE',
    'char': 'CHAR_TYPE',
    'void': 'VOID_TYPE',
    'bool': 'BOOL_TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'BOOL_LITERAL',
    'false': 'BOOL_LITERAL',
    'main': 'MAIN'
}

# Tokens
t_AND = r'&&'
t_OR = r'\|\|'
t_EQUAL = r'='
t_NOT_EQUAL = r'!='
t_GREATER_THAN_EQUAL = r'>='
t_LESS_THAN_EQUAL = r'<='
t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\^'
t_ASSIGN = r':='
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_keywords.get(t.value, 'ID')  # Check if it's a reserved keyword
    return t

def t_FLOAT_LITERAL(t):
    r'[0-9]*\.[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Invalid float value %d", t.value)
        t.value = 0
    return t

def t_INTEGER_LITERAL(t):
    r'[0-9]+(_[0-9]+)*'
    try:
        t.value = int(t.value.replace('_', ''))
    except ValueError:
        print("Invalid integer value: %d", t.value)
        t.value = 0
    return t

def t_BOOL_LITERAL(t):
    r'true|false'
    try:
        t.value = True if t.value == 'true' else False
    except ValueError:
        print("Invalid boolean value")
        t.value = False  
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    try:
        t.value = t.value[1:-1]  # Remove quotes
    except ValueError:
        print("Invalid String: %s", t.value)
        t.value = ""
    return t

def t_CHAR_LITERAL(t):
	r"(\'([^\\\'])\')|(\"([^\\\"])\")"
	return t

def t_COMMENT(t):
    r'\#.*'
    pass

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

from ply import lex
import sys

if __name__ == '__main__':
    
    # Create lexer
    lexer = lex.lex()

    if len(sys.argv) > 1:
        # Read input from file
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    else:
        # Read input from standard input
        data = ""
        while True:
            try:
                data += input() + "\n"
            except EOFError:
                break

    # Give input to lexer
    lexer.input(data)

    # Tokenize and print all tokens
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
    