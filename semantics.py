from inspect import Parameter
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, IfStatement, MainFunction, Program, WhileStatement


types = ['integer','float','char','string','boolean','void']

class TypeError(Exception):
	pass
class Any(object):
	def __eq__(self,o):
		return True
	def __ne__(self,o):
		return False

class Context(object):
	def __init__(self,name=None):
		self.variables = [{}]
		self.functions = {}
	

	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name):
		return self.variables[name]
	
	def set_var(self,name,typ):
		self.variables[-1][name] = (typ,)
		self.var_count[name] = 0

contexts = []
functions = {
	'print':('void',[
			("a",Any())
		]),
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
			("a",'real')
		])
}

def pop():
	count = contexts[-1].var_count
	for v in count:
		if count[v] == 0:
			print("Warning: variable %s was declared, but not used." % v)
	contexts.pop()

def check_if_function(var):
	if var.lower() in functions and not is_function_name(var.lower()):
		raise Exception, "A function called %s already exists" % var
		
def is_function_name(var):
	for i in contexts[::-1]:
		if i.name == var:
			return True
	return False
		
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			c.var_count[var] += 1
			return c.get_var(var)
	raise Exception, "Variable %s is referenced before assignment" % var
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception, "Variable %s already defined" % var
	else:
		now.set_var(var,typ.lower())
	
def get_params(node):
	if node.type == "parameter":
		return [check(node.args[0])]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
		return l
		

def is_node(n):
	return hasattr(n,"type")

def check(node):
	if not is_node(node):
		if hasattr(node,"__iter__") and type(node) != type(""):
			for i in node:
				check(i)
		else:
			return node
	else:
		if node.type in ['identifier']:
			return node.args[0]
			
		elif node.type in ['var_list','statement_list','function_list']:
			return check(node.args)
			
		elif node.type in ["program","block"]:
			contexts.append(Context())
			check(node.args)
			pop()
			
		elif node.type == "var":
			var_name = node.args[0].args[0]
			var_type = node.args[1].args[0]
			set_var(var_name, var_type)
			
		elif node.type in ['function','procedure']:
			head = node.args[0]
			name = head.args[0].args[0].lower()
			check_if_function(name)
			
			if len(head.args) == 1:
				args = []
			else:
				args = flatten(head.args[1])
				args = map(lambda x: (x.args[0].args[0],x.args[1].args[0]), args)
				
			if node.type == 'procedure':
				rettype = 'void'
			else:
				rettype = head.args[-1].args[0].lower()
				
			functions[name] = (rettype,args)
			
			
			contexts.append(Context(name))
			for i in args:
				set_var(i[0],i[1])
			check(node.args[1])
			pop()
			
		elif node.type in ["function_call","function_call_inline"]:
			fname = node.args[0].args[0].lower()
			if fname not in functions:
				raise Exception, "Function %s is not defined" % fname
			if len(node.args) > 1:
				args = get_params(node.args[1])
			else:
				args = []
			rettype,vargs = functions[fname]
		
			if len(args) != len(vargs):
				raise Exception, "Function %s is expecting %d parameters and got %d" % (fname, len(vargs), len(args))
			else:
				for i in range(len(vargs)):
					if vargs[i][1] != args[i]:
						raise Exception, "Parameter #%d passed to function %s should be of type %s and not %s" % (i+1,fname,vargs[i][1],args[i])
			
			return rettype
			
		elif node.type == "assign":	
				varn = check(node.args[0]).lower()
				if is_function_name(varn):
					vartype = functions[varn][0]
				else:
					if not has_var(varn):
						raise Exception, "Variable %s not declared" % varn
					vartype = get_var(varn)
				assgntype = check(node.args[1])
				
				if vartype != assgntype:
					raise Exception, "Variable %s is of type %s and does not support %s" % (varn, vartype, assgntype)
				
				
		elif node.type == 'and_or':
			op = node.args[0].args[0]
			for i in range(1,2):
				a = check(node.args[i])
				if a != "boolean":
					raise Exception, "%s requires a boolean. Got %s instead." % (op,a)

			
		elif node.type == "op":
			
			op = node.args[0].args[0]
			vt1 = check(node.args[1])
			vt2 = check(node.args[2])

			if vt1 != vt2:
				raise Exception, "Arguments of operation '%s' must be of the same type. Got %s and %s." % (op,vt1,vt2)
				
			if op in ['mod','div']:
				if vt1 != 'integer':
					raise Exception, "Operation %s requires integers." % op
			
			if op == '/':
				if vt1 != 'real':
					raise Exception, "Operation %s requires reals." % op
				
			if op in ['=','<=','>=','>','<','<>']:
				return 'boolean'
                
			else:
				return vt1	
			
				
		elif node.type in ['if','while','repeat']:
			if node.type == 'repeat':
				c = 1
			else:
				c = 0
			t = check(node.args[c])
			if t != 'boolean':
				raise Exception, "%s condition requires a boolean. Got %s instead." % (node.type,t)
			
			# check body
			check(node.args[1-c])
			
			# check else
			if len(node.args) > 2:
				check(node.args[2])
				
			
		elif node.type == 'for':
			contexts.append(Context())
			v = node.args[0].args[0].args[0].lower()
			set_var(v,'INTEGER')
			
			st = node.args[0].args[1].args[0].type.lower()
			if st != 'integer':
				raise Exception, 'For requires a integer as a starting value'
			
			fv = node.args[2].args[0].type.lower()
			if fv != 'integer':
				raise Exception, 'For requires a integer as a final value'
			
			check(node.args[3])
			
			pop()
			
		elif node.type == 'not':
			return check(node.args[0])
			
		elif node.type == "element":
			if node.args[0].type == 'identifier':
				return get_var(node.args[0].args[0])
			elif node.args[0].type == 'function_call_inline':
				return check(node.args[0])
			else:
				if node.args[0].type in types:
					return node.args[0].type
				else:
					return check(node.args[0])
			
			
		else:
			print( "semantic missing:", node.type)
			

def verify(ctx: Context, node):
    if node["Program"] == "Program":
        for decl in node["global_vars"]:
            verify(ctx, decl)
        for fun in node["functions"]:
            verify(ctx, fun)
    elif node["nt"] == "vardecl":
        name = node["name"]
        if ctx.has_var(name):
            raise TypeError("Variable %s already declared" % name)
        ctx.set_var(name, node["type"])
			

example_tree = Program(
    main_block_sequence=[
        Declaration(
            declaration_type='val',
            id='unsorted',
            type_specifier='[float]',
            expression=FunctionCall(
                id='getArrayRandomFloats',
                param_list=None
            )
        ),
        FunctionDeclaration(
            declaration_type='ffi',
            id='float_array_length',
            param_list=Parameter(
                declaration_type='val',
                id='arr',
                type_specifier='[float]'
            ),
            return_type='int',
            body=None
        ),
        FunctionDeclaration(
            declaration_type='function',
            id='bubble_sort',
            param_list=Parameter(
                declaration_type='val',
                id='arr',
                type_specifier='[float]'
            ),
            return_type='[float]',
            body=[
                Declaration(
                    declaration_type='var',
                    id='sorted',
                    type_specifier='[float]',
                    expression='arr'
                ),
                Declaration(
                    declaration_type='var',
                    id='n',
                    type_specifier='int',
                    expression=FunctionCall(
                        id='float_array_length',
                        param_list=['sorted']
                    )
                ),
                Declaration(
                    declaration_type='var',
                    id='swapped',
                    type_specifier='bool',
                    expression='true'
                ),
                WhileStatement(
                    condition='swapped',
                    block_seq=[
                        Declaration(
                            declaration_type='update',
                            id='swapped',
                            type_specifier=None,
                            expression='false'
                        ),
                        Declaration(
                            declaration_type='var',
                            id='i',
                            type_specifier='int',
                            expression=0
                        ),
                        WhileStatement(
                            condition=BinaryOperators(
                                operator='<',
                                left_operand='i',
                                right_operand=BinaryOperators(
                                    operator='-',
                                    left_operand='n',
                                    right_operand=1
                                )
                            ),
                            block_seq=[
                                IfStatement(
                                    condition=BinaryOperators(
                                        operator='>',
                                        left_operand=ArrayAccess(
                                            ID='sorted',
                                            index='i'
                                        ),
                                        right_operand=ArrayAccess(
                                            ID='sorted',
                                            index=BinaryOperators(
                                                operator='+',
                                                left_operand='i',
                                                right_operand=1
                                            )
                                        )
                                    ),
                                    thenBlock=[
                                        Declaration(
                                            declaration_type='var',
                                            id='temp',
                                            type_specifier='float',
                                            expression=ArrayAccess(
                                                ID='sorted',
                                                index='i'
                                            )
                                        ),
                                        Declaration(
                                            declaration_type='update',
                                            id=ArrayAccess(
                                                ID='sorted',
                                                index='i'
                                            ),
                                            type_specifier=None,
                                            expression=ArrayAccess(
                                                ID='sorted',
                                                index=BinaryOperators(
                                                    operator='+',
                                                    left_operand='i',
                                                    right_operand=1
                                                )
                                            )
                                        ),
                                        Declaration(
                                            declaration_type='update',
                                            id=ArrayAccess(
                                                ID='sorted',
                                                index=BinaryOperators(
                                                    operator='+',
                                                    left_operand='i',
                                                    right_operand=1
                                                )
                                            ),
                                            type_specifier=None,
                                            expression='temp'
                                        ),
                                        Declaration(
                                            declaration_type='update',
                                            id='swapped',
                                            type_specifier=None,
                                            expression='true'
                                        )
                                    ],
                                    elseBlock=None
                                ),
                                Declaration(
                                    declaration_type='update',
                                    id='i',
                                    type_specifier=None,
                                    expression=BinaryOperators(
                                        operator='+',
                                        left_operand='i',
                                        right_operand=1
                                    )
                                )
                            ]
                        ),
                        Declaration(
                            declaration_type='update',
                            id='n',
                            type_specifier=None,
                            expression=BinaryOperators(
                                operator='-',
                                left_operand='n',
                                right_operand=1
                            )
                        )
                    ]
                ),
                Declaration(
                    declaration_type='update',
                    id='bubble_sort',
                    type_specifier=None,
                    expression='sorted'
                )
            ]
        ),
        MainFunction(
            body=[
                Declaration(
                    declaration_type='val',
                    id='sorted',
                    type_specifier='[float]',
                    expression=FunctionCall(
                        id='bubble_sort',
                        param_list=['unsorted']
                    )
                ),
                Declaration(
                    declaration_type='var',
                    id='i',
                    type_specifier='int',
                    expression=BinaryOperators(
                        operator='-',
                        left_operand=FunctionCall(
                            id='float_array_length',
                            param_list=['sorted']
                        ),
                        right_operand=1
                    )
                ),
                WhileStatement(
                    condition=BinaryOperators(
                        operator='>=',
                        left_operand='i',
                        right_operand=0
                    ),
                    block_seq=[
                        FunctionCall(
                            id='print_float',
                            param_list=[
                                ArrayAccess(
                                    ID='sorted',
                                    index='i'
                                )
                            ]
                        ),
                        Declaration(
                            declaration_type='update',
                            id='i',
                            type_specifier=None,
                            expression=BinaryOperators(
                                operator='-',
                                left_operand='i',
                                right_operand=1
                            )
                        )
                    ]
                )
            ]
        )
    ]
)
verify(Context(), example_tree)