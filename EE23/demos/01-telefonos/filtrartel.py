#! /usr/bin/env python

with open("./telefonos","r") as tel:
  with open("./telefonos_alava","w+") as tel_al:
    with open("./telefonos_gipu","w+") as tel_gip:
      with open("./telefonos_biz","w+") as tel_biz:
        for line in tel:
          if line.split(" - ")[-1].startswith("945"): tel_al.write(line)
          if line.split(" - ")[-1].startswith("944"): tel_biz.write(line)
          if line.split(" - ")[-1].startswith("943"): tel_gip.write(line)

