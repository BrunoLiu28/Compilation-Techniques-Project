import copy
import re
from rules import ArrayAccess, BinaryOperators, Declaration, FunctionCall, FunctionDeclaration, Identifier, IfStatement, Literal, MainFunction, Parameter, Program, UnaryOperators, WhileStatement

class TypeError(Exception):
	pass

class ContextInterpretor(object):
    def __init__(self,name=None):
        self.variables = {}
        self.functions = {}


    def has_var(self,id):
        return id in self.variables
    
    def get_var(self,id):
        return self.variables[id]
    
    def add_func(self, id, returnType, params):
        self.functions[id] = (returnType, params)

    def add_var(self, id, value, varOrVal):
        self.variables[id] = (value, varOrVal)

    #RETORNAR O PRIMEIRO ENCONTRADO
    def get_varOrVal(self, name):
        return self.variables[name][1]
    
    def get_varValValue(self, name):
        return self.variables[name][0]

    #Not Used
    def get_func(self, name):
        return self.functions[name]
    
    #Not Used
    def get_funcType(self, name):
        return self.functions[name][0]
    
    #Not Used
    def get_funcParam(self, name):
        return self.functions[name][1]

    #Not Used
    def var_pop(self):
        self.variables.pop()

    #Not Used
    def has_func(self, id):
        return id in self.functions

functions = {}

functions["print_int"] = FunctionDeclaration(declaration_type="ffi", id= "print_int", param_list= [Parameter(declaration_type='var', id='any', type_specifier='int')], return_type= "void", body=None)
functions["print_int"] = FunctionDeclaration(declaration_type="ffi", id= "print_int", param_list= [Parameter(declaration_type='val', id='any', type_specifier='int')], return_type= "void", body=None)
functions["print_float"] = FunctionDeclaration(declaration_type="ffi", id= "print_float", param_list= [Parameter(declaration_type='var', id='any', type_specifier='float')], return_type= "void", body=None)
functions["print_float"] = FunctionDeclaration(declaration_type="ffi", id= "print_float", param_list= [Parameter(declaration_type='val', id='any', type_specifier='float')], return_type= "void", body=None)
functions["print_bool"] = FunctionDeclaration(declaration_type="ffi", id= "print_bool", param_list= [Parameter(declaration_type='var', id='any', type_specifier='bool')], return_type= "void", body=None)
functions["print_bool"] = FunctionDeclaration(declaration_type="ffi", id= "print_bool", param_list= [Parameter(declaration_type='val', id='any', type_specifier='bool')], return_type= "void", body=None)
functions["print_char"] = FunctionDeclaration(declaration_type="ffi", id= "print_char", param_list= [Parameter(declaration_type='var', id='any', type_specifier='char')], return_type= "void", body=None)
functions["print_char"] = FunctionDeclaration(declaration_type="ffi", id= "print_char", param_list= [Parameter(declaration_type='val', id='any', type_specifier='char')], return_type= "void", body=None)
functions["print"] = FunctionDeclaration(declaration_type="ffi", id= "print", param_list= [Parameter(declaration_type='var', id='any', type_specifier='string')], return_type= "void", body=None)
functions["print"] = FunctionDeclaration(declaration_type="ffi", id= "print", param_list= [Parameter(declaration_type='val', id='any', type_specifier='string')], return_type= "void", body=None)

onMainBlock= True
#FAZER 2 PASSAGENS PELO PROGRAMA
pass1 = True

def interpretor(ctx: ContextInterpretor, node):
    global onMainBlock
    global pass1
    global functions
    if isinstance(node, Program):
        for block in node.main_block_sequence:
            if isinstance(block, Declaration): #Ver todas as variaveis globais primeiro
                interpretor(ctx, block)
            elif isinstance(block, FunctionDeclaration) and block.declaration_type == "ffi":
                interpretor(ctx, block)
            elif isinstance(block, FunctionDeclaration) and block.declaration_type == "function":
                interpretor(ctx, block) 
            
        
        pass1 = False
        for block in node.main_block_sequence:
            if isinstance(block, MainFunction):
                interpretor(ctx, block)
                
    elif isinstance(node, MainFunction):
        name = "main"
        onMainBlock = False
        for expr in node.body:
            interpretor(ctx, expr)
            print("result", ctx.get_varValValue("result"))
    elif isinstance(node, Declaration):
            name = node.id
            ctx.add_var(name, interpretor(ctx ,node.expression), node.declaration_type)
            
    elif isinstance(node, Identifier):
        return ctx.get_varValValue(node.id)
    
    elif isinstance(node, ArrayAccess):	#FALTA FAZER ESTE
        if not ctx.has_var(node.ID):
            raise TypeError(f"Variable {node.ID} is not declared")
        if verify(ctx, node.index) != "int":
            raise TypeError(f"Array index should be an integer and not {verify(ctx, node.index)}")
        return get_type(ctx.get_varValType(node.ID))
    elif isinstance(node, FunctionDeclaration):  #FAZER SEPARACAO SE DEVOLVE ALGUMA COISA OU SE É VOID
        #Se for FFI entra aqui
        name = node.id
        type = node.return_type
        if node.declaration_type == "ffi":
            # name = node.id
            # if ctx.has_func(name):
            #     raise TypeError(f"function {name} already declared")
            #Nao faz nada?
            if pass1 == True:
                ctx.add_func(name, type, node.param_list)
        else: #funcao normal
            if pass1 == True:
                functions[node.id] = (node)
            else:
                #INTERPRETAR A FUNCAO QUANDO ELA É CHAMADA
                #Criar variavel que é utilizada para guardar o valor de retorno
                if type == "void":
                    pass
                elif type == "int":
                    ctx.add_var(name, 0, "var")
                elif type == "float":
                    ctx.add_var(name, 0.0, "var")
                elif type == "bool":
                    ctx.add_var(name, False, "var")
                elif type == "char":
                    ctx.add_var(name, "", "var")
                elif type == "string":
                    ctx.add_var(name, "", "var")

                #interpretar cada expr dentro da funcao
                for expr in node.body:
                    interpretor(ctx, expr)

                #retornar ultimo valor atribuido a variavel de retorno

                return ctx.get_varValValue(name)
        
    elif isinstance(node, FunctionCall): 
        name = node.id
        ## BUSCAR A FUNCAO E FAZER INTERPREDATOR COM ARGUMENTOS
        if functions[node.id].return_type == "void":
            return
        new_ctx = copy.deepcopy(ctx)
        function = functions[node.id]

        for i in range(len(node.param_list)):
            a = node.param_list[i]
            insideParam = function.param_list[i]
            if isinstance(a, Identifier):
                new_ctx.add_var(insideParam.id, new_ctx.get_varValValue(a.id), insideParam.declaration_type)
            elif isinstance(a, Literal):
                new_ctx.add_var(insideParam.id, a.value, insideParam.declaration_type)
            elif isinstance(a, BinaryOperators):
                new_ctx.add_var(insideParam.id, interpretor(a), insideParam.declaration_type)
            elif isinstance(a, UnaryOperators):
                new_ctx.add_var(insideParam.id, interpretor(a), insideParam.declaration_type)
            elif isinstance(a, FunctionCall):
                new_ctx.add_var(insideParam.id, interpretor(a), insideParam.declaration_type)
            elif isinstance(a, ArrayAccess):
                new_ctx.add_var(insideParam.id, interpretor(a), insideParam.declaration_type)

        interpretor(new_ctx, functions[node.id])
    
        return new_ctx.get_varValValue(name)

    elif isinstance(node, BinaryOperators):	
        op = node.operator
        vt1 = interpretor(ctx, node.left_operand)
        vt2 = interpretor(ctx, node.right_operand)
        if op == '%':
            return vt1%vt2
        elif op == '/':
            return vt1/vt2
        elif op == '*':
            return vt1*vt2
        elif op == '+':
            return vt1+vt2
        elif op == '-':
            return vt1-vt2
        elif op == '^':
            return vt1**vt2
        elif op == '=':
            return vt1==vt2
        elif op == '!=':
            return vt1!=vt2
        elif op == '<=':
            return vt1<=vt2
        elif op == '>=':
            return vt1>=vt2
        elif op == '>':
            return vt1>vt2
        elif op == '<':
            return vt1<vt2
        elif op == '&&':
            return vt1 and vt2
        elif op == '||':
            return vt1 or vt2
    elif isinstance(node, UnaryOperators):
        op = node.operator
        vt = interpretor(ctx ,node.operand)
        if op == '!':
            return not vt
        if op == '-':
            return -vt
    elif isinstance(node, IfStatement):
        condition = node.condition
        interpretor(ctx ,condition)
        if interpretor(ctx ,condition) == True:
            for a in node.thenBlock:
                interpretor(ctx ,a)
        else:
            if node.elseBlock != None:
                for a in node.elseBlock:
                    interpretor(ctx ,a)
    elif isinstance(node, WhileStatement):	
        condition = node.condition
        while interpretor(ctx ,condition) == True:
            for a in node.block_seq:
                interpretor(ctx ,a)
    elif isinstance(node, Parameter):	
        ctx.add_var(node.id, node.type_specifier, node.declaration_type)
    elif isinstance(node, Literal):
        return node.value
    else:
        print("interpretor missing:", node.__class__.__name__)


def get_type(type_string):
    match = re.search(r'\b(\w+)\b', type_string)
    if match:
        return match.group(1)
    else:
        return None


# interpretor(Context(),  ast)
# print("OK!")