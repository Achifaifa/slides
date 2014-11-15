#! /usr/bin/env python

import subprocess, random

for i in range(10):
  for j in range(50):
    subprocess.call(["touch","Jack_Sparrow_Saga_%02ix%02i_[Ripped_by_dude][%i][%i].avi"%(i+1,j+1,random.randint(10000,99999),random.randint(10000,99999))])