import copy
import re
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, Literal, MainFunction, Parameter, Program, UnaryOperators, WhileStatement

class TypeError(Exception):
	pass

class Context(object):


    def __init__(self,name=None):
        self.variables = {}
        self.functions = {}

        self.add_func('print_int', 'void', [Parameter(declaration_type='var', id='any', type_specifier='int')])
        self.add_func('print_int', 'void', [Parameter(declaration_type='val', id='any', type_specifier='int')])

        self.add_func('print_float', 'void', [Parameter(declaration_type='var', id='any', type_specifier='float')])
        self.add_func('print_float', 'void', [Parameter(declaration_type='val', id='any', type_specifier='float')])

        self.add_func('print_bool', 'void', [Parameter(declaration_type='var', id='any', type_specifier='bool')])
        self.add_func('print_bool', 'void', [Parameter(declaration_type='val', id='any', type_specifier='bool')])

        self.add_func('print_char', 'void', [Parameter(declaration_type='var', id='any', type_specifier='char')])
        self.add_func('print_char', 'void', [Parameter(declaration_type='val', id='any', type_specifier='char')])

        self.add_func('print', 'void', [Parameter(declaration_type='var', id='any', type_specifier='string')])
        self.add_func('print', 'void', [Parameter(declaration_type='val', id='any', type_specifier='string')])

    def has_var(self,id):
        return id in self.variables
    
    def get_var(self,id):
        return self.variables[id]
    
    def add_func(self, id, returnType, params):
        self.functions[id] = (returnType, params)

    def add_var(self, id, typ, varOrVal):
        self.variables[id] = (typ, varOrVal)

    #RETORNAR O PRIMEIRO ENCONTRADO
    def get_varOrVal(self, name):
        return self.variables[name][1]
    
    def get_varValType(self, name):
        return self.variables[name] [0]

    def get_func(self, name):
        return self.functions[name]
    
    def get_funcType(self, name):
        return self.functions[name][0]
    
    def get_funcParam(self, name):
        return self.functions[name][1]

    def has_func(self, id):
        return id in self.functions

contexts = []
pass1 = True
#FAZER 2 PASSAGENS PELO PROGRAMA


def verify(ctx: Context, node):
    global pass1
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            verify(ctx, block)
        
        pass1 = False  #SEGUNDA PASSAGEM
        for block in node.main_block_sequence:
            #IGNORAR DECLARATIONS E FUNCTIONDECLARATIONS
            if isinstance(block, Declaration) or (isinstance(block, FunctionDeclaration) and block.declaration_type == "ffi"):
                pass
            else:
                verify(ctx, block)
    elif isinstance(node, Declaration):
        if pass1 :
            name = node.id
            if node.declaration_type == "update":
                if isinstance(node.id, ArrayAccess):
                    if not ctx.has_var(node.id.ID):
                        raise TypeError(f"The global array {node.id.ID} doesnt exist impossible to update")
                    
                    if ctx.get_varOrVal(node.id.ID) == "val":
                        raise TypeError(f"The global array {node.id.ID} is a val, impossible to update")
                    
                    type = verify(ctx, node.id)
                    if type != verify(ctx, node.expression):
                        raise TypeError(f"The global array {node.id.ID} is of type {type} and not {verify(ctx, node.expression)}")
                    pass
                else:
                    if not ctx.has_var(name):
                        raise TypeError(f"The global variable {name} doesnt exist impossible to update")
                    #variavel existe, verificar se é var ou val
                    if ctx.get_varOrVal(name) == "val":
                        raise TypeError(f"The global variable {name} is a val, impossible to update")
                    expr = node.expression
                    if verify(ctx, expr) != ctx.get_varValType(name):
                        raise TypeError(f"The global variable {name} is of type {ctx.get_varValType(name)} and not {verify(ctx, expr)}")
            
            elif ctx.has_var(name):
                raise TypeError(f"The global variable {name} already declared")
            elif node.type_specifier != verify(ctx, node.expression):
                raise TypeError(f"The global variable {name} is of type {node.type_specifier} and not {verify(ctx, node.expression)}")
            else:
                ctx.add_var(name, node.type_specifier, node.declaration_type)
        else:
            name = node.id
            if node.declaration_type == "update":
                if isinstance(node.id, ArrayAccess):
                    if not ctx.has_var(node.id.ID):
                        raise TypeError(f"Array {node.id.ID} doesnt exist impossible to update")
                    
                    if ctx.get_varOrVal(node.id.ID) == "val":
                        raise TypeError(f"Array {node.id.ID} is a val, impossible to update")
                    
                    type = verify(ctx, node.id)
                    if type != verify(ctx, node.expression):
                        raise TypeError(f"Array {node.id.ID} is of type {type} and not {verify(ctx, node.expression)}")
                    pass
                else:
                    if not ctx.has_var(name):
                        raise TypeError(f"Variable {name} doesnt exist impossible to update")
                    #variavel existe, verificar se é var ou val
                    if ctx.get_varOrVal(name) == "val":
                        raise TypeError(f"Variable {name} is a val, impossible to update")
                    expr = node.expression
                    if verify(ctx, expr) != ctx.get_varValType(name):
                        raise TypeError(f"Variable {name} is of type {ctx.get_varValType(name)} and not {verify(ctx, expr)}")
            
            elif ctx.has_var(name):
                raise TypeError(f"Variable {name} already declared")
            elif node.type_specifier != verify(ctx, node.expression):
                raise TypeError(f"Variable {name} is of type {node.type_specifier} and not {verify(ctx, node.expression)}")
            else:
                ctx.add_var(name, node.type_specifier, node.declaration_type)
    elif isinstance(node, Identifier):
        if not ctx.has_var(node.id):
            raise TypeError(f"Variable {node.id} is not declared")
        return ctx.get_varValType(node.id)
    elif isinstance(node, ArrayAccess):
        if not ctx.has_var(node.ID):
            raise TypeError(f"Variable {node.ID} is not declared")
        if len(node.index) > 1:
            for index in node.index:
                if verify(ctx, index) != "int":
                    raise TypeError(f"Array index should be an integer and not {verify(ctx, index)}")
        
        countOriginalSize = ctx.get_varValType(node.ID).count('[') 
        if len(node.index) > countOriginalSize:
            raise TypeError(f"Array {node.ID} has {countOriginalSize} dimensions and you are trying to access {len(node.index)} dimensions")
       
        resultSize = countOriginalSize - len(node.index)
        base_type = get_type(ctx.get_varValType(node.ID))
        for _ in range(resultSize):
            base_type = "[" + base_type + "]"

        return base_type
        
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        #Se for FFI entra aqui
        name = node.id
        type = node.return_type
        if node.declaration_type == "ffi":
            
            name = node.id
            if ctx.has_func(name):
                raise TypeError(f"function {name} already declared")
            
            ctx.add_func(name, type, node.param_list)
        else: #funcao normal
            if pass1 == True:
                if ctx.has_func(name):
                    raise TypeError(f"function {name} already declared")
                ctx.add_func(name, type, node.param_list)
            else:
                new_ctx = copy.deepcopy(ctx)
                if node.param_list != None:
                    
                    for param in node.param_list:
                        verify(new_ctx, param)
                    
                if type != "void":
                    new_ctx.add_var(name, type, "var")

                for expr in node.body:
                    verify(new_ctx, expr)
        
    elif isinstance(node, MainFunction):
        name = "main"
        if pass1 == True:
            if ctx.has_func(name):
                raise TypeError(f"function {name} already declared")
            ctx.add_func(name, "void", [Parameter(declaration_type='var', id='args', type_specifier='[string]')])

        else:
            new_ctx = copy.deepcopy(ctx)
            for expr in node.body:
                verify(new_ctx, expr)
    elif isinstance(node, FunctionCall): 
        name = node.id
        if not ctx.has_func(name):
             raise TypeError(f"Function {name} is not defined")
        
        if ctx.get_funcParam(name) != None and node.param_list == None:
            raise TypeError(f"function {name} have arguments and you called it without arguments")
        elif ctx.get_funcParam(name) == None and node.param_list != None:
            raise TypeError(f"function {name} dont have arguments and you called it with arguments")
        
        if ctx.get_funcParam(name) == None and node.param_list == None:
            pass
        else:
            if len(node.param_list) != len(ctx.get_funcParam(name)):
                raise TypeError(f"function {name} called with wrong number of arguments")
            
            for arg, param in zip(node.param_list, ctx.get_funcParam(name)):
                if verify(ctx, arg) != param.type_specifier:
                    raise TypeError(f"function {name} called with wrong argument types")

        return ctx.get_funcType(name)

    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(ctx, node.left_operand)
        vt2 = verify(ctx, node.right_operand)
        if op in ['%','/', '*', '+', '-']:
            if vt1 == 'int' and not vt2 == 'int':
                raise TypeError(f"Operation {op} requires both to be integers.")
            if vt1 == 'float' and not vt2 == 'float':
                raise TypeError(f"Operation {op} requires both to be floats.")
            return vt1
        if op == '^':
            if vt1 == 'int' and not vt2 == 'int':
                raise TypeError(f"Operation {op} requires both to be integers.")
            if vt1 == 'float' and not vt2 == 'int':
                raise TypeError(f"Operation {op} requires both to be floats.")
            return vt1
        if op in ['=','!=']:
            if vt1 != vt2:
                raise TypeError(f"Operation {op} requires both type to be the same.")
            return 'bool'
        if op in ['<=','>=','>','<']:
            if vt1 == 'int' and not vt2 == 'int':
                raise TypeError(f"Operation {op} requires both to be integers.")
            if vt1 == 'float' and not vt2 == 'float':
                raise TypeError(f"Operation {op} requires both to be floats.")
            return 'bool'
        if op in ['&&','||']:
            if verify(ctx ,vt1) != "bool":
                raise TypeError(f"{op} requires a boolean. Got {verify(ctx, vt1)} instead.")
            if verify(ctx ,vt2) != "bool":
                raise TypeError(f"{op} requires a boolean. Got {verify(ctx, vt1)} instead.")
    elif isinstance(node, UnaryOperators):
        op = node.operator
        vt = verify(ctx ,node.operand)
        if op == '!':
            if vt != 'bool':
                raise TypeError(f"Operation {op} requires a boolean. Got {vt} instead.")
            return 'bool'
        if op == '-':
            if vt == 'int':
                return 'int'
            if vt == 'float':
                return 'float'
            raise TypeError(f"Operation {op} requires an integer or float. Got {vt} instead.")
    elif isinstance(node, IfStatement):
        condition = node.condition
        # print(condition)
        if verify(ctx ,condition) != 'bool':
            raise TypeError(f"If condition requires a boolean. Got {verify(ctx, condition)} instead.")
        for a in node.thenBlock:
            verify(ctx ,a)
        if node.elseBlock != None:
            for a in node.elseBlock:
                verify(ctx ,a)
    
    elif isinstance(node, WhileStatement):	
        condition = node.condition
        if verify(ctx ,condition) != 'bool':
            raise TypeError(f"WHILE condition requires a boolean. Got {verify(ctx, condition)} instead.")
        for a in node.block_seq:
            verify(ctx ,a)
    elif isinstance(node, Parameter):	
        ctx.add_var(node.id, node.type_specifier, node.declaration_type)
    elif isinstance(node, Literal):
        return node.type
    else:
        print("semantic missing:", node.__class__.__name__)


def get_type(type_string):
    match = re.search(r'\b(\w+)\b', type_string)
    if match:
        return match.group(1)
    else:
        return None


# verify(Context(),  ast)
# print("OK!")