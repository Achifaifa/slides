#!/usr/bin/env python

import copy, json, time
from ply import lex, yacc

# Token list

tokens = ['LIST', 'SHOW', 'OF', 'DATA', 'LEAVE', 'SIT', 'MAP', 'IS', 'WORD', 'DONE', 'FIELD']
data_tokens = ['NAME', 'EMAIL', 'CITY', 'TRANSPORT']

# States and data mode buffer

states = (
   ('data','exclusive'),
)
globaldata={"cli_prompt":"",
            "mode":"",
            "newmember":{"city": "", 
                        "location": "", 
                        "name": "", 
                        "transport": "", 
                        "email": ""
            }
}
emptymember=copy.copy(globaldata['newmember'])

# Normal mode tokens

def t_DATA(t):
  r'(JOIN)|(ALTER)'
  globaldata['mode']=t.value
  t.lexer.begin('data')
  globaldata['cli_prompt']=">"
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

# Data mode tokens

def t_data_DONE(t):
  r'DONE'
  t.lexer.begin('INITIAL')
  globaldata['cli_prompt']=""
  return t

def t_data_WORD(t):
  r'[a-zA-Z][a-zA-Z_.@0-9]*'
  t.type = 'WORD' if t.value not in data_tokens else 'FIELD'
  return t

def t_data_error(t):

  print "Illegal character '%s'"%t.value[0] 
  t.lexer.skip(1)

# Global tokens

t_ANY_ignore = " \t"

# Rules

def p_state(p):
  '''stat : map 
          | list
          | wargs 
          | data
          | spec'''

  pass

def p_list(p):
  '''list : LIST'''

  print "|--group members\n|",
  print "\n| ".join([i['name'] for i in datadict])
  print "|--end"

def p_map(p):
  '''map : MAP'''

  print "GENERATING MAP"

def p_wargs(p):
  '''wargs : LEAVE WORD'''

  global datadict
  print "| --removing %s"%p[2]
  datadict=[i for i in datadict if i['name']!=p[2]]
  print "| --end"

def p_spec(p):
  '''spec : SIT WORD WORD
          | SHOW WORD IS WORD
          | SHOW WORD OF WORD'''

  print p

def p_data(p):
  '''data : DATA WORD
          | DONE
          | FIELD WORD'''

  if p[1] in ['JOIN', 'ALTER']:
    if globaldata['mode']=="JOIN": globaldata["newmember"]["name"]=p[2]
    if globaldata["mode"]=="ALTER": globaldata["newmember"]=[i for i in datadict if i['name']==p[2]][0]
  elif p[1] in data_tokens: globaldata["newmember"][p[1].lower()]=p[2]
  elif p[1]=="DONE": 
    if globaldata['mode']=="JOIN": datadict.append(copy.copy(globaldata["newmember"]))
    globaldata['newmember']=copy.copy(emptymember)


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
  print "PTML 0.1"
  print time.strftime('%Y-%m-%d - %H%M')
  print "-----------------------------------------"
  while 1:
    try: s = raw_input(globaldata['cli_prompt'])

    # In case of exception, save the data on file and exit
    except: 
      with open("./data.json","w+") as data:
        data.write(json.dumps(datadict))
      break

    # Repeat if there was an empty string, parse if not
    if not s: continue
    yacc.parse(s)
