#! /usr/bin/env python

import os, select, sys, termios, time

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
    return select.select([sys.stdin], [], [], 0.01)==([sys.stdin], [], [])

  c=""
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
  lastkey=tempkey if tempkey else lastkey

  if loopmanage():

    os.system('clear')
    print "\r lastkey - %s"%lastkey

while 1:
  os.system('clear')