from dataclasses import dataclass


start = 'program'

precedence = (
    ('left', 'COMMA'),
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUAL', 'NOT_EQUAL'),
    ('nonassoc', 'GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),
    ('right', 'POWER'),
    ('right', 'NOT'),
    ('left', 'LPAREN', 'RPAREN'),  # Parentheses
)


#ACEDER A UM ARRAY
@dataclass
class Expression():
     pass

@dataclass
class BinaryOperators():
    operator: str
    left_operand: Expression
    right_operand: Expression

@dataclass
class UnaryOperators():
    operator: str
    operand: Expression

@dataclass
class TypeClass():
    type: str

@dataclass
class ArrayLiterals():
    elements: list

@dataclass
class ArrayAccess():
    ID: str
    index: list

# @dataclass
# class ArrayType():
#     type: str

@dataclass
class Declaration(): 
    declaration_type: str
    id: str  
    type_specifier: str
    expression: Expression   

@dataclass
class FunctionDeclaration():
    declaration_type: str
    id: str
    param_list: list
    return_type: str
    body: list

@dataclass
class MainFunction():
    body: list

@dataclass
class FunctionParamList():
    lista: list

@dataclass
class Parameter():
    declaration_type: str
    id: str  
    type_specifier: str


@dataclass
class FunctionCall():
    id: str 
    param_list: list
    
@dataclass
class WhileStatement():
    condition: Expression
    block_seq: list

@dataclass
class IfStatement():
    condition: Expression
    thenBlock: list
    elseBlock: list

@dataclass
class Comment():
    comment: str

@dataclass
class Program():
    main_block_sequence: list

@dataclass
class Identifier():
    id: str

@dataclass
class Literal():
    type: str
    value: str

def p_program(t):
    """program : main_block_sequence """
    if len(t) == 2:
        t[0] = Program(main_block_sequence=t[1])

def p_main_block_sequence(t):
	"""main_block_sequence : main_block main_block_sequence
	                        | main_block"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = t[1] + t[2]

def p_comment(t):
    """comment : COMMENT STRING_LITERAL"""
    t[0] = Comment(comment=t[2])


def p_main_block(t):
	"""main_block : constant_declaration
     | variable_declaration 
     | var_const_update
	 | function_declaration 
     | main_function
     | comment
	"""
	if len(t) > 1:
		t[0] = [t[1]]
    
#VAL DECLARATION
def p_constant_declaration(t):
    """constant_declaration : VAL ID COLON types ASSIGN expression SEMICOLON"""
    t[0] = Declaration(declaration_type=t[1], id= t[2], type_specifier= t[4], expression= t[6])

#VAR DECLARATION
def p_variable_declaration(t):
    """variable_declaration : VAR ID COLON types ASSIGN expression SEMICOLON"""
    t[0] = Declaration(declaration_type=t[1], id= t[2], type_specifier= t[4], expression= t[6])

#VAR CONST UPDATE
def p_var_const_update(t):
    """var_const_update :  ID ASSIGN expression SEMICOLON
                        | arrayaccess ASSIGN expression SEMICOLON"""
    t[0] = Declaration(declaration_type="update", id= t[1], type_specifier= None, expression= t[3])

#FUNCTION DECLARATION
def p_function_declaration(t):
    """function_declaration : FUNCTION ID LPAREN function_param_list RPAREN COLON types SEMICOLON
    |  FUNCTION ID LPAREN function_param_list RPAREN COLON types LBRACE function_body RBRACE"""
    if len(t) == 9:
        t[0] = FunctionDeclaration(declaration_type="ffi", id= t[2], param_list= t[4], return_type= t[7], body=None)
    else:
        t[0] = FunctionDeclaration(declaration_type="function", id= t[2], param_list= t[4], return_type= t[7], body=t[9])
    
def p_main_function(t):
    """main_function : FUNCTION MAIN LPAREN function_param_list RPAREN LBRACE function_body RBRACE"""
    t[0] = MainFunction(body=t[7])

def p_function_param_list(t):
    """function_param_list : function_param_list_aux
                           |"""
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = None

def p_function_param_list_aux(t):
    """function_param_list_aux : parameter COMMA function_param_list_aux
                            | parameter"""
    if len(t) == 4:
        if isinstance(t[3], list):
            t[0] = [t[1]] + t[3]
        else:
            t[0] = [t[1], t[3]]
    else:
        t[0] = [t[1]]

def p_parameter(t):
    """ parameter : VAL ID COLON types
                  | VAR ID COLON types"""
    if t[1] == 'var':
        t[0] = Parameter(declaration_type=t[1], id= t[2], type_specifier = t[4])
    else:

        t[0] = Parameter(declaration_type=t[1], id= t[2], type_specifier = t[4])

#FUNCTION CALL
def p_function_call(t):
    """function_call : ID LPAREN function_param_list_call RPAREN 
                     | ID LPAREN RPAREN 
    """
    if len(t) == 5:
        t[0] = FunctionCall(id = t[1], param_list = t[3]) 
    else:
        t[0] = FunctionCall(id = t[1], param_list = None)


def p_function_param_list_call(t):
    """function_param_list_call : expression COMMA function_param_list_call
                                | expression"""
    if len(t) == 4:
        if isinstance(t[3], list):
            t[0] = [t[1]] + t[3]
        else:
            t[0] = [t[1], t[3]]
    else:
        t[0] = [t[1]]

#TO GET THE FUNCTION BODY
def p_function_body(t):
    """function_body : block_sequence"""
    t[0] = t[1]
    

def p_block_sequence(t):
	"""block_sequence : block block_sequence
	 | block"""
	if len(t) == 2:
		t[0] = [t[1]]
	else:
		t[0] = [t[1]] + t[2]

def p_block(t):
	"""block : constant_declaration
     | variable_declaration 
     | var_const_update
	 | if_block
	 | while_block
	 | function_call SEMICOLON
     | comment
	"""
	if len(t) > 1:
		t[0] = t[1]

def p_if_block(t):
    """if_block : IF expression LBRACE block_sequence RBRACE ELSE LBRACE block_sequence RBRACE
	            | IF expression LBRACE block_sequence RBRACE 
	"""
    print(t[2])
    if len(t) == 10:
        t[0] = IfStatement(condition=t[2], thenBlock= t[4], elseBlock=t[8])
    else:
        t[0] = IfStatement(condition=t[2], thenBlock= t[4], elseBlock=None)
	
def p_while_block(t):
    """while_block : WHILE expression LBRACE block_sequence RBRACE"""
    t[0] = WhileStatement(condition=t[2], block_seq=t[4])

#FALTA OS ARRAYS E SE CALHAR INCLUIR O CHAR
def p_types(t):
    """types : defaulttype
            | LSQUARE arraytype RSQUARE"""
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = "["+t[2]+"]"

def p_defaultype(t):
    """defaulttype : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | VOID_TYPE
            | CHAR_TYPE"""
    t[0] = t[1]

def p_arraytype(t):
    """arraytype : LSQUARE arraytype RSQUARE
            | INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | VOID_TYPE
            """
    if len(t)>2:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0] = t[1]
        
def p_identifier(t):
    '''expression : ID '''
    t[0] = Identifier(id=t[1])


def p_arrayaccess(t):
    '''arrayaccess : ID LSQUARE expression RSQUARE arrayaccess2 
                    | function_call LSQUARE expression RSQUARE arrayaccess2'''
    if t[5] is not None:
        t[0] = ArrayAccess(ID=t[1], index=[t[3]] + t[5])
    else:
        t[0] = ArrayAccess(ID=t[1], index=[t[3]])

def p_arrayaccess2(t):
    '''arrayaccess2 : LSQUARE expression RSQUARE arrayaccess2
                    | '''
    if len(t) == 5:
        print(t[2])
        if t[4] is not None:
            t[0] = [t[2]] + t[4]
        else:
            t[0] = [t[2]]


def p_integer_literal(t):
    """expression : INTEGER_LITERAL
                  | MINUS INTEGER_LITERAL %prec UMINUS"""
    if len(t) == 2:
        t[0] = Literal(type='int', value=t[1])
    else:
        t[0] = Literal(type='int', value=-t[2])
    
def p_float_literal(t):
    """expression : FLOAT_LITERAL
                  | MINUS FLOAT_LITERAL %prec UMINUS"""
    if len(t) == 2:
        t[0] = Literal(type='float', value=t[1])
    else:
        t[0] = Literal(type='float', value=-t[2])

def p_string_literal(t):
    """expression : STRING_LITERAL"""
    t[0] = Literal(type='string', value=t[1])

def p_bool_literal(t):
    """expression : BOOL_LITERAL"""
    t[0] = Literal(type='bool', value=t[1])

def p_char_literal(t):
    """expression : CHAR_LITERAL"""
    t[0] = Literal(type='char', value=t[1])

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
                  | function_call
                  | arrayaccess
                  | LPAREN expression RPAREN'''
    if len(t) == 2:
        t[0] = t[1]
    elif t[2] == '+':
        t[0]  = BinaryOperators(operator='+', left_operand=t[1], right_operand=t[3])
    elif t[2] == '-':
        t[0]  = BinaryOperators(operator='-', left_operand=t[1], right_operand=t[3])
    elif t[2] == '*':
        t[0]  = BinaryOperators(operator='*', left_operand=t[1], right_operand=t[3])
    elif t[2] == '/':
        t[0]  = BinaryOperators(operator='/', left_operand=t[1], right_operand=t[3])
    elif t[2] == '%':
        t[0]  = BinaryOperators(operator='%', left_operand=t[1], right_operand=t[3])
    elif t[2] == '^':
        t[0]  = BinaryOperators(operator='^', left_operand=t[1], right_operand=t[3])
    elif t[2] == '=':
        t[0]  = BinaryOperators(operator='=', left_operand=t[1], right_operand=t[3])
    elif t[2] == '!=':
        t[0]  = BinaryOperators(operator='!=', left_operand=t[1], right_operand=t[3])
    elif t[2] == '>':
        t[0]  = BinaryOperators(operator='>', left_operand=t[1], right_operand=t[3])
    elif t[2] == '>=':
        t[0]  = BinaryOperators(operator='>=', left_operand=t[1], right_operand=t[3])
    elif t[2] == '<':
        t[0]  = BinaryOperators(operator='<', left_operand=t[1], right_operand=t[3])
    elif t[2] == '<=':
        t[0]  = BinaryOperators(operator='<=', left_operand=t[1], right_operand=t[3])
    elif t[2] == '&&':
        t[0]  = BinaryOperators(operator='&&', left_operand=t[1], right_operand=t[3])
    elif t[2] == '||':
        t[0]  = BinaryOperators(operator='||', left_operand=t[1], right_operand=t[3])
    elif t[1] == '!':
        t[0]  = UnaryOperators(operator='!', operand=t[2])


def p_error(p):
    print("Syntax error in input!")
    print(p)

