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
alloc_list = []
store_param = []
variable_map_global = {}
variable_map = {}
function_map = {}
string_map = {}
register_map = {}
call_counter = 0
binary_Op_counter = 0
if_counter = 0
while_counter = 0
arrayAccess_counter = 0
prom_counter = 0
string_counter = 0

def add_to_function(name, var_type, number):
    function_map[name] = {"type": var_type, "number": number}

add_to_function("print_int", "void", -1)
add_to_function("print_float", "void", -1)
add_to_function("print_bool", "void", -1)
add_to_function("print_char", "void", -1)
add_to_function("print", "void", -1)
add_to_function("pow_int", "int", -1)
add_to_function("pow_float", "float", -1)
add_to_function("and", "int", -1)
add_to_function("or", "int", -1)

body.append("declare dso_local void @print_int(i32) ")
body.append("declare dso_local void @print_float(float)")
body.append("declare dso_local void @print_bool(i1)")
body.append("declare dso_local void @print_char(i8)")
body.append("declare dso_local void @print(i8*)")
body.append("declare dso_local i32 @pow_int(i32, i32)")
body.append("declare dso_local float @pow_float(float, i32)")
body.append("declare dso_local i1 @and(i1, i1)")
body.append("declare dso_local i1 @or(i1, i1)")

def verify(node):
    global pass1
    global codigo
    global body
    global counter
    global variable_map
    global call_counter
    global binary_Op_counter
    global if_counter
    global while_counter
    global arrayAccess_counter
    global prom_counter
    global string_counter
    global string_map
    global alloc_list
    global register_map
    global store_param
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            if isinstance(block, Declaration):
                verify(block)
            elif isinstance(block, FunctionDeclaration):
                add_to_function(block.id, block.return_type, -1)


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
                add_variable_global(name, node.type_specifier, -1)
                
                print()
                body.append(f"@{node.id} = dso_local global i8* {verify(node.expression)}")
            elif node.type_specifier == "char": 
                valorDoCharEmHex = hex(ord(node.expression))[2:]
                header.append(f"@{node.id} = dso_local global i8 {valorDoCharEmHex}")
                add_variable_global(name, "char", -1)
        else: #Local variables
            name = node.id
            #UPDATE DE VARIAVELS
            if node.declaration_type == "update":
                # is_param = ""
                # if node.id in store_param:
                #     is_param = ".addr"
                if isinstance(node.id, ArrayAccess): #DEPOIS
                    num_pairs, base_type = parse_type_specifier(variable_map[node.id.ID]["type"])
                    arrayOrNot = '*' * (num_pairs-1)
                    if base_type == "int":
                        if isinstance(node.expression, ArrayAccess):
                            aux = verify(node.expression)
                            body.append(f"%{counter} = load i32, i32* {aux}")
                            body.append(f"store i32{arrayOrNot} %{counter}, i32*{arrayOrNot} {verify(name)}")
                            add_register(counter, "i32")
                            counter += 1
                        else:
                            body.append(f"store i32{arrayOrNot} {verify(node.expression)}, i32*{arrayOrNot} {verify(name)}")
                        # body.append(f"store i32{arrayOrNot} {verify(node.id)}, i32* %arrayidx{arrayAccess_counter}")
                    elif base_type == "float":
                        if isinstance(node.expression, ArrayAccess):
                            aux = verify(node.expression)
                            body.append(f"%{counter} = load float, float* {aux}")
                            counter += 1
                            body.append(f"store float{arrayOrNot} %{counter-1}, float*{arrayOrNot} {verify(name)}")
                            add_register(counter, "float")
                            # counter += 1
                        else:
                            body.append(f"store float{arrayOrNot} {verify(node.expression)}, float*{arrayOrNot} {verify(name)}")
                        # body.append(f"store float {verify(node.expression)}, float* {verify(node.id)}")
                    # elif base_type == "bool":
                    #     if node.expression == "true":
                    #         body.append(f"store i1 1, i1* %{name}")
                    #     else:
                    #         body.append(f"store i1 0, i1* %{name}")
                    # elif base_type == "string": #VER DEPOIS
                    #     #devolver o valor mesmo no node.expression
                    #     body.append(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}", align 1')
                    # elif base_type == "char":
                    #     body.append(f"store i8 {ord(node.expression)}, i8* %{name}")
                    pass
                else:   #UPDATE DE VARIAVEL QUE NAO É ARRAY	 
                    if node.id in variable_map: #VARIAVEL LOCAL
                        type = variable_map[name]["type"]
                        is_param = ""
                        num_pairs, base_type = parse_type_specifier(type)
                        arrayOrNot = '*' * num_pairs
                        if node.id in store_param:
                            is_param = ".addr"
                        if type == "int":
                            if isinstance(node.expression, ArrayAccess):
                                aux = verify(node.expression)
                                body.append(f"%{counter} = load i32, i32* {aux}")
                                body.append(f"store i32{arrayOrNot} %{counter}, i32*{arrayOrNot} %{name+is_param}")
                                add_register(counter, "i32")
                                counter += 1
                            else:
                                body.append(f"store i32{arrayOrNot} {verify(node.expression)}, i32*{arrayOrNot} %{name+is_param}")
                        elif type == "float":
                            if isinstance(node.expression, ArrayAccess):
                                aux = verify(node.expression)
                                body.append(f"%{counter} = load float, float* {aux}")
                                body.append(f"store float{arrayOrNot} %{counter}, float*{arrayOrNot} %{name+is_param}")
                                add_register(counter, "float")
                                counter += 1
                            else:
                                body.append(f"store float{arrayOrNot} {verify(node.expression)}, float*{arrayOrNot} %{name+is_param}")
                            # body.append(f"store float {verify(node.expression)}, float* %{name+is_param}")
                        elif type == "bool":
                            body.append(f"store i1 {verify(node.expression)}, i1* %{name+is_param}")
                        elif type == "string": #VER DEPOIS
                            if name not in variable_map:
                                alloc_list.append(f"%{name} = alloca i8*")
                                add_variable(name, node.type_specifier, -1)
                            # key = verify(node.expression)
                            body.append(f"store i8* {verify(node.expression)}, i8** %{name+is_param}")
                        elif type == "char":
                            body.append(f"store i8 {ord(node.expression)}, i8* %{name+is_param}")
                    else: #VARIAVEL GLOBAL
                        type = variable_map_global[name]["type"]
                        if type == "int":
                            body.append(f"store i32 {verify(node.expression)}, i32* @{name}")
                        elif type == "float":
                            body.append(f"store float {verify(node.expression)}, float* @{name}")
                        elif type == "bool":
                            if node.expression == "true":
                                body.append(f"store i1 1, i1* @{name}")
                            else:
                                body.append(f"store i1 0, i1* @{name}")
                        elif type == "string": #VER DEPOIS
                            # key = verify(node.expression)
                            body.append(f"store i8* {verify(node.expression)}, i8** @{name}")
                            # body.append(f'@{node.id} = dso_local global [{len(node.expression)} x i8] c"{len(node.expression)}", align 1')
                        elif type == "char":
                            body.append(f"store i8 {ord(node.expression)}, i8* @{name}")
            else: #DECLARACAO DE VARIAVEL
                num_pairs, base_type = parse_type_specifier(node.type_specifier)
                arrayOrNot = '*' * num_pairs
                if base_type == "int":
                    if name not in variable_map:
                        alloc_list.append(f"%{name} = alloca i32{arrayOrNot}")
                        add_variable(name, node.type_specifier, -1)
                    if isinstance(node.expression, ArrayAccess):
                        aux = verify(node.expression)
                        body.append(f"%{counter} = load i32, i32* {aux}")
                        body.append(f"store i32{arrayOrNot} %{counter}, i32*{arrayOrNot} %{name}")
                        add_register(counter, "int")
                        counter += 1
                    else:
                        body.append(f"store i32{arrayOrNot} {verify(node.expression)}, i32*{arrayOrNot} %{name}")
                elif base_type == "float":
                    if name not in variable_map:
                        alloc_list.append(f"%{name} = alloca float{arrayOrNot}")
                        add_variable(name, node.type_specifier, -1)
                    if isinstance(node.expression, ArrayAccess):
                        aux = verify(node.expression)
                        body.append(f"%{counter} = load float, float* {aux}")
                        body.append(f"store float{arrayOrNot} %{counter}, float*{arrayOrNot} %{name}")
                        add_register(counter, "float")
                        counter += 1
                    else:
                        body.append(f"store float{arrayOrNot} {verify(node.expression)}, float*{arrayOrNot} %{name}")
                    
                elif base_type == "bool":
                    if name not in variable_map:
                        alloc_list.append(f"%{name} = alloca i1{arrayOrNot}")
                        add_variable(name, node.type_specifier, -1)

                    body.append(f"store i1{arrayOrNot} {verify(node.expression)}, i1* %{name}")
                elif base_type == "string":  #NOT SURE E AINDA VERIFICAR ARRAY DE STRING
                    if name not in variable_map:
                        alloc_list.append(f"%{name} = alloca i8*")
                        add_variable(name, node.type_specifier, -1)
                    # key = verify(node.expression)
                    body.append(f"store i8* {verify(node.expression)}, i8** %{name}")
                elif base_type == "char":    #VERIFICAR ARRAY DE CHAR
                    if name not in variable_map:
                        alloc_list.append(f"%{name} = alloca i8")
                        add_variable(name, node.type_specifier, -1)
                    body.append(f"store i8 {ord(verify(node.expression)[1])}, i8* %{name}")
                pass

    elif isinstance(node, Identifier):
        if node.id in variable_map: #VARIAVEL LOCAL
            num_pairs, type = parse_type_specifier(variable_map[node.id]["type"])
            arrayOrNot = '*' * num_pairs
            is_param = ""
            if node.id in store_param:
                is_param = ".addr"
            if type == "int":
                body.append(f'%{counter} = load i32{arrayOrNot}, i32*{arrayOrNot} %{node.id + is_param}')
                add_register(f'%{counter}', "int")
                add_variable(node.id, variable_map[node.id]["type"], counter)
            elif type == "float":
                body.append(f'%{counter} = load float{arrayOrNot}, float*{arrayOrNot} %{node.id+ is_param}')
                add_register(f'%{counter}', "float")
                add_variable(node.id, variable_map[node.id]["type"], counter)
            elif type == "bool":
                body.append(f'%{counter} = load i1{arrayOrNot}, i1*{arrayOrNot} %{node.id+ is_param}')
                add_register(f'%{counter}', "bool")
                add_variable(node.id, variable_map[node.id]["type"], counter)
            elif type == "string":
                body.append(f'%{counter} = load i8*{arrayOrNot}, i8**{arrayOrNot} %{node.id+ is_param}')
                add_register(f'%{counter}', "string")
                add_variable(node.id, variable_map[node.id]["type"], counter)
            elif type == "char":
                body.append(f'%{counter} = load i8{arrayOrNot}, i8*{arrayOrNot} %{node.id+ is_param}')
                add_register(f'%{counter}', "char")
                add_variable(node.id, variable_map[node.id]["type"], counter)
            counter += 1
            return f"%{counter-1}"
        else:   #VARIAVEL GLOBAL
            # type = variable_map_global[node.id]["type"]
            print(body)
            num_pairs, type = parse_type_specifier(variable_map_global[node.id]["type"])
            arrayOrNot = '*' * num_pairs
            
            if type == "int":
                body.append(f'%{counter} = load i32{arrayOrNot}, i32*{arrayOrNot} @{node.id}')
                add_register(counter, "int")
                add_variable_global(node.id, "int", counter)
            elif type == "float":
                body.append(f'%{counter} = load float{arrayOrNot}, float*{arrayOrNot} @{node.id}')
                add_register(counter, "float")
                add_variable_global(node.id, "float", counter)
            elif type == "bool":
                body.append(f'%{counter} = load i1{arrayOrNot}, i1*{arrayOrNot} @{node.id}')
                add_register(counter, "bool")
                add_variable_global(node.id, "bool", counter)
            elif type == "string":
                body.append(f'%{counter} = load i8*{arrayOrNot}, i8**{arrayOrNot} @{node.id}')
                add_register(counter, "string")
                add_variable_global(node.id, "string", counter)
            elif type == "char":
                body.append(f'%{counter} = load i8{arrayOrNot}, i8*{arrayOrNot} @{node.id}')
                add_register(counter, "char")
                add_variable_global(node.id, "char", counter)
            counter += 1
            return f"%{counter-1}"
        
    elif isinstance(node, ArrayAccess):	                                                                                    #FALTA FAZER ESTE
        num_pairs, type = parse_type_specifier(variable_map[node.ID]["type"])
        arrayOrNot = '*' * (num_pairs-1)
        if type == "int":
            for i in range(len(node.index)):
                if i == 0:
                    if isinstance(node.index[i], Literal):
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds i32{arrayOrNot}, i32*{arrayOrNot} {verify(Identifier(id=node.ID))}, i64 {verify(node.index[i])}")
                    else:
                        body.append(f"%idxprom{prom_counter} = sext i32 {verify(node.index[i])} to i64")
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds i32{arrayOrNot}, i32*{arrayOrNot} {verify(Identifier(id=node.ID))}, i64 %idxprom{prom_counter}")
                        prom_counter += 1
                    add_variable(f"arrayidx{arrayAccess_counter}", variable_map[node.ID]["type"][1:-1], arrayAccess_counter)
                    add_register(f"%arrayidx{arrayAccess_counter}", "float")
                else:
                    if isinstance(node.index[i], Literal):
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds i32{arrayOrNot}, i32*{arrayOrNot} {verify(Identifier(id=f"arrayidx{arrayAccess_counter-1}"))}, i64 {verify(node.index[i])}")
                    else:
                        body.append(f"%idxprom{prom_counter} = sext i32 {verify(node.index[i])} to i64")
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds i32{arrayOrNot}, i32*{arrayOrNot} {verify(Identifier(id=f"arrayidx{arrayAccess_counter-1}"))}, i64 %idxprom{prom_counter}")
                        prom_counter += 1
                    add_variable(f"arrayidx{arrayAccess_counter}", variable_map[f"arrayidx{arrayAccess_counter-1}"]["type"][1:-1], arrayAccess_counter)
                arrayAccess_counter += 1
                arrayOrNot = arrayOrNot[:-1]
            add_variable(f"arrayidx{arrayAccess_counter}", type, arrayAccess_counter)
            add_register(f"%arrayidx{arrayAccess_counter}", "float")
            return f"%arrayidx{arrayAccess_counter-1}"
        elif type == "float":
            for i in range(len(node.index)):
                if i == 0:
                    if isinstance(node.index[i], Literal):
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds float{arrayOrNot}, float*{arrayOrNot} {verify(Identifier(id=node.ID))}, i64 {verify(node.index[i])}")
                    else:
                        body.append(f"%idxprom{prom_counter} = sext i32 {verify(node.index[i])} to i64")
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds float{arrayOrNot}, float*{arrayOrNot} {verify(Identifier(id=node.ID))}, i64 %idxprom{prom_counter}")
                        prom_counter += 1
                    add_variable(f"arrayidx{arrayAccess_counter}", variable_map[node.ID]["type"][1:-1], arrayAccess_counter)
                    add_register(f"%arrayidx{arrayAccess_counter}", "float")
                else:
                    if isinstance(node.index[i], Literal):
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds float{arrayOrNot}, float*{arrayOrNot} {verify(Identifier(id=f"arrayidx{arrayAccess_counter-1}"))}, i64 {verify(node.index[i])}")
                    else:
                        body.append(f"%idxprom{prom_counter} = sext i32 {verify(node.index[i])} to i64")
                        body.append(f"%arrayidx{arrayAccess_counter} = getelementptr inbounds float{arrayOrNot}, float*{arrayOrNot} {verify(Identifier(id=f"arrayidx{arrayAccess_counter-1}"))}, i64 %idxprom{prom_counter}")
                        prom_counter += 1
                    add_variable(f"arrayidx{arrayAccess_counter}", variable_map[f"arrayidx{arrayAccess_counter-1}"]["type"][1:-1], arrayAccess_counter)
                    add_register(f"%arrayidx{arrayAccess_counter}", "float")
                arrayAccess_counter += 1
                arrayOrNot = arrayOrNot[:-1]

            add_variable(f"arrayidx{arrayAccess_counter}", type, arrayAccess_counter)
            return f"%arrayidx{arrayAccess_counter-1}"
        # elif type == "bool": #FALTA FAZER PARA OS OUTROS TIPOS
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        #Se for FFI entra aqui
        name = node.id
        type = node.return_type
        alloc_list = []
        store_param = []
        if node.declaration_type == "ffi": #FALTA FAZER VER DPS COMO SE FAZ
            add_to_function(name, type, -1)
            num_pairs, base_type = parse_type_specifier(function_map[node.id]["type"])
            arrayOrNot = '*' * num_pairs
            if base_type == "int":
                body.append(f"declare dso_local i32{arrayOrNot} @{name}(")
            elif base_type == "float":
                body.append(f"declare dso_local float{arrayOrNot} @{name}(")
            elif base_type == "bool":
                body.append(f"declare dso_local i1{arrayOrNot} @{name}(")
            elif base_type == "string":
                body.append(f"declare dso_local i8*{arrayOrNot} @{name}(")
            elif base_type == "char":
                body.append(f"declare dso_local i8{arrayOrNot} @{name}(")
            else:
                body.append(f"declare dso_local void @{name}(")
            # node.param_list = function_map[node.id]["params"]
            if node.param_list != None:
                params = []
                for x in node.param_list:
                    num_pairs, base_type = parse_type_specifier(x.type_specifier)
                    arrayOrNot = '*' * num_pairs 
                    if base_type == "int":
                        params.append(f"i32{arrayOrNot} noundef %{x.id}")
                    elif base_type == "float":
                        params.append(f"float{arrayOrNot} noundef %{x.id}")
                    elif base_type == "bool":
                        params.append(f"i1{arrayOrNot} noundef %{x.id}")
                    elif base_type == "string":
                        params.append(f"i8*{arrayOrNot} noundef %{x.id}")
                    elif base_type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext %{x.id}")
                body[-1] += ",".join(params) + f")"
            else:
                body[-1] += f")"
            
            add_to_function(name, type, -1)
            return
        else: #funcao normal
            num_pairs, base_type = parse_type_specifier(type)
            arrayOrNot = '*' * num_pairs
            if base_type == "int":
                body.append(f"define dso_local i32{arrayOrNot} @{name}(")
            elif base_type == "float":
                body.append(f"define dso_local float{arrayOrNot} @{name}(")
            elif base_type == "bool":
                body.append(f"define dso_local i1{arrayOrNot} @{name}(")
            elif base_type == "string":
                body.append(f"define dso_local i8*{arrayOrNot} @{name}(")
            elif base_type == "char":
                body.append(f"define dso_local signext i8{arrayOrNot} @{name}(")
            elif base_type == "void":
                body.append(f"define dso_local void @{name}(")
            add_to_function(name, type, -1)
            
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
            num_pairs, base_type = parse_type_specifier(type)
            arrayOrNot = '*' * num_pairs
            if base_type == "int":
                body.append(f"%{name} = alloca i32{arrayOrNot}")
                body.append(f"store i32{arrayOrNot} -1, i32*{arrayOrNot} %{name}")
                add_variable(name, "int", -1)
            elif base_type == "float":
                body.append(f"%{name} = alloca float{arrayOrNot}")
                body.append(f"store float{arrayOrNot} -1.0, float*{arrayOrNot} %{name}")
                add_variable(name, "float", -1)
            elif base_type == "bool":
                body.append(f"%{name} = alloca i1{arrayOrNot}")
                body.append(f"store i1{arrayOrNot} 0, i1*{arrayOrNot} %{name}")
                add_variable(name, "bool", -1)
            elif base_type == "string":
                body.append(f"%{name} = alloca i8*{arrayOrNot}")
                body.append(f"store i8*{arrayOrNot} "", i8**{arrayOrNot} %{name}")
                add_variable(name, "string", -1)
            elif base_type == "char":
                body.append(f"%{name} = alloca i8{arrayOrNot}")
                body.append(f"store i8{arrayOrNot} '', i8*{arrayOrNot} %{name}")
                add_variable(name, "char", -1)

            index = len(body)
            #BODY
            for expr in node.body:
                verify(expr)

            body = body[:index] + alloc_list + body[index:]

            #RETURN VALUE
            if type == "int":
                body.append(f"%{counter} = load i32, i32* %{name}")
                add_register(counter, "int")
                body.append(f"ret i32 %{counter}")
                counter+=1
            elif type == "float":
                body.append(f"%{counter} = load float, float* %{name}")
                add_register(counter, "float")
                body.append(f"ret float %{counter}")
            elif type == "bool":
                body.append(f"%{counter} = load i1, i1* %{name}")
                add_register(counter, "bool")
                body.append(f"ret i1 %{counter}")
            elif type == "string":
                body.append(f"%{counter} = load i8*, i8** %{name}")
                add_register(counter, "string")
                body.append(f"ret i8* %{counter}")
            elif type == "char":
                body.append(f"%{counter} = load i8, i8* %{name}")
                add_register(counter, "char")
                body.append(f"ret i8 %{counter}")
            elif type == "void":
                body.append(f"ret void")
            
            #REMOVER PARAMETROS
            if node.param_list != None:
                for param in node.param_list:
                    variable_map.pop(param.id)

            body.append(f"}}")
            counter = 0
    elif isinstance(node, MainFunction):
        alloc_list = []
        store_param = []
        body.append(f"define dso_local void @main(i8** noundef %argv) {{")
        body.append("entry:")
        body.append(f"%argv.addr = alloca i8**")
        body.append(f"store i8** %argv, i8*** %argv.addr")



        index = len(body)

        for expr in node.body:
            verify(expr)
        
        body = body[:index] + alloc_list + body[index:]

        body.append("ret void")
        body.append("}")
        counter = 0
        pass
    elif isinstance(node, FunctionCall): 
        name = node.id
        call = ""

        num_pairs, base_type = parse_type_specifier(function_map[node.id]["type"])
        arrayOrNot = '*' * num_pairs
        
        if base_type == "int":
            call = (f"%call{call_counter} = call i32{arrayOrNot} @{name}(")
            add_register(f"%call{call_counter}", "int")
        elif base_type == "float":
            call = (f"%call{call_counter} = call float{arrayOrNot} @{name}(")
            add_register(f"%call{call_counter}", "float")
        elif base_type == "bool":
            call = (f"%call{call_counter} = call i1{arrayOrNot} @{name}(")
            add_register(f"%call{call_counter}", "bool")
        elif base_type == "string":
            call = (f"%call{call_counter} = call i8*{arrayOrNot} @{name}(")   #VER ISTO
            add_register(f"%call{call_counter}", "string")
        elif base_type == "char":
            call = (f"%call{call_counter} = call i8{arrayOrNot} @{name}(")
            add_register(f"%call{call_counter}", "char")
        else:
            call = (f"call void @{name}(")
        
        # body.append(f"%call{call_counter} = call void @{name}(")

        add_to_function(name, function_map[node.id]["type"], call_counter)
        call_counter += 1
        params = []
        if node.param_list != None:
            for x in node.param_list:
                if isinstance(x, Literal):
                    if x.type == "int":
                        params.append(f"i32 noundef {verify(x)}")
                    elif x.type == "float":
                        params.append(f"float noundef {verify(x)}")
                    elif x.type == "bool":
                        params.append(f"i1 noundef {verify(x)}")
                    elif x.type == "string":
                        params.append(f"i8* noundef {verify(x)}")
                    elif x.type == "char":
                        params.append(f"i8 noundef signext {verify(x)}")
                elif isinstance(x, FunctionCall):
                    num_pairs, type = parse_type_specifier(function_map[x.id]["type"])
                    arrayOrNot = '*' * num_pairs
                    if type == "int":
                        params.append(f"i32{arrayOrNot} noundef {verify(x)}")
                    elif type == "float":
                        params.append(f"float{arrayOrNot} noundef {verify(x)}")
                    elif type == "bool":
                        params.append(f"i1{arrayOrNot} noundef {verify(x)}")
                    elif type == "string":
                        params.append(f"i8*{arrayOrNot} noundef {verify(x)}")
                    elif type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext {verify(x)}")
                elif isinstance(x, ArrayAccess):
                    num_pairs, type = parse_type_specifier(variable_map[x.ID]["type"])
                    arrayOrNot = '*' * (num_pairs-1)
                    value = verify(x)[1:]
                    if type == "int":
                        params.append(f"i32{arrayOrNot} noundef {verify(Identifier(id=value))}")
                    elif type == "float":
                        params.append(f"float{arrayOrNot} noundef {verify(Identifier(id=value))}")
                    elif type == "bool":
                        params.append(f"i1{arrayOrNot} noundef {verify(Identifier(id=value))}")
                    elif type == "string":
                        params.append(f"i8*{arrayOrNot} noundef {verify(Identifier(id=value))}")
                    elif type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext {verify(Identifier(id=value))}")
                elif isinstance(x, BinaryOperators):
                    register = verify(x)
                    register_type = register_map[register]["type"]  
                    print(register)
                    print(register_type)
                    num_pairs, type = parse_type_specifier(register_type)
                    arrayOrNot = '*' * (num_pairs-1)
                    if type == "int":
                        params.append(f"i32{arrayOrNot} noundef {register}")
                    elif type == "float":
                        params.append(f"float{arrayOrNot} noundef {register}")
                    elif type == "bool":
                        params.append(f"i1{arrayOrNot} noundef {register}")
                    elif type == "string":
                        params.append(f"i8*{arrayOrNot} noundef {register}")
                    elif type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext {register}")
                elif x.id in variable_map: #VARIAVEL LOCAL
                    num_pairs, type = parse_type_specifier(variable_map[x.id]["type"])
                    arrayOrNot = '*' * num_pairs
                    if type == "int":
                        params.append(f"i32{arrayOrNot} noundef {verify(x)}")
                    elif type == "float":
                        params.append(f"float{arrayOrNot} noundef {verify(x)}")
                    elif type == "bool":
                        params.append(f"i1{arrayOrNot} noundef {verify(x)}")
                    elif type == "string":
                        params.append(f"i8*{arrayOrNot} noundef {verify(x)}")
                    elif type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext {verify(x)}")
                else: #VARIAVEL GLOBAL
                    num_pairs, type = parse_type_specifier(variable_map_global[x.id]["type"])
                    arrayOrNot = '*' * num_pairs
                    if type == "int":
                        params.append(f"i32{arrayOrNot} noundef {verify(x)}")
                    elif type == "float":
                        params.append(f"float{arrayOrNot} noundef {verify(x)}")
                    elif type == "bool":
                        params.append(f"i1{arrayOrNot} noundef {verify(x)}")
                    elif type == "string":
                        params.append(f"i8*{arrayOrNot} noundef {verify(x)}")
                    elif type == "char":
                        params.append(f"i8{arrayOrNot} noundef signext {verify(x)}")
            body.append(call + (",".join(params)) + ")")
        else:
            body.append(call + ("\n".join(params)) + ")")
        return f"%call{function_map[name]["number"]}"
    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = verify(node.left_operand)
        vt2 = verify(node.right_operand)
        if isinstance(vt1, str) and "arrayidx" in vt1:
            vt1 = verify(Identifier(id=vt1[1:]))
        if isinstance(vt2, str) and "arrayidx" in vt2:
            vt2 = verify(Identifier(id=vt2[1:]))
        if op == '%':
            body.append(f'%biop{binary_Op_counter} = srem i32 {vt1}, {vt2}')
            id = f"%biop{binary_Op_counter}"
            add_register(id, "int")
            binary_Op_counter += 1
            return id
        elif op == '/':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = sdiv i32 {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "int")
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = sdiv i32 {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "int")
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fdiv float {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "float")
            else:
                body.append(f'%biop{binary_Op_counter} = fdiv float {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "float")

            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '*':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = mul nsw i32 {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "int")
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = mul nsw i32 {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "int")
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fmul float {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "float")
            else:
                body.append(f'%biop{binary_Op_counter} = fmul float {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "float")
            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '+':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = add nsw i32 {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "int")
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = add nsw i32 {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "int")
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fadd float {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "float")
            else:
                body.append(f'%biop{binary_Op_counter} = fadd float {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "float")
            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '-':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = sub nsw i32 {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "int")
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = sub nsw i32 {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "int")
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fsub float {vt1}, {vt2}')
                    add_register(f"%biop{binary_Op_counter}", "float")
            else:
                body.append(f'%biop{binary_Op_counter} = fsub float {vt1}, {vt2}')
                add_register(f"%biop{binary_Op_counter}", "float")
            id = f"%biop{binary_Op_counter}"
            add_register(id, "int")
            binary_Op_counter += 1
            return id
        elif op == '^':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = call i32 @pow_int(i32 {vt1}, i32 {vt2})')
                add_register(f"%biop{binary_Op_counter}", "int")
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = call i32 @pow_int(i32 {vt1}, i32 {vt2})')
                    add_register(f"%biop{binary_Op_counter}", "int")
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = call float @pow_float(float {vt1}, i32 {vt2})')
                    add_register(f"%biop{binary_Op_counter}", "float")
            else:
                body.append(f'%biop{binary_Op_counter} = call float @pow_float(float {vt1}, i32 {vt2})')
                add_register(f"%biop{binary_Op_counter}", "float")
            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '=':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp eq i32 {vt1}, {vt2}')
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp eq i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp oeq float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp oeq float {vt1}, {vt2}')
            
            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '!=':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp ne i32 {vt1}, {vt2}')
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp ne i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp one float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp one float {vt1}, {vt2}')

            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '<=':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp sle i32 {vt1}, {vt2}')
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp sle i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp ole float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp ole float {vt1}, {vt2}')

            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '>=':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp sge i32 {vt1}, {vt2}')
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp sge i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp oge float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp oge float {vt1}, {vt2}')
            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '>':
            print(node.left_operand)
            print(node.right_operand)
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp sgt i32 {vt1}, {vt2}')
            elif "%" in vt1:
                print(body)
                print(register_map)
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp sgt i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp ogt float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp ogt float {vt1}, {vt2}')
            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '<':
            if isinstance(vt1, int):
                body.append(f'%biop{binary_Op_counter} = icmp slt i32 {vt1}, {vt2}')
            elif "%" in vt1:
                vt1_type = register_map[vt1]["type"]
                if vt1_type == "int":
                    body.append(f'%biop{binary_Op_counter} = icmp slt i32 {vt1}, {vt2}')
                elif vt1_type == "float":
                    body.append(f'%biop{binary_Op_counter} = fcmp olt float {vt1}, {vt2}')
            else:
                body.append(f'%biop{binary_Op_counter} = fcmp olt float {vt1}, {vt2}')
            id = f"%biop{binary_Op_counter}"
            add_register(id, "bool")
            binary_Op_counter += 1
            return id
        elif op == '&&': 
            body.append(f'%biop{binary_Op_counter} = call i1 @and(i1 {vt1}, i1 {vt2})')
            add_register(f"%biop{binary_Op_counter}", "bool")
            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
        elif op == '||': 
            body.append(f'%biop{binary_Op_counter} = call i1 @or(i1 {vt1}, i1 {vt2})')
            add_register(f"%biop{binary_Op_counter}", "bool")
            id = f"%biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
    elif isinstance(node, UnaryOperators):
        op = node.operator
        vt = verify(node.operand)
        if op == '!': #FALTA FAZER ESTE
            body.append(f'%biop{binary_Op_counter} = xor i1 {vt}, true')
            id = f"biop{binary_Op_counter}"
            binary_Op_counter += 1
            return id
    elif isinstance(node, IfStatement):
        condition = node.condition

        if node.elseBlock != None:  #TEM ELSE
            id = verify(condition)
            body.append(f"br i1 {id}, label %if.then{if_counter}, label %if.else{if_counter}")

            #THEN BLOCK
            body.append(f"if.then{if_counter}:")
            for a in node.thenBlock:
                verify(a)
            body.append(f"br label %if.end{if_counter}") 

            #ELSE BLOCK
            body.append(f"if.else{if_counter}:")
            for a in node.elseBlock:
                verify(a)
            body.append(f"br label %if.end{if_counter}") 

            body.append(f"if.end{if_counter}:") 
        else:   #NAO TEM ELSE
            id = verify(condition)
            body.append(f"br i1 {id}, label %if.then{if_counter}, label %if.end{if_counter}")

            #THEN BLOCK
            body.append(f"if.then{if_counter}:")
            for a in node.thenBlock:
                verify(a)
            body.append(f"br label %if.end{if_counter}")

            body.append(f"if.end{if_counter}:")
        if_counter += 1
    elif isinstance(node, WhileStatement):	
        condition = node.condition

        body.append(f"br label %while.cond{while_counter}")
        #WHILE CONDITION
        body.append(f"while.cond{while_counter}:")
        id = verify(condition)
        body.append(f"br i1 {id}, label %while.body{while_counter}, label %while.end{while_counter}")

        #WHILE BODY
        body.append(f"while.body{while_counter}:")
        for a in node.block_seq:
            verify(a)

        body.append(f"br label %while.cond{while_counter}")

        #END WHILE
        body.append(f"while.end{while_counter}:")
        while_counter += 1
    elif isinstance(node, Parameter):
        num_pairs, base_type = parse_type_specifier(node.type_specifier)
        arrayOrNot = '*' * num_pairs
        if base_type == "int":
            body.append(f"%{node.id}.addr = alloca i32{arrayOrNot}")
            body.append(f"store i32{arrayOrNot} %{node.id}, i32*{arrayOrNot} %{node.id}.addr")
            add_variable(node.id, "int", -1)
        elif base_type == "float":
            body.append(f"%{node.id}.addr = alloca float{arrayOrNot}")
            body.append(f"store float{arrayOrNot} %{node.id}, float*{arrayOrNot} %{node.id}.addr")
            add_variable(node.id, "float", -1)
        elif base_type == "bool":
            body.append(f"%{node.id}.addr = alloca i1{arrayOrNot}")
            body.append(f"store i1{arrayOrNot} %{node.id}, i1*{arrayOrNot} %{node.id}.addr")
            add_variable(node.id, "bool", -1)
        elif base_type == "string":
            body.append(f"%{node.id}.addr = alloca i8*{arrayOrNot}")
            body.append(f"store i8*{arrayOrNot} %{node.id}, i8**{arrayOrNot} %{node.id}.addr")
            add_variable(node.id, "string", -1)
        elif base_type == "char":
            body.append(f"%{node.id}.addr = alloca i8{arrayOrNot}")
            body.append(f"store i8{arrayOrNot} %{node.id}, i8*{arrayOrNot} %{node.id}.addr")
            add_variable(node.id, "char", -1)
        store_param.append(node.id)
    elif isinstance(node, Literal):
        if node.type == "float":
            return float_to_hex(node.value)
        elif node.type == "string":
            # key = verify(node.expression)
            if node.value not in string_map:
                header.append(f'@.str.{string_counter} = private unnamed_addr constant [{len(node.value) + 1} x i8] c"{node.value}\\00"')
                add_string(node.value, f"@.str.{string_counter}", len(node.value)+1)
                string_counter += 1
            key = node.value 
            return f"getelementptr inbounds ([{string_map[key]['size']} x i8], [{string_map[key]['size']} x i8]* {string_map[key]['id']}, i64 0, i64 0)"
        elif node.type == "bool":
            if node.value == "true":
                return 1
            else:
                return 0
        return node.value
    else:
        print("semantic missing:", node.__class__.__name__)


def get_type(type_string):
    match = re.search(r'\b(\w+)\b', type_string)
    if match:
        return match.group(1)
    else:
        return None

def add_variable(name, var_type, number):
    variable_map[name] = {"type": var_type, "number": number}

def add_variable_global(name, var_type, number):
    variable_map_global[name] = {"type": var_type, "number": number}

def add_string(value, id, size):
    string_map[value] = {"id": id, "size": size}

def add_register(register, var_type):
    register_map[register] = {"type": var_type}

def parse_type_specifier(type_specifier):
    # Regular expression to match the base type and brackets
    match = re.match(r'(\[*)\s*(\w+)\s*(\]*)', type_specifier)
    
    if not match:
        raise ValueError("Invalid type specifier format")
    
    # Get the number of opening brackets
    opening_brackets = match.group(1)
    # Get the base type
    base_type = match.group(2)
    # Get the number of closing brackets
    closing_brackets = match.group(3)
    
    # Number of pairs of brackets is the length of opening brackets
    num_pairs = len(opening_brackets)# // 2
    
    return num_pairs, base_type

def float_to_hex(f):
    packed = struct.pack('>d', f)
    unpacked = struct.unpack('>Q', packed)[0] & 0xffffffffe0000000
    hex_value = f"0x{unpacked:016X}"
    hex_value = hex_value[:-7] + '0000000'
    return hex_value