#!/usr/bin/env python

import json, re, time
from ply import lex, yacc

# Token list

tokens = ['LIST', 'SHOW', 'WORD', 'ID']

def t_ID(t):
  r'[0-9]+'
  t.type='ID'
  return t
  
def t_WORD(t):
  r'[a-zA-Z][a-zA-Z_0-9]*'
  t.type = t.value if t.value in tokens else 'WORD'
  return t

def t_newline(t):

  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_error(t):

  print "Illegal character '%s'"%t.value[0] 
  t.lexer.skip(1)

# Global tokens

t_ignore = " \t"

# Rules

def p_state(p):
  '''stat : list
          | details'''

  pass

def p_list(p):
  '''list : LIST'''

  print "|--talk list\n|",
  print "\n|".join(sorted([" -- ".join((i['@id'],i['title'])) for i in datadict], key=lambda x: int(x.split(" ")[0])))
  print "|--end"


def p_details(p):
  '''details : SHOW ID'''

  global datadict
  try: 
    talk=[i for i in datadict if i['@id']==p[2]][0]
  except IndexError: 
    raise
  print "\n%s\n%s - %s - %s\n----------\n%s\n%s"%(talk['title'], i['date'], i['duration'], i['room'], i['description'], i['abstract'])

def p_error(p):
  if p:
    print "Syntax error at '%s'"%p.value
  else:
    print "Syntax error at EOF"

# Start the interpreted if the file is launched

if __name__=="__main__":

  # Start lex/yacc
  lex.lex()
  yacc.yacc()

  # Load data
  with open("./data.json","r") as data:
    datadict=json.loads(data.read())

  # Enter interpreter loop
  print "PyConES 2017 scheduletron"
  print time.strftime('%Y-%m-%d - %H%M')
  print "-----------------------------------------"
  while 1:
    s = raw_input('>')

    # Repeat if there was an empty string, parse if not
    if not s: continue
    yacc.parse(s)
