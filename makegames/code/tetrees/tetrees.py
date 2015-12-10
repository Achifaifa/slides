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

  timem["timepool"]=0 if timem["timepool"]*1000>=300 else timem["timepool"]+time.time()-timem["previoustime"]
  timem["previoustime"]=time.time()
  return not timem["timepool"]

def pressed():

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

def merge():

  global world    #Shhhh...
  global curpiece #No pain now

  tempworld=copy.deepcopy(world)

  for numi, i in enumerate(curpiece["piece"]):
    for numj, j in enumerate(i):
      if j=="#":
        tempworld[numi+curpiece["coords"][0]][numj+curpiece["coords"][1]]="#"
  world=tempworld
  curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}

  processlines()

def output():

  os.system('clear')
  tempworld=copy.deepcopy(world)

  if curpiece:
    for numi, i in enumerate(curpiece["piece"]):
      for numj, j in enumerate(i):
        if j=="#":
          tempworld[numi+curpiece["coords"][0]][numj+curpiece["coords"][1]]=j 

  for i in tempworld: print " ".join(i)

def collision():

  piece=curpiece["piece"]
  coords=curpiece["coords"]
  if coords[0]+len(piece)>21: return 0
  for numi, i in enumerate(piece[-1]):
    if i=="#" and world[coords[0]+len(piece)][coords[1]+numi]=="#": return 1

def movepiece(direction):

  global curpiece #Yeah I know

  try:
    if curpiece is None:
      curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}
  except UnboundLocalError:
    curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}

  contact=collision()

  if direction==keys[0] or not timem["timepool"]: 
    if curpiece["coords"][0]+len(curpiece["piece"])>=22 or contact:
      merge()
    else:
      curpiece["coords"][0]+=1
  if direction==keys[1] and curpiece["coords"][1]-1>=0: 
    curpiece["coords"][1]-=1
  if direction==keys[2] and curpiece["coords"][1]+1+len(curpiece["piece"][0])<=10: 
    curpiece["coords"][1]+=1
  if direction==keys[3]: curpiece["piece"]=rotate()
  
def processlines():

  global world

  world=[i for i in world if not all(j=="#" for j in i)]
  world=([["."]*10]*(22-len(world)))+world

def rotate():

  temp=[[] for i in curpiece["piece"][0]]
  for i in curpiece["piece"]:
    for numj,j in enumerate(i):
      temp[numj].append(j)
  temp=[i[::-1] for i in temp]
  return temp

def mainloop():

  tempkey=pressed()
  try: lastkey=tempkey if tempkey in keys else lastkey
  except: lastkey=""

  if loopmanage() or lastkey:

    movepiece(lastkey)
    output()
    print "%s / %s"%(tempkey,lastkey)

if __name__=="__main__":
  while 1:
    mainloop()
