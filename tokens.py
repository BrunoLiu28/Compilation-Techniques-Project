tokens = (
    'COMMENT', 'VAL', 'VAR', 'FUNCTION', 'ID',
    'INT_TYPE','FLOAT_TYPE','STRING_TYPE','VOID_TYPE', 'BOOL_TYPE',
    'INTEGER_LITERAL','FLOAT_LITERAL','STRING_LITERAL', 'BOOL_LITERAL',
    # 'ARRAY_TYPE',
    'AND','OR','EQUAL','NOT_EQUAL',
    'GREATER_THAN','GREATER_THAN_EQUAL','LESS_THAN_EQUAL','LESS_THAN',
    'PLUS','MINUS','TIMES','DIVIDE','MOD', 'POWER',
    'ASSIGN','NOT',
    'LPAREN','RPAREN','LBRACE','RBRACE','LSQUARE','RSQUARE',
    'SEMICOLON','COMMA','COLON', 
    #'DOT'
    'IF','THEN','ELSE','WHILE',
    'TRUE','FALSE'
)

# Reserved keywords
reserved_keywords = {
    'val': 'VAL',
    'var': 'VAR',
    'function': 'FUNCTION',
    'int': 'INT_TYPE',
    'float': 'FLOAT_TYPE',
    'string': 'STRING_TYPE',
    'void': 'VOID_TYPE',
    'bool': 'BOOL_TYPE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Tokens
t_COMMENT = r'\#.*'
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
# t_DOT = r'\.'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_keywords.get(t.value, 'ID')  # Check if it's a reserved keyword
    return t


def t_INTEGER_LITERAL(t):
    r'\d+(_\d+)*'
    try:
        t.value = int(t.value.replace('_', ''))
    except ValueError:
        print("Invalid integer value: %d", t.value)
        t.value = 0
    return t

def t_FLOAT_LITERAL(t):
    r'\d*\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Invalid float value %d", t.value)
        t.value = 0
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    try:
        t.value = t.value[1:-1]  # Remove quotes
    except ValueError:
        print("Invalid String: %s", t.value)
        t.value = ""
    return t

def t_BOOL_LITERAL(t):
    r'true|false'
    try:
        t.value = True if t.value == 'true' else False
    except ValueError:
        print("Invalid boolean value")
        t.value = False  
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

# precedence = (
#     ('left', 'OR'),
#     ('left', 'AND'),
#     # ('nonassoc', 'EQUAL', 'NOT_EQUAL'),
#     # ('nonassoc', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'),
#     ('left', 'EQUAL', 'NOT_EQUAL'),
#     ('left', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'),
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'TIMES', 'DIVIDE', 'MOD'),
#     ('right', 'POWER'),
#     ('right', 'NOT'),
#     ('left', 'LPAREN', 'RPAREN'),  # Parentheses
# )

# # dictionary of names
# names = { }


# #FALTA OS ARRAYS E SE CALHAR INCLUIR O CHAR
# def p_type(t):
#     """type : INT_TYPE
#             | FLOAT_TYPE
#             | STRING_TYPE
#             | BOOL_TYPE"""
#     t[0] = t[1]

# def p_expression(t):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression
#                   | expression TIMES expression
#                   | expression DIVIDE expression
#                   | expression MOD expression
#                   | expression POWER expression
#                   | expression EQUAL expression
#                   | expression NOT_EQUAL expression
#                   | expression GREATER_THAN expression
#                   | expression GREATER_THAN_EQUAL expression
#                   | expression LESS_THAN expression
#                   | expression LESS_THAN_EQUAL expression
#                   | expression AND expression
#                   | expression OR expression
#                   | NOT expression
#                   | INTEGER_LITERAL
#                   | FLOAT_LITERAL
#                   | STRING_LITERAL
#                   | BOOL_LITERAL
#                   | ID
#                   | LPAREN expression RPAREN'''
#     if len(t) == 2:
#         t[0] = t[1]
#     elif t[2] == '+':
#         t[0] = t[1] + t[3]
#     elif t[2] == '-':
#         t[0] = t[1] - t[3]
#     elif t[2] == '*':
#         t[0] = t[1] * t[3]
#     elif t[2] == '/':
#         t[0] = t[1] / t[3]
#     elif t[2] == '%':
#         t[0] = t[1] % t[3]
#     elif t[2] == '^':
#         t[0] = t[1] ** t[3]
#     elif t[2] == '=':
#         t[0] = t[1] == t[3]
#     elif t[2] == '!=':
#         t[0] = t[1] != t[3]
#     elif t[2] == '>':
#         t[0] = t[1] > t[3]
#     elif t[2] == '>=':
#         t[0] = t[1] >= t[3]
#     elif t[2] == '<':
#         t[0] = t[1] < t[3]
#     elif t[2] == '<=':
#         t[0] = t[1] <= t[3]
#     elif t[2] == '&&':
#         t[0] = t[1] and t[3]
#     elif t[2] == '||':
#         t[0] = t[1] or t[3]
#     elif t[1] == '!':
#         t[0] = not t[2]

# #VAL DECLARATION
# def p_constant_declaration(t):
#     """constant_declaration : VAL ID COLON type ASSIGN expression SEMICOLON"""
#     t[0] = ('CONSTANT_DECLARATION', t[2], t[4], t[6])

# #VAR DECLARATION
# def p_variable_declaration(t):
#     """variable_declaration : VAR ID COLON type ASSIGN expression SEMICOLON"""
#     t[0] = ('VARIABLE_DECLARATION', t[2], t[4], t[6])

# #FUNCTION DECLARATION
# def p_function_declaration(t):
#     """function_declaration : FUNCTION ID LPAREN function_param_list RPAREN COLON type SEMICOLON
#     |  FUNCTION ID LPAREN function_param_list RPAREN COLON type LBRACE function_body RBRACE"""
#     if len(t) == 9:
#         t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7])
#     else:
#         t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7], t[9])
    

# def p_function_param_list(t):
#     """function_param_list : parameter COMMA function_param_list
#     | parameter"""
#     if len(t) == 4:
#         t[0] = ("function_param_list", t[1], t[3])
#     else:
#         t[0] = t[1]

# def p_parameter(t):
# 	""" parameter : VAL ID COLON type
#     | VAR ID COLON type"""
# 	t[0] = ("parameter", t[2], t[4])

# #FUNCTION CALL
# def p_function_call(t):
#     """function_call : ID LPAREN function_param_list_call RPAREN SEMICOLON
#     """
#     t[0] = ('FUNCTION_CALL', t[1], t[3])

# def p_function_param_list_call(t):
#     """function_param_list_call : ID COMMA function_param_list_call
#     | ID"""
#     if len(t) == 4:
#         t[0] = ("function_param_list_call", t[1], t[3])
#     else:
#         t[0] = t[1]

# #TO GET THE FUNCTION BODY
# def p_function_body(t):
#     """function_body : block_sequence"""
#     t[0] = ('VARIABLE_DECLARATION', t[2], t[4], t[6])

# def p_block_sequence(t):
# 	"""block_sequence : block SEMICOLON block_sequence
# 	 | block"""
# 	if len(t) == 2:
# 		t[0] = t[1]
# 	else:
# 		t[0] = ('block_list',t[1],t[3])

# def p_block(t):
# 	"""block : constant_declaration
#      | variable_declaration
# 	 | if_block
# 	 | while_block
# 	 | function_call
# 	 |
# 	"""
# 	if len(t) > 1:
# 		t[0] = t[1]

# def p_if_block(t):
# 	"""if_block : IF expression LBRACE block RBRACE LBRACE ELSE block RBRACE
# 	| IF expression THEN block ELSE block
# 	"""
# 	if len(t) == 5:
# 		t[0] = ('if',t[2],t[4])
# 	else:
# 		t[0] = ('if',t[2],t[4],t[6])
	
# def p_while_block(t):
# 	"""while_block : WHILE expression LBRACE block RBRACE"""
# 	t[0] = ('while',t[2],t[4])


# def p_error(p):
#     print("Syntax error in input!")
#     print(p)

# import ply.yacc as yacc
# parser = yacc.yacc()
# parser.start = 'constant_declaration', 'variable_declaration', 'function_declaration'

if __name__ == '__main__':
    # Build the lexer
    from ply import lex
    import sys 
    
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
    