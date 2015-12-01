#! /usr/bin/env python

import os, select, sys, termios, time, tty

world=[["." for i in range(10)] for i in range(22)]
pieces=[["#","#","#","#"],
        [["#","#","."],[".","#","#"]],
        [[".","#","#"],["#","#","."]],
        [["#",".","."],["#","#","#"]],
        [[".",".","#"],["#","#","#"]],
        [["#","#"],["#","#"]]]
keys={"d":"c","l":"z","r":"v","rot":" "}
timem={"timepool":0,"previoustime":0}

def loopmanage():
  """
  Internally manages the main game loop cycles 
  """

  timem["timepool"]=0 if timem["timepool"]*1000>=300 else timem["timepool"]+time.time()-timem["previoustime"]
  timem["previoustime"]=time.time()
  return not timem["timepool"]

def pressed():
  """
  Returns a pressed key (Supposedly non-blocking)
  """

  def isData():
    return select.select([sys.stdin], [], [], 0.2)==([sys.stdin], [], [])

  c=0
  old_settings=termios.tcgetattr(sys.stdin)
  try:
    tty.setcbreak(sys.stdin.fileno())
    if isData():
      c=sys.stdin.read(1)
  finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return c

def mainloop():

  tempkey=pressed()
  try: lastkey=tempkey if tempkey else lastkey
  except: lastkey=""

  if loopmanage() or lastkey:

    os.system('clear')
    print "\rlastkey - [%s]"%lastkey
    print "\rtempkey - [%s]"%tempkey
    print timem

while 1:
  try:
    mainloop()
  except KeyboardInterrupt:
    exit()