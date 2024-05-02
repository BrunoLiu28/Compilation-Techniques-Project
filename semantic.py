from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, IfStatement, MainFunction, Program, WhileStatement

ast = Program(main_block_sequence=[Declaration(declaration_type='var', id='a', type_specifier='[float]', expression='arr'), Declaration(declaration_type='var', id='b', type_specifier='int', expression=FunctionCall(id='float_array_length', param_list=['sorted'])), Declaration(declaration_type='var', id='c', type_specifier='bool', expression='true'), Declaration(declaration_type='var', id='d', type_specifier='int', expression='arr'), Declaration(declaration_type='var', id='e', type_specifier='string', expression='true'), Declaration(declaration_type='var', id='f', type_specifier='char', expression='arr'), Declaration(declaration_type='var', id='g', type_specifier='float', expression='true'), Declaration(declaration_type='var', id='g', type_specifier='string', expression='true')])


types = ['integer','float','char','string','boolean','void']

class TypeError(Exception):
	pass

class Context(object):
	def __init__(self,name=None):
		self.variables = {}
		self.var_count = {}
		self.name = name
	
	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name):
		return self.variables[name]
	
	def set_var(self,name,typ):
		self.variables[name] = typ
		self.var_count[name] = 0

contexts = []

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
        if varCtx.has_var(name):
            raise TypeError("Variable %s already declared" % name)
        varCtx.set_var(name, node.type_specifier)
    # elif isinstance(node, FunctionCall):
    #     pass
    elif isinstance(node, FunctionDeclaration):
        name = node.id
        type = node.declaration_type
        if funcCtx.has_var(name):
            raise TypeError("function %s already declared" % name)
        funcCtx.set_var(name, node.type_specifier)
        for expr in node.body:
            verify(varCtx, funcCtx, expr)
        pass


verify(Context(),Context(),  ast)