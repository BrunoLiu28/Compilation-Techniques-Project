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
header = []
body = []
variable_map_global = {}
variable_map = {}
function_map = {}
call_counter = 0
binary_Op_counter = 0

def verify(node):
    global pass1
    global codigo
    global counter
    global variable_map
    global call_counter
    global binary_Op_counter
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            if isinstance(block, Declaration):
                verify(block)

        pass1 = False  #SEGUNDA PASSAGEM
        for block in node.main_block_sequence:
            if isinstance(block, Declaration): #or (isinstance(block, FunctionDeclaration) and block.declaration_type == "ffi"):
                pass
            else:
                verify(block)

        header_body = header + body
        return header_body
    elif isinstance(node, Declaration):
        if pass1: #Global variables
            name = node.id
            if node.type_specifier == "int":
                header.append(f'@{node.id} = dso_local global i32 {verify(node.expression)}')
                add_variable_global(name, "int", -1)
            elif node.type_specifier == "float":   #VERIFICAR SE ESTA CERTO
                valorDoCharEmHex = float_to_hex(node.expression)
                header.append(f'@{node.id} = dso_local global float {valorDoCharEmHex}')
                add_variable_global(name, "float", -1)
            elif node.type_specifier == "bool":
                header.append(f'@{node.id} = dso_local global i1 {verify(node.expression)}')
                add_variable_global(name, "bool", -1)
            elif node.type_specifier == "string":
                #devolver o valor mesmo no node.expression
                header.append(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}"')
                add_variable_global(name, "string", -1)
            elif node.type_specifier == "char": 
                valorDoCharEmHex = hex(ord(node.expression))[2:]
                header.append(f"@{node.id} = dso_local global i8 {valorDoCharEmHex}")
                add_variable_global(name, "char", -1)
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
                    type = variable_map[name]["type"]
                    if type == "int":
                        body.append(f"store i32 {verify(node.expression)}, i32* %{name}")
                    elif type == "float":
                        body.append(f"store float {verify(node.expression)}, float* %{name}")
                    elif type == "bool":
                        if node.expression == "true":
                            body.append(f"store i1 1, i1* %{name}")
                        else:
                            body.append(f"store i1 0, i1* %{name}")
                    elif type == "string": #VER DEPOIS
                        # #devolver o valor mesmo no node.expression
                        body.append(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}", align 1')
                    elif type == "char":
                        body.append(f"store i8 {ord(node.expression)}, i8* %{name}")
            else: #DECLARACAO DE VARIAVEL
                if node.type_specifier == "int":
                    body.append(f"%{name} = alloca i32")
                    body.append(f"store i32 {verify(node.expression)}, i32* %{name}")
                    add_variable(name, "int", -1)
                elif node.type_specifier == "float":
                    body.append(f"%{name} = alloca float")
                    body.append(f"store float {verify(node.expression)}, float* %{name}")
                    add_variable(name, "float", -1)
                elif node.type_specifier == "bool":
                    body.append(f"%{name} = alloca i1")
                    if node.expression == "true":
                        body.append(f"store i1 1, i1* %{name}")
                    else:
                        body.append(f"store i1 0, i1* %{name}")
                    add_variable(name, "bool", -1)
                elif node.type_specifier == "string":  #NOT SURE
                    body.append(f'@__const.{name} = private unnamed_addr constant [{len(node.expression) + 1} x i8] c"{node.expression}\\00"')
                    body.append(f"%{name} = alloca [{len(node.expression) + 1} x i8]")
                    body.append(f"%{counter} = bitcast [{len(node.expression) + 1} x i8]* %{name} to i8*")
                    body.append(f"call void @llvm.memcpy.p0i8.p0i8.i64(i8* %{counter}, i8* getelementptr inbounds ([{len(node.expression) + 1} x i8], [{len(node.expression) + 1} x i8]* @__const.{name}, i32 0, i32 0), i64 {len(node.expression) + 1}, i1 false)")
                    add_variable(name, "string", counter)
                    counter += 1
                elif node.type_specifier == "char": 
                    body.append(f"%{name} = alloca i8")
                    body.append(f"store i8 {ord(node.expression)}, i8* %{name}")
                    add_variable(name, "char", -1)
                pass

    elif isinstance(node, Identifier):
        if node.id in variable_map:
            type = variable_map[node.id]["type"]
            if type == "int":
                body.append(f'%{counter} = load i32, i32* %{node.id}')
                add_variable(node.id, "int", counter)
            elif type == "float":
                body.append(f'%{counter} = load float, float* %{node.id}')
                add_variable(node.id, "float", counter)
            elif type == "bool":
                body.append(f'%{counter} = load i1, i1* %{node.id}')
                add_variable(node.id, "bool", counter)
            elif type == "string":
                body.append(f'%{counter} = load i8*, i8** %{node.id}')
                add_variable(node.id, "string", counter)
            elif type == "char":
                body.append(f'%{counter} = load i8, i8* %{node.id}')
                add_variable(node.id, "char", counter)
            counter += 1
            return f"{counter-1}"
        else:
            type = variable_map_global[node.id]["type"]
            if type == "int":
                body.append(f'%{counter} = load i32, i32* @{node.id}')
                add_variable_global(node.id, "int", counter)
            elif type == "float":
                body.append(f'%{counter} = load float, float* @{node.id}')
                add_variable_global(node.id, "float", counter)
            elif type == "bool":
                body.append(f'%{counter} = load i1, i1* @{node.id}')
                add_variable_global(node.id, "bool", counter)
            elif type == "string":
                body.append(f'%{counter} = load i8*, i8** @{node.id}')
                add_variable_global(node.id, "string", counter)
            elif type == "char":
                body.append(f'%{counter} = load i8, i8* @{node.id}')
                add_variable_global(node.id, "char", counter)
            counter += 1
            return f"{counter-1}"
        
    elif isinstance(node, ArrayAccess):	#FALTA FAZER ESTE
        # if not ctx.has_var(node.ID):
        #     raise TypeError(f"Variable {node.ID} is not declared")
        # if verify(ctx, node.index) != "int":
        #     raise TypeError(f"Array index should be an integer and not {verify(ctx, node.index)}")
        # return get_type(ctx.get_varValType(node.ID))
        pass
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        #Se for FFI entra aqui
        name = node.id
        type = node.return_type
        if node.declaration_type == "ffi": #FALTA FAZER VER DPS COMO SE FAZ
            pass
        else: #funcao normal
            if type == "int":
                body.append(f"define dso_local i32 @{name}(")
            elif type == "float":
                body.append(f"define dso_local float @{name}(")
            elif type == "bool":
                body.append(f"define dso_local i1 @{name}(")
            elif type == "string":
                body.append(f"define dso_local i8* @{name}(")
            elif type == "char":
                body.append(f"define dso_local signext i8 @{name}(")
            elif type == "void":
                body.append(f"define dso_local void @{name}(")

            if node.param_list != None:
                params = []
                for x in node.param_list:
                    if x.type_specifier == "int":
                        params.append(f"i32 noundef %{x.id}")
                    elif x.type_specifier == "float":
                        params.append(f"float noundef %{x.id}")
                    elif x.type_specifier == "bool":
                        params.append(f"i1 noundef %{x.id}")
                    elif x.type_specifier == "string":
                        params.append(f"i8* noundef %{x.id}")
                    elif x.type_specifier == "char":
                        params.append(f"i8 noundef signext %{x.id}")
                body[-1] += ",".join(params) + "){"
                body.append("entry:")

                #DECLARACAO DE PARAMETROS
                for param in node.param_list:
                    verify(param)
            else:
                body[-1] += "){"
                body.append("entry:")

            #DECLARACAO DE VARIAVEL DE RETORNO
            if type == "int":
                body.append(f"%{name} = alloca i32")
                body.append(f"store i32 -1, i32* %{name}")
                add_variable(name, "int", -1)
            elif type == "float":
                body.append(f"%{name} = alloca float")
                body.append(f"store float -1.0, float* %{name}")
                add_variable(name, "float", -1)
            elif type == "bool":
                body.append(f"%{name} = alloca i1")
                body.append(f"store i1 0, i1* %{name}")
                add_variable(name, "bool", -1)
            elif type == "string":
                body.append(f"%{name} = alloca i8*")
                body.append(f"store i8* "", i8** %{name}")
                add_variable(name, "string", -1)
            elif type == "char":
                body.append(f"%{name} = alloca i8")
                body.append(f"store i8 '', i8* %{name}")
                add_variable(name, "char", -1)

            #BODY
            for expr in node.body:
                verify(expr)

            #RETURN
            if type == "int":
                body.append(f"%{counter} = load i32, i32* %{name}")
                body.append(f"ret i32 %{counter}")
                counter+=1
            elif type == "float":
                body.append(f"%{counter} = load float, float* %{name}")
                body.append(f"ret float %{counter}")
            elif type == "bool":
                body.append(f"%{counter} = load i1, i1* %{name}")
                body.append(f"ret i1 %{counter}")
            elif type == "string":
                body.append(f"%{counter} = load i8*, i8** %{name}")
                body.append(f"ret i8* %{counter}")
            elif type == "char":
                body.append(f"%{counter} = load i8, i8* %{name}")
                body.append(f"ret i8 %{counter}")
            elif type == "void":
                body.append(f"ret void")
        
            body.append(f"}}")
            counter = 0
    elif isinstance(node, MainFunction):
        body.append("define dso_local void @main() {")  #VERIFICAR SE É ISTO MAYBE VOID
        body.append("entry:")

        for expr in node.body:
            verify(expr)
        
        body.append("ret void")
        body.append("}")
        counter = 0
        pass
    elif isinstance(node, FunctionCall): 
        name = node.id
        for arg in node.param_list:
            if isinstance(arg, Literal):
                continue
            verify(arg)

        # body.append(f"call void @{name}()") #FALTA POR PARAMETROS
        print(node.param_list)
        body.append(f"%call{call_counter} =call void @{name}(")
        add_to_function(name, "void", call_counter)
        call_counter += 1
        params = []
        for x in node.param_list:
            if isinstance(x, Literal):
                if x.type == "int":
                    params.append(f"i32 noundef {x.value}")
                elif x.type == "float":
                    params.append(f"float noundef {x.value}")
                elif x.type == "bool":
                    params.append(f"i1 noundef {x.value}")
                elif x.type == "string":
                    params.append(f"i8* noundef {x.value}")
                elif x.type == "char":
                    params.append(f"i8 noundef signext {x.value}")
            else:
                if x.id in variable_map:
                    type = variable_map[x.id]["type"]
                    if type == "int":
                        params.append(f"i32 noundef %{variable_map[x.id]["number"]}")
                    elif type == "float":
                        params.append(f"float noundef %{variable_map[x.id]["number"]}")
                    elif type == "bool":
                        params.append(f"i1 noundef %{variable_map[x.id]["number"]}")
                    elif type == "string":
                        params.append(f"i8* noundef %{variable_map[x.id]["number"]}")
                    elif type == "char":
                        params.append(f"i8 noundef signext %{variable_map[x.id]["number"]}")
                else:
                    type = variable_map_global[x.id]["type"]
                    if type == "int":
                        params.append(f"i32 noundef %{variable_map_global[x.id]["number"]}")
                    elif type == "float":
                        params.append(f"float noundef %{variable_map_global[x.id]["number"]}")
                    elif type == "bool":
                        params.append(f"i1 noundef %{variable_map_global[x.id]["number"]}")
                    elif type == "string":
                        params.append(f"i8* noundef %{variable_map_global[x.id]["number"]}")
                    elif type == "char":
                        params.append(f"i8 noundef signext %{variable_map_global[x.id]["number"]}")
        body[-1] += ",".join(params) + ")"

        return f"call{function_map[name]["number"]}"
    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(node.left_operand)
        vt2 = verify(node.right_operand)
        if op == '%':
            body.append(f'%biop{binary_Op_counter} = srem nsw i32 %{vt1}, {vt2}')
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '/':
            body.append(f'%biop{binary_Op_counter} = sdiv nsw i32 %{vt1}, {vt2}')
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '*':
            body.append(f'%biop{binary_Op_counter} = mul nsw i32 %{vt1}, {vt2}')
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '+':
            body.append(f'%biop{binary_Op_counter} = add nsw i32 %{vt1}, {vt2}') #VERIFICAR ULTIMA PARTE
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '-':
            body.append(f'%biop{binary_Op_counter} = sub nsw i32 %{vt1}, {vt2}')
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '^': #VER COMO FAZER ISTO
            return vt1**vt2
        elif op == '=':
            # %cmp = icmp eq i32 %0, %1
            # %conv = zext i1 %cmp to i32
            # store i32 %conv, i32* %b, align 4
            body.append(f'%cmp = icmp eq i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1==vt2
        elif op == '!=':
            body.append(f'%cmp = icmp ne i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1!=vt2
        elif op == '<=':
            body.append(f'%cmp = icmp sle i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1<=vt2
        elif op == '>=':
            body.append(f'%cmp = icmp sge i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1>=vt2
        elif op == '>':
            body.append(f'%cmp = icmp sgt i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
            return vt1>vt2
        elif op == '<':
            body.append(f'%cmp = icmp slt i32 %{vt1}, {vt2}')
            body.append(f'%conv = zext i1 %cmp to i32')
            # print(f'store i32 %conv, i32* %{node.left_operand}')
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
        verify(condition)
        # if verify(ctx ,condition) != 'bool':
        #     raise TypeError(f"If condition requires a boolean. Got {verify(ctx, condition)} instead.")
        # for a in node.thenBlock:
        #     verify(ctx ,a)
        # if node.elseBlock != None:
        #     for a in node.elseBlock:
        #         verify(ctx ,a)
    
    elif isinstance(node, WhileStatement):	
        condition = node.condition
        if verify(ctx ,condition) != 'bool':
            raise TypeError(f"WHILE condition requires a boolean. Got {verify(ctx, condition)} instead.")
        for a in node.block_seq:
            verify(ctx ,a)
    elif isinstance(node, Parameter):
        if node.type_specifier == "int":
            body.append(f"%{node.id}.addr = alloca i32")
            body.append(f"store i32 %{node.id}, i32* %{node.id}.addr")
            add_variable(node.id, "int", -1)
        elif node.type_specifier == "float":
            body.append(f"%{node.id}.addr = alloca float")
            body.append(f"store float %{node.id}, float* %{node.id}.addr")
            add_variable(node.id, "float", -1)
        elif node.type_specifier == "bool":
            body.append(f"%{node.id}.addr = alloca i1")
            body.append(f"store i1 %{node.id}, i1* %{node.id}.addr")
            add_variable(node.id, "bool", -1)
        elif node.type_specifier == "string":
            body.append(f"%{node.id}.addr = alloca i8*")
            body.append(f"store i8* %{node.id}, i8** %{node.id}.addr")
            add_variable(node.id, "string", -1)
        elif node.type_specifier == "char":
            body.append(f"%{node.id}.addr = alloca i8")
            body.append(f"store i8 %{node.id}, i8* %{node.id}.addr")
            add_variable(node.id, "char", -1)

    elif isinstance(node, Literal):
        return node.value
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

def add_variable(name, var_type, number):
    variable_map[name] = {"type": var_type, "number": number}

def add_variable_global(name, var_type, number):
    variable_map_global[name] = {"type": var_type, "number": number}

def add_to_function(name, var_type, number):
    function_map[name] = {"type": var_type, "number": number}