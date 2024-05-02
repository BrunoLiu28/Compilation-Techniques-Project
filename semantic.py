from inspect import Parameter
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, MainFunction, Program, UnaryOperators, WhileStatement

ast = Program(main_block_sequence=[Declaration(declaration_type='var', id='a', type_specifier='[float]', expression='arr'), Declaration(declaration_type='var', id='b', type_specifier='int', expression=FunctionCall(id='float_array_length', param_list=['sorted'])), Declaration(declaration_type='var', id='c', type_specifier='bool', expression='true'), Declaration(declaration_type='var', id='d', type_specifier='int', expression='arr'), Declaration(declaration_type='var', id='e', type_specifier='string', expression='true'), Declaration(declaration_type='var', id='f', type_specifier='char', expression='arr'), Declaration(declaration_type='var', id='g', type_specifier='float', expression='true'), Declaration(declaration_type='var', id='g', type_specifier='string', expression='true')])
# ast1 = Program(main_block_sequence=[Declaration(declaration_type='val', id='unsorted', type_specifier='[float]', expression=FunctionCall(id='getArrayRandomFloats', param_list=None)), FunctionDeclaration(declaration_type='ffi', id='float_array_length', param_list=[Parameter(declaration_type='val', id='arr', type_specifier='[float]'), Parameter(declaration_type='val', id='args', type_specifier='[string]')], return_type='int', body=None), FunctionDeclaration(declaration_type='function', id='bubble_sort', param_list=[Parameter(declaration_type='val', id='arr', type_specifier='[float]'), Parameter(declaration_type='val', id='args', type_specifier='[string]')], return_type='[float]', body=[Declaration(declaration_type='var', id='i', type_specifier='int', expression=0)])])
ast2= Program(main_block_sequence=[Declaration(declaration_type='var', id='c', type_specifier='bool', expression='true'), Declaration(declaration_type='var', id='d', type_specifier='int', expression=Identifier(id='arr')), Declaration(declaration_type='var', id='e', type_specifier='string', expression='true'), Declaration(declaration_type='var', id='f', type_specifier='char', expression=Identifier(id='arr')), Declaration(declaration_type='var', id='g', type_specifier='float', expression='true'), Declaration(declaration_type='var', id='g', type_specifier='string', expression='true')])
ast3 = Program(main_block_sequence=[Declaration(declaration_type='var', id='c', type_specifier='bool', expression='true')])

types = ['integer','float','char','string','boolean','void']

class TypeError(Exception):
	pass

class Context(object):
    def __init__(self,name=None):
        self.variables = {}
        self.functions = {}

    def has_var(self,id):
        return id in self.variables
    
    def get_var(self,id):
        return self.variables[id]
    
    def add_func(self, id, returnType, params):
        self.variables[id] = (returnType, params)

    def add_var(self, id, typ, varOrVal):
        self.variables[id] = (typ, varOrVal)

    def get_varOrVal(self, name):
        return self.varOrVal[name][1]
    
    def get_varValType(self, name):
        return self.varOrVal[name][0]

    def get_func(self, name):
        return self.functions[name]

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
                  raise TypeError("Variable %s doesnt exist impossible to update" % name)
            #variavel existe, verificar se é var ou val
            if ctx.get_varOrVal(name) == "val":
                raise TypeError("Variable %s is a val, impossible to update" % name)
            expr = node.expression
            if verify(ctx, expr) != ctx.get_varValType[name]:
                raise TypeError("Variable %s is of type %s and not %s" % (name, ctx.get_var[name], verify(ctx, expr)))
        
        if ctx.has_var(name):
            raise TypeError("Variable %s already declared" % name)
        
        ctx.add_var(name, node.type_specifier, node.declaration_type)
    elif isinstance(node, Identifier):
        return ctx.get_varValType(node.id)
    elif isinstance(node, ArrayAccess):	
        pass
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        name = node.id
        type = node.return_type
        if ctx.has_func(name):
            raise TypeError("function %s already declared" % name)
        ctx.add_func(name, node.type_specifier)
        for param in node.param_list:
            print(param)
            ctx.set_var(param.id , param.type_specifier)

        for expr in node.body:
            verify(ctx, expr)
    elif isinstance(node, MainFunction):	
            pass
    elif isinstance(node, FunctionCall):
        name = node.id
        if not ctx.has_func(name):
             raise TypeError("Function %s is not defined" % name)
        
        if len(node.param_list) > 1:
            args = (node.param_list[1])    
        else:
            args = []

        rettype, vargs = ctx.ge[name]
        if len(args) != len(vargs):
            raise TypeError("Function %s is expecting %d parameters and got %d" % (name, len(vargs), len(args)))
        else:
            for i in range(len(vargs)):
                #OBTER O ARGS E O SEU TIPO NO CONTEXTO E VERIFICAR O TIPO NO ARGS COM O TIPO DA FUNCAO
                if vargs[i][1] != args[i].type:
                    raise TypeError("Parameter #%d passed to function %s should be of type %s and not %s" % (i+1, name, vargs[i][1], args[i]))

        return rettype

    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(node.left_operand)
        vt2 = verify(node.right_operand)
        if vt1 != vt2:
            raise TypeError("Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2))
        if op in ['%','/', '*', '+', '-']:
            if vt1 == 'integer' and not vt2 == 'integer':
                raise TypeError("Operation %s requires both to be integers." % op)
            if vt1 == 'float' and not vt2 == 'float':
                raise TypeError("Operation %s requires both to be floats." % op)
            return vt1
        if op == '^':
            if vt1 == 'integer' and not vt2 == 'integer':
                raise TypeError("Operation %s requires both to be integers." % op)
            if vt1 == 'float' and not vt2 == 'integer':
                raise TypeError( "Operation %s requires both to be floats." % op)
            return vt1
        if op == '=':
            if vt1 != vt2:
                raise TypeError( "Operation %s requires both type to be the same." % op)
            return 'boolean'
        if op in ['<=','>=','>','<']:
            if vt1 == 'integer' and not vt2 == 'integer':
                raise TypeError("Operation %s requires both to be integers." % op)
            if vt1 == 'float' and not vt2 == 'float':
                raise TypeError("Operation %s requires both to be floats." % op)
            return 'boolean'
        if op in ['&&','||']:
            if verify(vt1) != "boolean":
                raise TypeError("%s requires a boolean. Got %s instead." % (op, verify(vt1)))
            if verify(vt2) != "boolean":
                raise TypeError("%s requires a boolean. Got %s instead." % (op, verify(vt1)))
    elif isinstance(node, UnaryOperators):
        op = node.operator
        vt = verify(node.operand)
        if op == '!':
            if vt != 'boolean':
                raise TypeError("Operation %s requires a boolean. Got %s instead." % (op, vt))
            return 'boolean'
        if op == '-':
            if vt == 'integer':
                return 'integer'
            if vt == 'float':
                return 'float'
            raise TypeError("Operation %s requires an integer or float. Got %s instead." % (op, vt))
    elif isinstance(node, IfStatement):
        condition = node.condition
        if verify(condition) != 'boolean':
            raise TypeError("If condition requires a boolean. Got %s instead." % (verify(condition)))
        for a in node.thenBlock:
            verify(a)
        for a in node.elseBlock:
            verify(a)
    
    elif isinstance(node, WhileStatement):	
        condition = node.condition
        if verify(condition) != 'boolean':
            raise TypeError("WHILE condition requires a boolean. Got %s instead." % (verify(condition)))
        for a in node.block_seq:
            verify(a)
    else:
        print("semantic missing:", node.__class__.__name__)


verify(Context(),  ast2)
print("OK!")