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
	for i in ast.main_block_sequence:
		if isinstance(i, ImportStatement):
			input_filename = i.filepath 
			logger = yacc.NullLogger() 
			yacc.yacc(debug = logger, errorlog= logger ) 
			data = get_input(input_filename) 
			ast =  yacc.parse(data,lexer = lex.lex(nowarn=1)) 
			print(ast)
			
	# print("----------------------------------------------------------------------------------------------------")
	# verify(Context(),  ast)
	# print("OK! TYPE CHECKING PASSED!")

	# # interpretor(ContextInterpretor(),  ast)
	# # print("OK! INTERPRETATION PASSED!")
	# code_lines = codeGen.verify(ast)
	# code_string = '\n'.join(code_lines)
	# print("----------------------------------------------------------------------------------------------------")
	# print("----------------------------------------------------------------------------------------------------")
	# print(code_string)
	# with open("test.ll", "w") as file:
	# 	file.write(code_string)
if __name__ == '__main__':
	main()