#! /usr/bin/env python

with open("./telefonos","r") as tel:
  with open("./telefonos_alava","w+") as tel_out:
    for line in tel:
      if line.split(" - ")[-1].startswith("945"): tel_out.write(line)