import copy
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, Literal, MainFunction, Parameter, Program, UnaryOperators, WhileStatement

ast = Program(main_block_sequence=[FunctionDeclaration(declaration_type='function', id='maxRangeSquared', param_list=[Parameter(declaration_type='var', id='mi', type_specifier='float'), Parameter(declaration_type='val', id='ma', type_specifier='int')], return_type='int', body=[Declaration(declaration_type='var', id='current_max', type_specifier='int', expression=BinaryOperators(operator='^', left_operand=Identifier(id='mi'), right_operand=Literal(type='integer', value=2)))])])

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

    def var_pop(self):
        self.variables.pop()

    def has_func(self, id):
        return id in self.functions

contexts = []


def verify(ctx: Context, node):
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            verify(ctx, block)
    elif isinstance(node, Declaration):
        name = node.id
        if node.declaration_type == "update":
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
        pass
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        print(node)
        name = node.id
        type = node.return_type
        if ctx.has_func(name):
            raise TypeError(f"function {name} already declared")
        ctx.add_func(name, type, node.param_list)
        print(node.param_list)
        new_ctx = copy.deepcopy(ctx)
        for param in node.param_list:
            verify(new_ctx, param)
            
        if type != "void":
            new_ctx.add_var(name, type, "var")

        for expr in node.body:
            verify(new_ctx, expr)
        
    elif isinstance(node, MainFunction):
        print(node)
        name = "main"
        if ctx.has_func(name):
            raise TypeError(f"function {name} already declared")
        ctx.add_func(name, "void", [Parameter(declaration_type='var', id='args', type_specifier='[string]')])

        new_ctx = copy.deepcopy(ctx)

        for expr in node.body:
            verify(new_ctx, expr)
    elif isinstance(node, FunctionCall):    ## VER ISTOOOOOOOOO!!!!!!
        name = node.id
        if not ctx.has_func(name):
             raise TypeError(f"Function {name} is not defined")
        
        # if len(node.param_list) > 1:
        #     args = (node.param_list[1])    
        # else:
        #     args = []

        # rettype, vargs = ctx.get_func[name]
        # if len(args) != len(vargs):
        #     raise TypeError(f"Function {name} is expecting {len(vargs)} parameters and got {len(args)}")
        # else:
        #     for i in range(len(vargs)):
        #         #OBTER O ARGS E O SEU TIPO NO CONTEXTO E VERIFICAR O TIPO NO ARGS COM O TIPO DA FUNCAO
        #         if vargs[i][1] != args[i].type:
        #             raise TypeError(f"Parameter {i+1} passed to function {name} should be of type {vargs[i][1]} and not {args[i]}")

        if len(node.param_list) != len(ctx.get_funcParam(name)):
            raise TypeError(f"function {name} called with wrong number of arguments")
        for arg, param in zip(node.param_list, ctx.get_funcParam(name)):
            if verify(ctx, arg) != param.type_specifier:
                raise TypeError(f"function {name} called with wrong argument types")

        return ctx.get_funcType(name)

    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(ctx, node.left_operand)
        # print(vt1)
        vt2 = verify(ctx, node.right_operand)
        # print(vt2)
        # if vt1 != vt2:
        #     raise TypeError(f"Arguments of operation '{op}' must be of the same type. Got {vt1} and {vt2}.")
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
        if op == '=':
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
                raise TypeError(f"{op} requires a boolean. Got {verify(vt1)} instead.")
            if verify(ctx ,vt2) != "bool":
                raise TypeError(f"{op} requires a boolean. Got {verify(vt1)} instead.")
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
        if verify(ctx ,condition) != 'bool':
            raise TypeError(f"If condition requires a boolean. Got {verify(condition)} instead.")
        for a in node.thenBlock:
            verify(ctx ,a)
        if node.elseBlock != None:
            for a in node.elseBlock:
                verify(ctx ,a)
    
    elif isinstance(node, WhileStatement):	
        condition = node.condition
        if verify(ctx ,condition) != 'bool':
            raise TypeError(f"WHILE condition requires a boolean. Got {verify(condition)} instead.")
        for a in node.block_seq:
            verify(ctx ,a)
    elif isinstance(node, Parameter):	
        ctx.add_var(node.id, node.type_specifier, node.declaration_type)
    elif isinstance(node, Literal):
        return node.type
    else:
        print("semantic missing:", node.__class__.__name__)


# verify(Context(),  ast)
# print("OK!")