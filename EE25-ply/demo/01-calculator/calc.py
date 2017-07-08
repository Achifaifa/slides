# A simple calculator.   This is from O'Reilly's "Lex and Yacc", p. 63.

tokens = ['NUMBER']
literals = ['=', '+', '-', '*', '/', '(', ')']
t_ignore = " \t"

def t_NUMBER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):
  print "Illegal character '%s'"%t.value[0] 
  t.lexer.skip(1)

# Parsing rules
precedence = (
  ('left', '+', '-'),
  ('left', '*', '/'),
  ('right', 'UMINUS'),
)

def p_statement_expr(p):
  'statement : expression'
  print p[1]

def p_expression_binop(p):
  '''expression : expression '+' expression
                | expression '-' expression
                | expression '*' expression
                | expression '/' expression'''
  if p[2] == '+':   p[0] = p[1] + p[3]
  elif p[2] == '-': p[0] = p[1] - p[3]
  elif p[2] == '*': p[0] = p[1] * p[3]
  elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
  "expression : '-' expression %prec UMINUS"
  p[0] = -p[2]

def p_expression_group(p):
  "expression : '(' expression ')'"
  p[0] = p[2]

def p_expression_number(p):
  "expression : NUMBER"
  p[0] = p[1]

def p_error(p):
  if p:
    print "Syntax error at '%s'"%p.value
  else:
    print "Syntax error at EOF"

# Build the lexer
from ply import lex, yacc
lex.lex()
yacc.yacc()

while 1:
  try:
    s = raw_input('cal> ')
  except EOFError:
    break
  if not s:
    continue
  yacc.parse(s)
