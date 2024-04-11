start = 'main_block_sequence'

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


#MAIN BODY OF THE PROGRAM
# def p_start_block(t):
#     """start_block : main_block start_block
#                     | main_block """
#     if len(t) == 2:
#         t[0] = t[1]
#     else:
#         t[0] = ('START_BLOCK',t[1],t[2])

def p_main_block_sequence(t):
	"""main_block_sequence : main_block main_block_sequence
	 | main_block"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = ('MAIN_BLOCK_SEQUENCE',t[1],t[2])

def p_main_block(t):
	"""main_block : constant_declaration
     | variable_declaration 
	 | function_declaration 
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]
    
#VAL DECLARATION
def p_constant_declaration(t):
    """constant_declaration : VAL ID COLON defaulttype ASSIGN expression SEMICOLON
                            | VAL ID COLON arraytype ASSIGN expression SEMICOLON"""
    t[0] = ('CONSTANT_DECLARATION', t[2], t[4], t[6])

#VAR DECLARATION
def p_variable_declaration(t):
    """variable_declaration : VAR ID COLON defaulttype ASSIGN expression SEMICOLON
                            | VAR ID COLON arraytype ASSIGN expression SEMICOLON"""
    t[0] = ('VARIABLE_DECLARATION', t[2], t[4], t[6])

#FUNCTION DECLARATION
def p_function_declaration(t):
    """function_declaration : FUNCTION ID LPAREN function_param_list RPAREN COLON types SEMICOLON
    |  FUNCTION ID LPAREN function_param_list RPAREN COLON types LBRACE function_body RBRACE"""
    if len(t) == 9:
        t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7])
    else:
        t[0] = ('FUNCTION_DECLARATION', t[2], t[4], t[7], t[9])
    

def p_function_param_list(t):
    """function_param_list : parameter COMMA function_param_list
    | parameter"""
    if len(t) == 4:
        t[0] = ("FUNCTION_PARAM_LIST", t[1], t[3])
    else:
        t[0] = t[1]

def p_parameter(t):
    """ parameter : VAL ID COLON defaulttype
                    | VAR ID COLON defaulttype
                    | VAL ID COLON arraytype
                    | VAR ID COLON arraytype"""
    if t[1] == 'var':
        t[0] = ("VAR", t[2], t[4])
    else:
        t[0] = ("VAL", t[2], t[4])

#FUNCTION CALL
def p_function_call(t):
    """function_call : ID LPAREN function_param_list_call RPAREN SEMICOLON
    """
    t[0] = ('FUNCTION_CALL', t[1], t[3])

def p_function_param_list_call(t):
    """function_param_list_call : ID COMMA function_param_list_call
    | ID"""
    if len(t) == 4:
        t[0] = ("FUNCTION_PARAM_LIST_CALL", t[1], t[3])
    else:
        t[0] = t[1]

#TO GET THE FUNCTION BODY
def p_function_body(t):
    """function_body : block_sequence"""
    t[0] = ('FUNCTION_BODY', t[1])

def p_block_sequence(t):
	"""block_sequence : block block_sequence
	 | block"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = ('BLOCK_SEQUENCE',t[1],t[2])

def p_block(t):
	"""block : constant_declaration
     | variable_declaration 
	 | if_block
	 | while_block
	 | function_call 
	 |
	"""
	if len(t) > 1:
		t[0] = t[1]

def p_if_block(t):
	"""if_block : IF expression LBRACE block RBRACE LBRACE ELSE block RBRACE
	| IF expression LBRACE block RBRACE 
	"""
	if len(t) == 6:
		t[0] = ('if',t[2],t[4])
	else:
		t[0] = ('if',t[2],t[4],t[6])
	
def p_while_block(t):
	"""while_block : WHILE expression LBRACE block RBRACE"""
	t[0] = ('WHILE',t[2],t[4])


#FALTA OS ARRAYS E SE CALHAR INCLUIR O CHAR
def p_types(t):
    """types : defaulttype
            | arraytype"""
    t[0] = t[1]

def p_defaultype(t):
    """defaulttype : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | VOID_TYPE"""
    t[0] = t[1]

def p_arraytype(t):
    """arraytype : LSQUARE arraytype RSQUARE
            | INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE"""
    if len(t)>2:
        t[0] = ('ARRAY', t[2])
    else:
        t[0] = t[1]

def p_typeliterals(t):
    """typeliterals : INTEGER_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | BOOL_LITERAL"""
    t[0] = t[1]

def p_arrayliterals(t):
    """arrayliterals : LSQUARE int_array RSQUARE
            | LSQUARE float_array RSQUARE
            | LSQUARE string_array RSQUARE
            | LSQUARE bool_array RSQUARE"""
    t[0] = t[1]

def p_int_array(t):
    """int_array : INTEGER_LITERAL
                | INTEGER_LITERAL COMMA int_array"""
    if len(t) == 2:
        t[0] = ('INT_ARRAY', t[1])
    else:
        t[0] = ('INT_ARRAY', t[1], t[3])

def p_float_array(t):
    """float_array : FLOAT_LITERAL
                | FLOAT_LITERAL COMMA float_array"""
    if len(t) == 2:
        t[0] = ('FLOAT_ARRAY', t[1])
    else:
        t[0] = ('FLOAT_ARRAY', t[1], t[3])

def p_string_array(t):
    """string_array : STRING_LITERAL
                | STRING_LITERAL COMMA string_array"""
    if len(t) == 2:
        t[0] = ('STRING_ARRAY', t[1])
    else:
        t[0] = ('STRING_ARRAY', t[1], t[3])

def p_bool_array(t):
    """bool_array : BOOL_LITERAL
                | BOOL_LITERAL COMMA bool_array"""
    if len(t) == 2:
        t[0] = ('BOOL_ARRAY', t[1])
    else:
        t[0] = ('BOOL_ARRAY', t[1], t[3])


def p_expression(t):
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
                  | typeliterals
                  | arrayliterals
                  | ID
                  | LPAREN expression RPAREN'''
    if len(t) == 2:
        t[0] = t[1]
    elif t[2] == '+':
        t[0] = ('PLUS',t[1],t[3])
    elif t[2] == '-':
        t[0] = ('MINUS',t[1],t[3])
    elif t[2] == '*':
        t[0] = ('TIMES',t[1],t[3])
    elif t[2] == '/':
        t[0] = ('DIV',t[1],t[3])
    elif t[2] == '%':
        t[0] = ('MOD',t[1],t[3])
    elif t[2] == '^':
        t[0] = ('POWER',t[1],t[3])
    elif t[2] == '=':
        t[0] = ('EQUAL',t[1],t[3])
    elif t[2] == '!=':
        t[0] = ('NOT_EQUAL',t[1],t[3])
    elif t[2] == '>':
        t[0] = ('GREATER_THAN',t[1],t[3])
    elif t[2] == '>=':
        t[0] = ('GREATER_THAN_EQUAL',t[1],t[3])
    elif t[2] == '<':
        t[0] = ('LESS_THAN',t[1],t[3])
    elif t[2] == '<=':
        t[0] = ('LESS_THAN_EQUAL',t[1],t[3])
    elif t[2] == '&&':
        t[0] = ('AND',t[1],t[3])
    elif t[2] == '||':
        t[0] = ('OR',t[1],t[3])
    elif t[1] == '!':
        t[0] = ('NOT',t[1],t[3])


def p_error(p):
    print("Syntax error in input!")
    print(p)

