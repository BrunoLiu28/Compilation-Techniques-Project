start = 'start_block'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    # ('nonassoc', 'EQUAL', 'NOT_EQUAL'),
    # ('nonassoc', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'),
    ('left', 'EQUAL', 'NOT_EQUAL'),
    ('left', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('right', 'NOT'),
    ('left', 'LPAREN', 'RPAREN'),  # Parentheses
)

# dictionary of names
names = { }

def t_start_block(t):
	"""start_block :  constant_declaration
    | variable_declaration
    | function_declaration
    |
	"""
	t[0] = t[1]

#FALTA OS ARRAYS E SE CALHAR INCLUIR O CHAR
def t_type(t):
    """type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE"""
    t[0] = t[1]

def t_expression(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression POWER expression
                  | expression EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression GREATER_THAN expression
                  | expression GREATER_THAN_EQUAL expression
                  | expression LESS_THAN expression
                  | expression LESS_THAN_EQUAL expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | INTEGER_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | BOOL_LITERAL
                  | ID
                  | LPAREN expression RPAREN'''
    if len(t) == 2:
        t[0] = t[1]
    elif t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '^':
        t[0] = t[1] ** t[3]
    elif t[2] == '=':
        t[0] = t[1] == t[3]
    elif t[2] == '!=':
        t[0] = t[1] != t[3]
    elif t[2] == '>':
        t[0] = t[1] > t[3]
    elif t[2] == '>=':
        t[0] = t[1] >= t[3]
    elif t[2] == '<':
        t[0] = t[1] < t[3]
    elif t[2] == '<=':
        t[0] = t[1] <= t[3]
    elif t[2] == '&&':
        t[0] = t[1] and t[3]
    elif t[2] == '||':
        t[0] = t[1] or t[3]
    elif t[1] == '!':
        t[0] = not t[2]

#VAL DECLARATION
def t_constant_declaration(t):
    """constant_declaration : VAL ID COLON type ASSIGN expression SEMICOLON"""
    t[0] = ('CONSTANT_DECLARATION', t[2], t[4], t[6])

#VAR DECLARATION
def t_variable_declaration(t):
    """variable_declaration : VAR ID COLON type ASSIGN expression SEMICOLON"""
    t[0] = ('VARIABLE_DECLARATION', t[2], t[4], t[6])

#FUNCTION DECLARATION
def t_function_declaration(t):
    """function_declaration : FUNCTION ID LPAREN function_param_list RPAREN COLON type SEMICOLON
    |  FUNCTION ID LPAREN function_param_list RPAREN COLON type LBRACE function_body RBRACE"""
    if len(t) == 9:
        t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7])
    else:
        t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7], t[9])
    

def t_function_param_list(t):
    """function_param_list : parameter COMMA function_param_list
    | parameter"""
    if len(t) == 4:
        t[0] = ("function_param_list", t[1], t[3])
    else:
        t[0] = t[1]

def t_parameter(t):
	""" parameter : VAL ID COLON type
    | VAR ID COLON type"""
	t[0] = ("parameter", t[2], t[4])

#FUNCTION CALL
def t_function_call(t):
    """function_call : ID LPAREN function_param_list_call RPAREN SEMICOLON
    """
    t[0] = ('FUNCTION_CALL', t[1], t[3])

def t_function_param_list_call(t):
    """function_param_list_call : ID COMMA function_param_list_call
    | ID"""
    if len(t) == 4:
        t[0] = ("function_param_list_call", t[1], t[3])
    else:
        t[0] = t[1]

#TO GET THE FUNCTION BODY
def t_function_body(t):
    """function_body : block_sequence"""
    t[0] = ('VARIABLE_DECLARATION', t[2], t[4], t[6])

def t_block_sequence(t):
	"""block_sequence : block SEMICOLON block_sequence
	 | block"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = ('block_list',t[1],t[3])

def t_block(t):
	"""block : constant_declaration
     | variable_declaration
	 | if_block
	 | while_block
	 | function_call
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]

def t_if_block(t):
	"""if_block : IF expression LBRACE block RBRACE LBRACE ELSE block RBRACE
	| IF expression LBRACE block RBRACE 
	"""
	if len(t) == 6:
		t[0] = ('if',t[2],t[4])
	else:
		t[0] = ('if',t[2],t[4],t[6])
	
def t_while_block(t):
	"""while_block : WHILE expression LBRACE block RBRACE"""
	t[0] = ('while',t[2],t[4])


def t_error(p):
    print("Syntax error in input!")
    print(p)





    