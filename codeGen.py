import copy
import re
import struct
from interpretor import interpretor
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, Literal, MainFunction, Parameter, Program, UnaryOperators, WhileStatement
pass1 = True
#FAZER 2 PASSAGENS PELO PROGRAMA

#PRIMEIRA PASSAGEM VERIFICA VARIAVEIS GLOBAIS mas nao funcoes(?)
codigo =[]
counter = 0
def verify(node):
    global pass1
    global codigo
    global counter
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
                print(f'@{node.id} = dso_local global i32 0')
            elif node.type_specifier == "float":
                valorDoCharEmHex = float_to_hex(node.expression)
                print(f'@{node.id} = dso_local global float {valorDoCharEmHex}')
            elif node.type_specifier == "bool":
                print(f'@{node.id} = dso_local global i1 0')
            elif node.type_specifier == "string":
                #devolver o valor mesmo no node.expression
                print(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}"')
            # elif node.type_specifier == "char":
            #     valorDoCharEmHex = hex(ord(node.expression))[2:]
            #     print(f"@{node.id} = dso_local global i8 {valorDoCharEmHex}")
        else: #Local variables
            name = node.id
            #UPDATE DE VARIAVELS
            if node.declaration_type == "update":
                if isinstance(node.id, ArrayAccess): #DEPOIS
                    # if not ctx.has_var(node.id.ID):
                    #     raise TypeError(f"Array {node.id.ID} doesnt exist impossible to update")
                    
                    # if ctx.get_varOrVal(node.id.ID) == "val":
                    #     raise TypeError(f"Array {node.id.ID} is a val, impossible to update")
                    
                    # type = verify(ctx, node.id)
                    # if type != verify(ctx, node.expression):
                    #     raise TypeError(f"Array {node.id.ID} is of type {type} and not {verify(ctx, node.expression)}")
                    pass
                else:   #UPDATE DE VARIAVEL QUE NAO É ARRAY	
                    if node.type_specifier == "int":
                        print(f"store i32 {interpretor(node.expression)}, i32* %{name}")
                    elif node.type_specifier == "float":
                        print(f"store float {interpretor(node.expression)}, float* %{name}")
                    elif node.type_specifier == "bool":
                        if node.expression == "true":
                            print(f"store i1 1, i1* %{name}")
                        else:
                            print(f"store i1 0, i1* %{name}")
                    elif node.type_specifier == "string": #VER DEPOIS
                        # #devolver o valor mesmo no node.expression
                        # print(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}", align 1')
                        pass
                    elif node.type_specifier == "char":
                        print(f"store i8 {ord(node.expression)}, i8* %{name}")
            else: #DECLARACAO DE VARIAVEL
                if node.type_specifier == "int":
                    print(f"%{name} = alloca i32")
                    print(f"store i32 {interpretor(node.expression)}, i32* %{name}")
                elif node.type_specifier == "float":
                    print(f"%{name} = alloca float")
                    print(f"store float {interpretor(node.expression)}, float* %{name}")
                elif node.type_specifier == "bool":
                    print(f"%{name} = alloca i1")
                    if node.expression == "true":
                        print(f"store i1 1, i1* %{name}")
                    else:
                        print(f"store i1 0, i1* %{name}")
                elif node.type_specifier == "string":  #NOT SURE
                    print(f'@__const.{name} = private unnamed_addr constant [{len(node.expression) + 1} x i8] c"{node.expression}\\00"')
                    print(f"%{name} = alloca [{len(node.expression) + 1} x i8]")
                    print(f"%{counter} = bitcast [{len(node.expression) + 1} x i8]* %{name} to i8*")
                    print(f"call void @llvm.memcpy.p0i8.p0i8.i64(i8* %{counter}, i8* getelementptr inbounds ([{len(node.expression) + 1} x i8], [{len(node.expression) + 1} x i8]* @__const.{name}, i32 0, i32 0), i64 {len(node.expression) + 1}, i1 false)")
                    counter += 1
                elif node.type_specifier == "char": 
                    print(f"%{name} = alloca i8")
                    print(f"store i8 {ord(node.expression)}, i8* %{name}")
                pass

    elif isinstance(node, Identifier):
       print(f'%{counter} = load i32, i32* %{node.id}')
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
        vt1 = interpretor(ctx, node.left_operand)
        vt2 = interpretor(ctx, node.right_operand)
        if op == '%':
            print(f'%rem = srem nsw i32 %{counter}, {node.right_operand}')
            print(f'store i32 %rem, i32* %{node.left_operand}') #o node left_operand tem de ser nome da variavel atribuida
            return vt1%vt2
        elif op == '/':
            print(f'%div = sdiv nsw i32 %{counter}, {node.right_operand}')
            print(f'store i32 %div, i32* %{node.left_operand}') #o node left_operand tem de ser nome da variavel atribuida
            return vt1/vt2
        elif op == '*':
            print(f'%mul = mul nsw i32 %{counter}, {node.right_operand}')
            print(f'store i32 %mul, i32* %{node.left_operand}') #o node left_operand tem de ser nome da variavel atribuida
            return vt1*vt2
        elif op == '+':
            # %0 = load i32, i32* %a, align 4
            # %add = add nsw i32 %0, 2
            # store i32 %add, i32* %b, align 4
            # print(f'%{counter} = load i32, i32* %{node.left_operand}')
            print(f'%add = add nsw i32 %{counter}, {node.right_operand}') #VERIFICAR ULTIMA PARTE
            #VERIFICAR 
            print(f'store i32 %add, i32* %{node.left_operand}') #o node left_operand tem de ser nome da variavel atribuida
            return vt1+vt2
        elif op == '-':
            print(f'%sub = sub nsw i32 %{counter}, {node.right_operand}')
            print(f'store i32 %sub, i32* %{node.left_operand}') #o node left_operand tem de ser nome da variavel atribuida
            return vt1-vt2
        elif op == '^': #VER COMO FAZER ISTO
            return vt1**vt2
        elif op == '=':
            # %cmp = icmp eq i32 %0, %1
            # %conv = zext i1 %cmp to i32
            # store i32 %conv, i32* %b, align 4
            print(f'%cmp = icmp eq i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1==vt2
        elif op == '!=':
            print(f'%cmp = icmp ne i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1!=vt2
        elif op == '<=':
            print(f'%cmp = icmp sle i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1<=vt2
        elif op == '>=':
            print(f'%cmp = icmp sge i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1>=vt2
        elif op == '>':
            print(f'%cmp = icmp sgt i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1>vt2
        elif op == '<':
            print(f'%cmp = icmp slt i32 %{counter}, {node.right_operand}')
            print(f'%conv = zext i1 %cmp to i32')
            print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1<vt2
        elif op == '&&':
            return vt1 and vt2
        elif op == '||':
            return vt1 or vt2
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

print(float_to_hex(11.1))

print(f'@__const. i8] c"\\00", align 1')