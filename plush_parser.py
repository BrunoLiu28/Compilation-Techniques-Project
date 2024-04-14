import sys, os
from subprocess import Popen, PIPE

from ply import yacc,lex

from tokens import *
from rules import *

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
	print(ast)
	
if __name__ == '__main__':
	main()