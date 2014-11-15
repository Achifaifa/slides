#! /usr/bin/env python

import os, subprocess

for i in range(10): subprocess.call(["mkdir","Season %02i"%(i+1)])
for i in os.listdir(os.curdir):
  if i.endswith(".avi"):
    os.rename(i," ".join(i.split("_")[:4])+".avi")
    i=" ".join(i.split("_")[:4])+".avi"
    os.rename(i,"Season %02i"%(int(i.split()[3].split("x")[0]))+"/"+i)
    