#! /usr/bin/env python

import copy, os, random, select, sys, termios, time, tty

world=[["." for i in range(10)] for i in range(22)]
pieces=[["#","#","#","#"],
        [["#","#","."],[".","#","#"]],
        [[".","#","#"],["#","#","."]],
        [["#",".","."],["#","#","#"]],
        [[".",".","#"],["#","#","#"]],
        [["#","#"],["#","#"]]]
keys=["c", "z", "v", " "]
timem={"timepool":0,"previoustime":0}
curpiece=None

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

def output():
  """
  Prints the current status of the game
  """

  os.system('clear')
  tempworld=copy.copy(world)
  for i in tempworld:
    print " ".join(i)

def movepiece(direction):

  try:
    if direction==keys[0]: curpiece["coords"][0]+=1
    if direction==keys[1]: curpiece["coords"][1]-=1
    if direction==keys[2]: curpiece["coords"][1]+=1
    if direction==keys[3]: rotate()
  except UnboundLocalError:
    curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}

def rotate():

  #[".",".","#"],["#","#","#"]
  temp=[[] for i in range(len(curpiece["piece"][0]))]
  for i in enumerate(curpiece["piece"]):
    for num,j in enumerate(i):
      temp[num].append(j)
  return [reversed(i) for i in temp]


def mainloop():

  tempkey=pressed()
  try: lastkey=tempkey if tempkey in keys else lastkey
  except: lastkey=""

  if loopmanage() or lastkey:

    movepiece(lastkey)
    output()

if __name__=="__main__"
  while 1:
    try:
      mainloop()
    except KeyboardInterrupt:
      exit()