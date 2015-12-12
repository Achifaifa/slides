#! /usr/bin/env python

import copy, os, random, select, sys, termios, time, tty

world=[["." for i in range(10)] for i in range(22)]
pieces=[["#","#","#","#"],
        [["#","#","."],[".","#","#"]],
        [[".","#","#"],["#","#","."]],
        [["#",".","."],["#","#","#"]],
        [[".",".","#"],["#","#","#"]],
        [[".","#","."],["#","#","#"]],
        [["#","#"],["#","#"]]]
keys=["c", "z", "v", " ", "q"]
timem={"timepool":0,"previoustime":0}
curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}
score={1:0, 2:0, 3:0, 4:0, "drops":0}

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

  for numi, i in enumerate(curpiece["piece"]):
    for numj, j in enumerate(i):
      if j=="#":
        world[numi+curpiece["coords"][0]][numj+curpiece["coords"][1]]="#"
  curpiece={"piece":copy.copy(random.choice(pieces)), "coords":[0,3]}
  if collision("down"): gameover()

  processlines()

def output():

  os.system('clear')
  tempworld=copy.deepcopy(world)

  for numi, i in enumerate(curpiece["piece"]):
    for numj, j in enumerate(i):
      if j=="#":
        tempworld[numi+curpiece["coords"][0]][numj+curpiece["coords"][1]]=j 


  for i in tempworld: print " ".join(i)

  print "score: %i"%(score["drops"]*2+score[1]*10+score[2]*50+score[3]*500+score[4]*1337)

def collision(direction):

  piece=curpiece["piece"]
  coords=curpiece["coords"]

  if direction=="down":
    for numi, i in enumerate(piece[-1]):
      try:
        if i=="#" and world[coords[0]+len(piece)][coords[1]+numi]=="#": return 1
        if piece[-2][numi]=="#" and world[coords[0]+len(piece)-1][coords[1]+numi]=="#": return 1
        if piece[-3][numi]=="#" and world[coords[0]+len(piece)-2][coords[1]+numi]=="#": return 1
      except IndexError: pass

  elif direction=="left":
    for numi, i in enumerate(piece):
      try:
        if i[0]=="#" and world[coords[0]+numi][coords[1]-1]=="#": return 1
        if i[1]=="#" and world[coords[0]+numi][coords[1]]=="#": return 1
        if i[2]=="#" and world[coords[0]+numi][coords[1]+1]=="#": return 1
      except IndexError: pass

  elif direction=="right":
    for numi, i in enumerate(piece):
      try:
        if i[-1]=="#" and world[coords[0]+numi][coords[1]+len(piece[0])]=="#": return 1
        if i[-2]=="#" and world[coords[0]+numi][coords[1]+len(piece[0])-1]=="#": return 1
        if i[-3]=="#" and world[coords[0]+numi][coords[1]+len(piece[0])-2]=="#": return 1
      except IndexError: pass

  return 0

def movepiece(direction):

  if direction==keys[0] or not timem["timepool"]: 
    if curpiece["coords"][0]+len(curpiece["piece"])>=22 or collision("down"):
      merge()
    else:
      curpiece["coords"][0]+=1
      if direction==keys[0]: score["drops"]+=1

  if direction==keys[1] and curpiece["coords"][1]-1>=0 and not collision("left"): 
    curpiece["coords"][1]-=1

  if direction==keys[2] and curpiece["coords"][1]+1+len(curpiece["piece"][0])<=10 and not collision("right"): 
    curpiece["coords"][1]+=1

  if direction==keys[3]: curpiece["piece"]=rotate()
  
def processlines():

  global world

  world=[i for i in world if not all(j=="#" for j in i)]
  removed=22-len(world)
  world=[["." for i in range(10)] for i in range(removed)]+world
  if removed: score[removed]+=1

def rotate():

  temp=[[] for i in curpiece["piece"][0]]
  if curpiece["coords"][1]+len(curpiece["piece"])>10: return curpiece["piece"]
  for i in curpiece["piece"]:
    for numj,j in enumerate(i):
      temp[numj].append(j)
  temp=[i[::-1] for i in temp]
  return temp

def gameover():

  os.system('clear')
  print "GAME OVER"
  print "\n1: %ix10: %i"%(score[1],score[1]*10)
  print "2: %ix50: %i"%(score[2],score[2]*50)
  print "3: %ix500: %i"%(score[3],score[3]*500)
  print "tetreeses: %ix1337: %i"%(score[4],score[4]*1337)
  print "drops: %i"%(score["drops"])
  print "\nTotal Score: %i"%(score["drops"]+score[1]*10+score[2]*50+score[3]*500+score[4]*1337)
  exit()

def mainloop():

  tempkey=pressed()
  try: lastkey=tempkey if tempkey in keys else lastkey
  except: lastkey=""
  if lastkey=="q": gameover()

  if loopmanage() or lastkey:

    movepiece(lastkey)
    output()

if __name__=="__main__":
  while 1:
    mainloop()
