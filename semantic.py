from inspect import Parameter
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, IfStatement, MainFunction, Program, WhileStatement

ast = Program(main_block_sequence=[Declaration(declaration_type='var', id='a', type_specifier='[float]', expression='arr'), Declaration(declaration_type='var', id='b', type_specifier='int', expression=FunctionCall(id='float_array_length', param_list=['sorted'])), Declaration(declaration_type='var', id='c', type_specifier='bool', expression='true'), Declaration(declaration_type='var', id='d', type_specifier='int', expression='arr'), Declaration(declaration_type='var', id='e', type_specifier='string', expression='true'), Declaration(declaration_type='var', id='f', type_specifier='char', expression='arr'), Declaration(declaration_type='var', id='g', type_specifier='float', expression='true'), Declaration(declaration_type='var', id='g', type_specifier='string', expression='true')])
ast1 = Program(main_block_sequence=[Declaration(declaration_type='val', id='unsorted', type_specifier='[float]', expression=FunctionCall(id='getArrayRandomFloats', param_list=None)), FunctionDeclaration(declaration_type='ffi', id='float_array_length', param_list=[Parameter(declaration_type='val', id='arr', type_specifier='[float]'), Parameter(declaration_type='val', id='args', type_specifier='[string]')], return_type='int', body=None), FunctionDeclaration(declaration_type='function', id='bubble_sort', param_list=[Parameter(declaration_type='val', id='arr', type_specifier='[float]'), Parameter(declaration_type='val', id='args', type_specifier='[string]')], return_type='[float]', body=[Declaration(declaration_type='var', id='i', type_specifier='int', expression=0)])])

types = ['integer','float','char','string','boolean','void']

class TypeError(Exception):
	pass

class Context(object):
    def __init__(self,name=None):
        self.variables = {}
        self.varOrVal = {}
        self.var_count = {}
        self.name = name
    def has_var(self,name):
        return name in self.variables
    def get_var(self,name):
        return self.variables[name]
    
    def set_var(self, name, typ, varOrVal):
        self.variables[name] = typ
        self.varOrVal[name] = varOrVal
        self.var_count[name] = 0

    def get_varOrVal(self, name):
        return self.varOrVal[name]


contexts = []
functions = {     #EXAMPLE DPS ALTERAR ISTO
	'print_int':('void',[
			("a",'integer')
		]),
	'print_string':('void',[
			("a",'string')
		]),
	'print_float':('void',[
			("a",'float')
		]),
	'print_boolean':('void',[
			("a",'bool')
		])
}

def verify(varCtx: Context, funcCtx: Context, node):
    if isinstance(node, Program):
        for func in node.main_block_sequence:
            verify(varCtx, funcCtx, func)
        # for decl in node["global_vars"]:
        #     verify(ctx, decl)
        # for fun in node["functions"]:
        #     verify(ctx, fun)
    elif isinstance(node, Declaration):
        name = node.id
        if node.declaration_type == "update":
            if not varCtx.has_var(name):
                  raise TypeError("Variable %s doesnt exist impossible to update" % name)
            #variavel existe, verificar se é var ou val
            aux = varCtx.get_var[name]
            if varCtx.get_varOrVal(name) == "val":
                raise TypeError("Variable %s is a val, impossible to update" % name)
            #VERIFICAR A EXPRESSION PARA VER SE CONDIZ COM O TIPO
            
        if varCtx.has_var(name):
            raise TypeError("Variable %s already declared" % name)
        varCtx.set_var(name, node.type_specifier, node.declaration_type)
    elif isinstance(node, ArrayAccess):	
        pass
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        name = node.id
        type = node.return_type
        if funcCtx.has_var(name):
            raise TypeError("function %s already declared" % name)
        funcCtx.set_var(name, node.type_specifier)
        for param in node.param_list:
            print(param)
            varCtx.set_var(param.id , param.type_specifier)

        for expr in node.body:
            verify(varCtx, funcCtx, expr)
    elif isinstance(node, MainFunction):	
            pass
    elif isinstance(node, FunctionCall):
        name = node.id
        if not funcCtx.has_var(name):
             raise Exception, "Function %s is not defined" % name
        
        if len(node.param_list) > 1:
            args = (node.param_list[1])    
        else:
            args = []

        rettype, vargs = functions[name]
        if len(args) != len(vargs):
            raise Exception("Function %s is expecting %d parameters and got %d" % (name, len(vargs), len(args)))
        else:
            for i in range(len(vargs)):
                #OBTER O ARGS E O SEU TIPO NO CONTEXTO E VERIFICAR O TIPO NO ARGS COM O TIPO DA FUNCAO
                if vargs[i][1] != args[i].type:
                    raise Exception("Parameter #%d passed to function %s should be of type %s and not %s" % (i+1, name, vargs[i][1], args[i]))
        #VERIFICAR O TYPE NO RETURN?
    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(node.left_operand)
        vt2 = verify(node.right_operand)
        if vt1 != vt2:
            raise Exception, "Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2)
        if op in ['%','div']:
            if vt1 != 'integer':
                raise Exception, "Operation %s requires integers." % op
        if op == '/':
            if vt1 != 'real':  #VER ISTO
                raise Exception("%s requires reals." % op)
        if op in ['=','<=','>=','>','<','<>']:
            return 'boolean'
        if op in ['&&','||']:
            if verify(vt1) != "boolean":
                raise Exception("%s requires a boolean. Got %s instead." % (op, verify(vt1)))
            if verify(vt2) != "boolean":
                raise Exception("%s requires a boolean. Got %s instead." % (op, verify(vt1)))
        elif isinstance(node, IfStatement):	
            pass
        elif isinstance(node, WhileStatement):	
            pass
        else:
            return vt1


verify(Context(),Context(),  ast1)