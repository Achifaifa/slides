#! /usr/bin/env python

import os

for i in range(1,11): os.mkdir("Season %02i"%i)
for i in os.listdir("."):
  if i.endswith(".avi"):
    new=" ".join(i.split("_")[:4])+".avi"
    season=i.split("_")[3][:2]
    os.rename(i,"Season %s/"%season+new)
