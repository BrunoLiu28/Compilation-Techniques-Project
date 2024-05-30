import sys, os
from subprocess import Popen, PIPE

from interpretor import ContextInterpretor, interpretor
from ply import yacc,lex

from semantic import Context, verify
from tokens import *
from rules import *
import codeGen

parser = yacc.yacc()


def get_input(file=False):
	if file:
		f = open(file,"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break
	return data


def main(options={},filename=False): 
	if len(sys.argv) != 2: 
		print("Usage: python script.py <input_file>") 
		sys.exit(1) 
	input_filename = sys.argv[1] 
	logger = yacc.NullLogger() 
	yacc.yacc(debug = logger, errorlog= logger ) 
	data = get_input(input_filename) 
	ast =  yacc.parse(data,lexer = lex.lex(nowarn=1)) 
	print("----------------------------------------------------------------------------------------------------")
	print(ast)
	
	continuar = True
	while continuar:
		continuar = False
		new_main_block_sequence = []
		for i in ast.main_block_sequence:
			if isinstance(i, ImportStatement):
				continuar = True
				input_filename = i.filepath 
				logger = yacc.NullLogger() 
				yacc.yacc(debug = logger, errorlog= logger ) 
				data = get_input(input_filename) 
				importedAst =  yacc.parse(data,lexer = lex.lex(nowarn=1)) 
				if i.functions[0] == "*":
					importedAst.main_block_sequence = [block for block in importedAst.main_block_sequence if not isinstance(block, MainFunction)]
					new_main_block_sequence.extend(importedAst.main_block_sequence)
				else:
					for function in i.functions:
						for block in importedAst.main_block_sequence:
							if isinstance(block, FunctionDeclaration) and block.id == function:
								new_main_block_sequence.append(block)
								i.functions.remove(function)
					if len(i.functions) > 0:
						print("ERROR: Function(s) not found: " + str(i.functions) + " in file " + i.filepath)
						sys.exit(1)
			else:
				new_main_block_sequence.append(i)
		ast.main_block_sequence = new_main_block_sequence
	
	print("----------------------------------------------------------------------------------------------------")
	verify(Context(),  ast)
	print("OK! TYPE CHECKING PASSED!")

	# # interpretor(ContextInterpretor(),  ast)
	# # print("OK! INTERPRETATION PASSED!")
	code_lines = codeGen.verify(ast)
	code_string = '\n'.join(code_lines)
	print("----------------------------------------------------------------------------------------------------")
	print("----------------------------------------------------------------------------------------------------")
	print(code_string)
	with open("test.ll", "w") as file:
		file.write(code_string)
if __name__ == '__main__':
	main()