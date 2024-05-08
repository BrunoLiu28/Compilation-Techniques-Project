import copy
import re
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, Literal, MainFunction, Parameter, Program, UnaryOperators, WhileStatement
pass1 = True
#FAZER 2 PASSAGENS PELO PROGRAMA

#PRIMEIRA PASSAGEM VERIFICA VARIAVEIS GLOBAIS mas nao funcoes(?)

def verify(node):
    global pass1
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            verify(block)

        pass1 = False  #SEGUNDA PASSAGEM
        for block in node.main_block_sequence:
            if isinstance(block, Declaration) or (isinstance(block, FunctionDeclaration) and block.declaration_type == "ffi"):
                pass
            else:
                verify(block)
    elif isinstance(node, Declaration):
        if pass1: #Global variables
            if node.type_specifier == "int":
                print(f"@{node.id} = dso_local global i32 0, align 4")
            elif node.type_specifier == "float":
                valorDoCharEmHex = float_to_hex(node.expression)
                print(f"@{node.id} = dso_local global float {valorDoCharEmHex}, align 1")
            elif node.type_specifier == "bool":
                print(f"@{node.id} = dso_local global i1 0, align 4")
            elif node.type_specifier == "string":
                #devolver o valor mesmo no node.expression
                print(f"@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}", align 1")
            elif node.type_specifier == "char":
                valorDoCharEmHex = hex(ord(node.expression))[2:]
                print(f"@{node.id} = dso_local global i8 {valorDoCharEmHex}, align 1")
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
    elif isinstance(node, ArrayAccess):	#FALTA FAZER ESTE
        if not ctx.has_var(node.ID):
            raise TypeError(f"Variable {node.ID} is not declared")
        if verify(ctx, node.index) != "int":
            raise TypeError(f"Array index should be an integer and not {verify(ctx, node.index)}")
        
        
        return get_type(ctx.get_varValType(node.ID))
        pass
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
        # print(node)
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


def float_to_hex(f):
    # Convert the float to its binary representation
    bits = ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in bytearray(struct.pack('>d', f)))
    
    # Extract sign, exponent, and significand parts
    sign = bits[0]
    exponent = bits[1:12]
    significand = bits[12:]
    
    # Format the result as hexadecimal
    hex_representation = hex(int(sign + exponent + significand, 2))
    
    return hex_representation