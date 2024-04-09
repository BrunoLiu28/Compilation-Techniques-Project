# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------

# tokens = (
#     'NAME','NUMBER',
#     'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
#     'LPAREN','RPAREN',
#     )
tokens = (
    'COMMENT', 'VAL', 'VAR', 'FUNCTION', 'NAME'
    'INT_TYPE','DOUBLE_TYPE','STRING_TYPE','VOID_TYPE',
    'INTEGER_LITERAL','FLOAT_LITERAL','STRING_LITERAL',
    # 'ARRAY_TYPE',
    # 'ID',
    'AND','OR','EQUAL','NOT_EQUAL',
    'GREATER_THAN','GREATER_THAN_EQUAL','LESS_THAN_EQUAL','LESS_THAN',
    'PLUS','MINUS','TIMES','DIVIDE','MOD',
    'ASSIGN','NOT',
    'LPAREN','RPAREN','LBRACE','RBRACE','LSQUARE','RSQUARE',
    'SEMICOLON','COMMA','COLON', 'DOT'
    'IF','THEN','ELSE','WHILE',
    'TRUE','FALSE'
)

# Reserved keywords
reserved = {
    'val': 'VAL',
    'var': 'VAR',
    'function': 'FUNCTION',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'string': 'STRING_TYPE',
    'void': 'VOID_TYPE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Add reserved keywords to tokens
tokens += list(reserved.values())
# Tokens
t_COMMENT = r'\#.*'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
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
t_DOT = r'\.'

def t_INTEGER_LITERAL(t):
    r'\d+(_\d+)*'
    try:
        t.value = int(t.value.replace('_', ''))
    except ValueError:
        print("Invalid integer value: %d", t.value)
        t.value = 0
    return t

def t_FLOAT_TYPE(t):
    r'\d*\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Invalid float value %d", t.value)
        t.value = 0
    return t

def t_STRING_TYPE(t):
    r'\"([^\\\n]|(\\.))*?\"'
    try:
        t.value = t.value[1:-1]  # Remove quotes
    except ValueError:
        print("Invalid String: %s", t.value)
        t.value = ""
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()


# Parsing rules
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)