#! /usr/bin/env python

from os import system as DO

board=[[" " for i in range(3)] for i in range(3)]
players=["X","O"]

for i in range(9):
  DO('clear')
  print "\n-----\n".join(["|".join(j) for j in board])
  x,y=[int(k)-1 for k in raw_input("Player %s >"%players[i%2]).split(',')]
  board[y][x]=players[i%2] if board[y][x]==" " else board[y][x]
   
