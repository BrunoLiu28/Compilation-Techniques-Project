
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programleftCOMMArightASSIGNleftORleftANDnonassocEQUALNOT_EQUALnonassocGREATER_THANGREATER_THAN_EQUALLESS_THANLESS_THAN_EQUALleftPLUSMINUSleftTIMESDIVIDEMODrightUMINUSrightPOWERrightNOTleftLPARENRPARENAND ASSIGN BOOL_LITERAL BOOL_TYPE CHAR_LITERAL CHAR_TYPE COLON COMMA COMMENT DIVIDE ELSE EQUAL FLOAT_LITERAL FLOAT_TYPE FUNCTION GREATER_THAN GREATER_THAN_EQUAL ID IF INTEGER_LITERAL INT_TYPE LBRACE LESS_THAN LESS_THAN_EQUAL LPAREN LSQUARE MAIN MINUS MOD NOT NOT_EQUAL OR PLUS POWER RBRACE RPAREN RSQUARE SEMICOLON STRING_LITERAL STRING_TYPE TIMES VAL VAR VOID_TYPE WHILEprogram : main_block_sequence main_block_sequence : main_block main_block_sequence\n\t                        | main_blockcomment : COMMENT STRING_LITERALmain_block : constant_declaration\n     | variable_declaration \n     | var_const_update\n\t | function_declaration \n     | main_function\n     | comment\n\tconstant_declaration : VAL ID COLON types ASSIGN expression SEMICOLONvariable_declaration : VAR ID COLON types ASSIGN expression SEMICOLONvar_const_update :  ID ASSIGN expression SEMICOLON\n                        | arrayaccess ASSIGN expression SEMICOLONfunction_declaration : FUNCTION ID LPAREN function_param_list RPAREN COLON types SEMICOLON\n    |  FUNCTION ID LPAREN function_param_list RPAREN COLON types LBRACE function_body RBRACEmain_function : FUNCTION MAIN LPAREN function_param_list RPAREN LBRACE function_body RBRACEfunction_param_list : parameter COMMA function_param_list\n    | parameter parameter : VAL ID COLON types\n                    | VAR ID COLON typesfunction_call : ID LPAREN function_param_list_call RPAREN \n                     | ID LPAREN RPAREN \n    function_param_list_call : expression COMMA function_param_list_call\n    | expressionfunction_body : block_sequenceblock_sequence : block block_sequence\n\t | blockblock : constant_declaration\n     | variable_declaration \n     | var_const_update\n\t | if_block\n\t | while_block\n\t | function_call SEMICOLON\n     | comment\n\tif_block : IF expression LBRACE block_sequence RBRACE ELSE LBRACE block_sequence RBRACE\n\t| IF expression LBRACE block_sequence RBRACE \n\twhile_block : WHILE expression LBRACE block_sequence RBRACEtypes : defaulttype\n            | LSQUARE arraytype RSQUAREdefaulttype : INT_TYPE\n            | FLOAT_TYPE\n            | STRING_TYPE\n            | BOOL_TYPE\n            | VOID_TYPE\n            | CHAR_TYPEarraytype : LSQUARE arraytype RSQUARE\n            | INT_TYPE\n            | FLOAT_TYPE\n            | STRING_TYPE\n            | BOOL_TYPE\n            | VOID_TYPE\n            arrayaccess : ID LSQUARE expression RSQUARE\n                    | function_call LSQUARE expression RSQUAREexpression : ID expression : INTEGER_LITERAL\n                  | MINUS INTEGER_LITERAL %prec UMINUSexpression : FLOAT_LITERAL\n                  | MINUS FLOAT_LITERAL %prec UMINUSexpression : STRING_LITERALexpression : BOOL_LITERALexpression : CHAR_LITERALexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expression\n                  | expression MOD expression\n                  | expression POWER expression\n                  | expression EQUAL expression\n                  | expression NOT_EQUAL expression\n                  | expression GREATER_THAN expression\n                  | expression GREATER_THAN_EQUAL expression\n                  | expression LESS_THAN expression\n                  | expression LESS_THAN_EQUAL expression\n                  | expression AND expression\n                  | expression OR expression\n                  | NOT expression\n                  \n                  | arrayaccess\n                  | function_call\n                  | LPAREN expression RPAREN'
    
_lr_action_items = {'VAL':([0,3,4,5,6,7,8,9,26,47,48,59,82,115,127,128,130,136,137,138,139,140,141,143,147,148,149,151,155,156,157,160,161,163,165,],[10,10,-5,-6,-7,-8,-9,-10,-4,85,85,-13,-14,85,10,-11,-12,10,-29,-30,-31,-32,-33,-35,-15,10,-17,-34,10,10,-16,-37,-38,10,-36,]),'VAR':([0,3,4,5,6,7,8,9,26,47,48,59,82,115,127,128,130,136,137,138,139,140,141,143,147,148,149,151,155,156,157,160,161,163,165,],[12,12,-5,-6,-7,-8,-9,-10,-4,86,86,-13,-14,86,12,-11,-12,12,-29,-30,-31,-32,-33,-35,-15,12,-17,-34,12,12,-16,-37,-38,12,-36,]),'ID':([0,3,4,5,6,7,8,9,10,12,14,19,20,21,23,26,27,37,40,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,82,85,86,89,113,127,128,130,136,137,138,139,140,141,143,145,146,147,148,149,151,155,156,157,160,161,163,165,],[11,11,-5,-6,-7,-8,-9,-10,18,22,24,29,29,29,29,-4,29,29,29,-13,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,-14,116,117,29,29,144,-11,-12,144,-29,-30,-31,-32,-33,-35,29,29,-15,144,-17,-34,144,144,-16,-37,-38,144,-36,]),'FUNCTION':([0,3,4,5,6,7,8,9,26,59,82,128,130,147,149,157,],[14,14,-5,-6,-7,-8,-9,-10,-4,-13,-14,-11,-12,-15,-17,-16,]),'COMMENT':([0,3,4,5,6,7,8,9,26,59,82,127,128,130,136,137,138,139,140,141,143,147,148,149,151,155,156,157,160,161,163,165,],[15,15,-5,-6,-7,-8,-9,-10,-4,-13,-14,15,-11,-12,15,-29,-30,-31,-32,-33,-35,-15,15,-17,-34,15,15,-16,-37,-38,15,-36,]),'$end':([1,2,3,4,5,6,7,8,9,17,26,59,82,128,130,147,149,157,],[0,-1,-3,-5,-6,-7,-8,-9,-10,-2,-4,-13,-14,-11,-12,-15,-17,-16,]),'ASSIGN':([11,13,50,51,53,54,55,56,57,58,78,81,88,121,144,],[19,23,89,-39,-41,-42,-43,-44,-45,-46,-53,113,-54,-40,19,]),'LSQUARE':([11,16,28,29,39,43,45,52,79,90,123,125,126,142,144,],[20,27,52,20,27,-23,52,90,-22,90,52,52,52,27,20,]),'LPAREN':([11,19,20,21,23,24,25,27,29,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,144,145,146,],[21,40,40,40,40,47,48,40,21,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,21,40,40,]),'MAIN':([14,],[25,]),'STRING_LITERAL':([15,19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[26,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'COLON':([18,22,114,116,117,],[28,45,123,125,126,]),'INTEGER_LITERAL':([19,20,21,23,27,32,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[31,31,31,31,31,74,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,]),'MINUS':([19,20,21,23,27,29,30,31,33,34,35,36,37,38,39,40,41,43,44,46,49,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,88,89,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,113,119,122,145,146,152,153,],[32,32,32,32,32,-55,61,-56,-58,-60,-61,-62,32,-78,-79,32,61,-23,61,61,61,32,32,32,32,32,32,32,32,32,32,32,32,32,32,-57,-59,-77,61,-53,-22,32,-54,32,-63,-64,-65,-66,-67,-68,61,61,61,61,61,61,61,61,-80,32,61,61,32,32,61,61,]),'FLOAT_LITERAL':([19,20,21,23,27,32,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[33,33,33,33,33,75,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'BOOL_LITERAL':([19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'CHAR_LITERAL':([19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'NOT':([19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,]),'RPAREN':([21,29,31,33,34,35,36,38,39,42,43,44,51,53,54,55,56,57,58,74,75,76,77,78,79,83,84,87,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,121,124,132,133,],[43,-55,-56,-58,-60,-61,-62,-78,-79,79,-23,-25,-39,-41,-42,-43,-44,-45,-46,-57,-59,-77,111,-53,-22,114,-19,118,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,-24,-40,-18,-20,-21,]),'IF':([26,59,82,127,128,130,136,137,138,139,140,141,143,148,151,155,156,160,161,163,165,],[-4,-13,-14,145,-11,-12,145,-29,-30,-31,-32,-33,-35,145,-34,145,145,-37,-38,145,-36,]),'WHILE':([26,59,82,127,128,130,136,137,138,139,140,141,143,148,151,155,156,160,161,163,165,],[-4,-13,-14,146,-11,-12,146,-29,-30,-31,-32,-33,-35,146,-34,146,146,-37,-38,146,-36,]),'RBRACE':([26,59,82,128,130,134,135,136,137,138,139,140,141,143,150,151,154,158,159,160,161,164,165,],[-4,-13,-14,-11,-12,149,-26,-28,-29,-30,-31,-32,-33,-35,-27,-34,157,160,161,-37,-38,165,-36,]),'INT_TYPE':([28,45,52,90,123,125,126,],[53,53,92,92,53,53,53,]),'FLOAT_TYPE':([28,45,52,90,123,125,126,],[54,54,93,93,54,54,54,]),'STRING_TYPE':([28,45,52,90,123,125,126,],[55,55,94,94,55,55,55,]),'BOOL_TYPE':([28,45,52,90,123,125,126,],[56,56,95,95,56,56,56,]),'VOID_TYPE':([28,45,52,90,123,125,126,],[57,57,96,96,57,57,57,]),'CHAR_TYPE':([28,45,123,125,126,],[58,58,58,58,58,]),'SEMICOLON':([29,30,31,33,34,35,36,38,39,43,46,51,53,54,55,56,57,58,74,75,76,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,121,122,131,142,],[-55,59,-56,-58,-60,-61,-62,-78,-79,-23,82,-39,-41,-42,-43,-44,-45,-46,-57,-59,-77,-53,-22,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,128,-40,130,147,151,]),'PLUS':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,60,-56,-58,-60,-61,-62,-78,-79,60,-23,60,60,60,-57,-59,-77,60,-53,-22,-54,-63,-64,-65,-66,-67,-68,60,60,60,60,60,60,60,60,-80,60,60,60,60,]),'TIMES':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,62,-56,-58,-60,-61,-62,-78,-79,62,-23,62,62,62,-57,-59,-77,62,-53,-22,-54,62,62,-65,-66,-67,-68,62,62,62,62,62,62,62,62,-80,62,62,62,62,]),'DIVIDE':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,63,-56,-58,-60,-61,-62,-78,-79,63,-23,63,63,63,-57,-59,-77,63,-53,-22,-54,63,63,-65,-66,-67,-68,63,63,63,63,63,63,63,63,-80,63,63,63,63,]),'MOD':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,64,-56,-58,-60,-61,-62,-78,-79,64,-23,64,64,64,-57,-59,-77,64,-53,-22,-54,64,64,-65,-66,-67,-68,64,64,64,64,64,64,64,64,-80,64,64,64,64,]),'POWER':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,65,-56,-58,-60,-61,-62,-78,-79,65,-23,65,65,65,-57,-59,-77,65,-53,-22,-54,65,65,65,65,65,65,65,65,65,65,65,65,65,65,-80,65,65,65,65,]),'EQUAL':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,66,-56,-58,-60,-61,-62,-78,-79,66,-23,66,66,66,-57,-59,-77,66,-53,-22,-54,-63,-64,-65,-66,-67,-68,None,None,-71,-72,-73,-74,66,66,-80,66,66,66,66,]),'NOT_EQUAL':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,67,-56,-58,-60,-61,-62,-78,-79,67,-23,67,67,67,-57,-59,-77,67,-53,-22,-54,-63,-64,-65,-66,-67,-68,None,None,-71,-72,-73,-74,67,67,-80,67,67,67,67,]),'GREATER_THAN':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,68,-56,-58,-60,-61,-62,-78,-79,68,-23,68,68,68,-57,-59,-77,68,-53,-22,-54,-63,-64,-65,-66,-67,-68,68,68,None,None,None,None,68,68,-80,68,68,68,68,]),'GREATER_THAN_EQUAL':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,69,-56,-58,-60,-61,-62,-78,-79,69,-23,69,69,69,-57,-59,-77,69,-53,-22,-54,-63,-64,-65,-66,-67,-68,69,69,None,None,None,None,69,69,-80,69,69,69,69,]),'LESS_THAN':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,70,-56,-58,-60,-61,-62,-78,-79,70,-23,70,70,70,-57,-59,-77,70,-53,-22,-54,-63,-64,-65,-66,-67,-68,70,70,None,None,None,None,70,70,-80,70,70,70,70,]),'LESS_THAN_EQUAL':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,71,-56,-58,-60,-61,-62,-78,-79,71,-23,71,71,71,-57,-59,-77,71,-53,-22,-54,-63,-64,-65,-66,-67,-68,71,71,None,None,None,None,71,71,-80,71,71,71,71,]),'AND':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,72,-56,-58,-60,-61,-62,-78,-79,72,-23,72,72,72,-57,-59,-77,72,-53,-22,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,72,-80,72,72,72,72,]),'OR':([29,30,31,33,34,35,36,38,39,41,43,44,46,49,74,75,76,77,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,119,122,152,153,],[-55,73,-56,-58,-60,-61,-62,-78,-79,73,-23,73,73,73,-57,-59,-77,73,-53,-22,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,73,73,73,73,]),'RSQUARE':([29,31,33,34,35,36,38,39,41,43,49,74,75,76,78,79,88,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,120,129,],[-55,-56,-58,-60,-61,-62,-78,-79,78,-23,88,-57,-59,-77,-53,-22,-54,121,-48,-49,-50,-51,-52,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,129,-47,]),'COMMA':([29,31,33,34,35,36,38,39,43,44,51,53,54,55,56,57,58,74,75,76,78,79,84,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,121,132,133,],[-55,-56,-58,-60,-61,-62,-78,-79,-23,80,-39,-41,-42,-43,-44,-45,-46,-57,-59,-77,-53,-22,115,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,-40,-20,-21,]),'LBRACE':([29,31,33,34,35,36,38,39,43,51,53,54,55,56,57,58,74,75,76,78,79,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,118,121,131,152,153,162,],[-55,-56,-58,-60,-61,-62,-78,-79,-23,-39,-41,-42,-43,-44,-45,-46,-57,-59,-77,-53,-22,-54,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-80,127,-40,148,155,156,163,]),'ELSE':([160,],[162,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'main_block_sequence':([0,3,],[2,17,]),'main_block':([0,3,],[3,3,]),'constant_declaration':([0,3,127,136,148,155,156,163,],[4,4,137,137,137,137,137,137,]),'variable_declaration':([0,3,127,136,148,155,156,163,],[5,5,138,138,138,138,138,138,]),'var_const_update':([0,3,127,136,148,155,156,163,],[6,6,139,139,139,139,139,139,]),'function_declaration':([0,3,],[7,7,]),'main_function':([0,3,],[8,8,]),'comment':([0,3,127,136,148,155,156,163,],[9,9,143,143,143,143,143,143,]),'arrayaccess':([0,3,19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,127,136,145,146,148,155,156,163,],[13,13,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,13,13,38,38,13,13,13,13,]),'function_call':([0,3,19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,127,136,145,146,148,155,156,163,],[16,16,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,142,142,39,39,142,142,142,142,]),'expression':([19,20,21,23,27,37,40,60,61,62,63,64,65,66,67,68,69,70,71,72,73,80,89,113,145,146,],[30,41,44,46,49,76,77,97,98,99,100,101,102,103,104,105,106,107,108,109,110,44,119,122,152,153,]),'function_param_list_call':([21,80,],[42,112,]),'types':([28,45,123,125,126,],[50,81,131,132,133,]),'defaulttype':([28,45,123,125,126,],[51,51,51,51,51,]),'function_param_list':([47,48,115,],[83,87,124,]),'parameter':([47,48,115,],[84,84,84,]),'arraytype':([52,90,],[91,120,]),'function_body':([127,148,],[134,154,]),'block_sequence':([127,136,148,155,156,163,],[135,150,135,158,159,164,]),'block':([127,136,148,155,156,163,],[136,136,136,136,136,136,]),'if_block':([127,136,148,155,156,163,],[140,140,140,140,140,140,]),'while_block':([127,136,148,155,156,163,],[141,141,141,141,141,141,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> main_block_sequence','program',1,'p_program','rules.py',119),
  ('main_block_sequence -> main_block main_block_sequence','main_block_sequence',2,'p_main_block_sequence','rules.py',124),
  ('main_block_sequence -> main_block','main_block_sequence',1,'p_main_block_sequence','rules.py',125),
  ('comment -> COMMENT STRING_LITERAL','comment',2,'p_comment','rules.py',132),
  ('main_block -> constant_declaration','main_block',1,'p_main_block','rules.py',137),
  ('main_block -> variable_declaration','main_block',1,'p_main_block','rules.py',138),
  ('main_block -> var_const_update','main_block',1,'p_main_block','rules.py',139),
  ('main_block -> function_declaration','main_block',1,'p_main_block','rules.py',140),
  ('main_block -> main_function','main_block',1,'p_main_block','rules.py',141),
  ('main_block -> comment','main_block',1,'p_main_block','rules.py',142),
  ('constant_declaration -> VAL ID COLON types ASSIGN expression SEMICOLON','constant_declaration',7,'p_constant_declaration','rules.py',149),
  ('variable_declaration -> VAR ID COLON types ASSIGN expression SEMICOLON','variable_declaration',7,'p_variable_declaration','rules.py',154),
  ('var_const_update -> ID ASSIGN expression SEMICOLON','var_const_update',4,'p_var_const_update','rules.py',159),
  ('var_const_update -> arrayaccess ASSIGN expression SEMICOLON','var_const_update',4,'p_var_const_update','rules.py',160),
  ('function_declaration -> FUNCTION ID LPAREN function_param_list RPAREN COLON types SEMICOLON','function_declaration',8,'p_function_declaration','rules.py',165),
  ('function_declaration -> FUNCTION ID LPAREN function_param_list RPAREN COLON types LBRACE function_body RBRACE','function_declaration',10,'p_function_declaration','rules.py',166),
  ('main_function -> FUNCTION MAIN LPAREN function_param_list RPAREN LBRACE function_body RBRACE','main_function',8,'p_main_function','rules.py',173),
  ('function_param_list -> parameter COMMA function_param_list','function_param_list',3,'p_function_param_list','rules.py',177),
  ('function_param_list -> parameter','function_param_list',1,'p_function_param_list','rules.py',178),
  ('parameter -> VAL ID COLON types','parameter',4,'p_parameter','rules.py',188),
  ('parameter -> VAR ID COLON types','parameter',4,'p_parameter','rules.py',189),
  ('function_call -> ID LPAREN function_param_list_call RPAREN','function_call',4,'p_function_call','rules.py',198),
  ('function_call -> ID LPAREN RPAREN','function_call',3,'p_function_call','rules.py',199),
  ('function_param_list_call -> expression COMMA function_param_list_call','function_param_list_call',3,'p_function_param_list_call','rules.py',208),
  ('function_param_list_call -> expression','function_param_list_call',1,'p_function_param_list_call','rules.py',209),
  ('function_body -> block_sequence','function_body',1,'p_function_body','rules.py',220),
  ('block_sequence -> block block_sequence','block_sequence',2,'p_block_sequence','rules.py',225),
  ('block_sequence -> block','block_sequence',1,'p_block_sequence','rules.py',226),
  ('block -> constant_declaration','block',1,'p_block','rules.py',233),
  ('block -> variable_declaration','block',1,'p_block','rules.py',234),
  ('block -> var_const_update','block',1,'p_block','rules.py',235),
  ('block -> if_block','block',1,'p_block','rules.py',236),
  ('block -> while_block','block',1,'p_block','rules.py',237),
  ('block -> function_call SEMICOLON','block',2,'p_block','rules.py',238),
  ('block -> comment','block',1,'p_block','rules.py',239),
  ('if_block -> IF expression LBRACE block_sequence RBRACE ELSE LBRACE block_sequence RBRACE','if_block',9,'p_if_block','rules.py',245),
  ('if_block -> IF expression LBRACE block_sequence RBRACE','if_block',5,'p_if_block','rules.py',246),
  ('while_block -> WHILE expression LBRACE block_sequence RBRACE','while_block',5,'p_while_block','rules.py',254),
  ('types -> defaulttype','types',1,'p_types','rules.py',260),
  ('types -> LSQUARE arraytype RSQUARE','types',3,'p_types','rules.py',261),
  ('defaulttype -> INT_TYPE','defaulttype',1,'p_defaultype','rules.py',268),
  ('defaulttype -> FLOAT_TYPE','defaulttype',1,'p_defaultype','rules.py',269),
  ('defaulttype -> STRING_TYPE','defaulttype',1,'p_defaultype','rules.py',270),
  ('defaulttype -> BOOL_TYPE','defaulttype',1,'p_defaultype','rules.py',271),
  ('defaulttype -> VOID_TYPE','defaulttype',1,'p_defaultype','rules.py',272),
  ('defaulttype -> CHAR_TYPE','defaulttype',1,'p_defaultype','rules.py',273),
  ('arraytype -> LSQUARE arraytype RSQUARE','arraytype',3,'p_arraytype','rules.py',277),
  ('arraytype -> INT_TYPE','arraytype',1,'p_arraytype','rules.py',278),
  ('arraytype -> FLOAT_TYPE','arraytype',1,'p_arraytype','rules.py',279),
  ('arraytype -> STRING_TYPE','arraytype',1,'p_arraytype','rules.py',280),
  ('arraytype -> BOOL_TYPE','arraytype',1,'p_arraytype','rules.py',281),
  ('arraytype -> VOID_TYPE','arraytype',1,'p_arraytype','rules.py',282),
  ('arrayaccess -> ID LSQUARE expression RSQUARE','arrayaccess',4,'p_arrayaccess','rules.py',292),
  ('arrayaccess -> function_call LSQUARE expression RSQUARE','arrayaccess',4,'p_arrayaccess','rules.py',293),
  ('expression -> ID','expression',1,'p_identifier','rules.py',297),
  ('expression -> INTEGER_LITERAL','expression',1,'p_integer_literal','rules.py',308),
  ('expression -> MINUS INTEGER_LITERAL','expression',2,'p_integer_literal','rules.py',309),
  ('expression -> FLOAT_LITERAL','expression',1,'p_float_literal','rules.py',316),
  ('expression -> MINUS FLOAT_LITERAL','expression',2,'p_float_literal','rules.py',317),
  ('expression -> STRING_LITERAL','expression',1,'p_string_literal','rules.py',324),
  ('expression -> BOOL_LITERAL','expression',1,'p_bool_literal','rules.py',328),
  ('expression -> CHAR_LITERAL','expression',1,'p_char_literal','rules.py',332),
  ('expression -> expression PLUS expression','expression',3,'p_expression','rules.py',336),
  ('expression -> expression MINUS expression','expression',3,'p_expression','rules.py',337),
  ('expression -> expression TIMES expression','expression',3,'p_expression','rules.py',338),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','rules.py',339),
  ('expression -> expression MOD expression','expression',3,'p_expression','rules.py',340),
  ('expression -> expression POWER expression','expression',3,'p_expression','rules.py',341),
  ('expression -> expression EQUAL expression','expression',3,'p_expression','rules.py',342),
  ('expression -> expression NOT_EQUAL expression','expression',3,'p_expression','rules.py',343),
  ('expression -> expression GREATER_THAN expression','expression',3,'p_expression','rules.py',344),
  ('expression -> expression GREATER_THAN_EQUAL expression','expression',3,'p_expression','rules.py',345),
  ('expression -> expression LESS_THAN expression','expression',3,'p_expression','rules.py',346),
  ('expression -> expression LESS_THAN_EQUAL expression','expression',3,'p_expression','rules.py',347),
  ('expression -> expression AND expression','expression',3,'p_expression','rules.py',348),
  ('expression -> expression OR expression','expression',3,'p_expression','rules.py',349),
  ('expression -> NOT expression','expression',2,'p_expression','rules.py',350),
  ('expression -> arrayaccess','expression',1,'p_expression','rules.py',352),
  ('expression -> function_call','expression',1,'p_expression','rules.py',353),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','rules.py',354),
]
