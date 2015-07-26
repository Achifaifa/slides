#! /usr/bin/env python

import random

with open("./telefonos","w+") as telefonos:
  for i in xrange(10000): telefonos.write("Nombre%08i - Apellido%08i - %i\n"%(i+1,i+1,random.randint(900000000,999999999)))
