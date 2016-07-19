# -*- coding: UTF-8 -*-
import json

with open("pisos.json", "r") as fin:
  data=json.load(fin) 

with open("pisos.csv", "w+") as fout:
  fields=[i for i in data[0]]
  fout.write(",".join(fields).replace("gps","latitude,longitude")+"\n")
  for i in data:
    for j in fields:
      if j=="gps": 
        fout.write(",".join([str(i) for i in i[j]]))
      else: 
        try: k=i[j]
        except: continue

        if isinstance(k,basestring): fout.write(k.encode("UTF-8").replace(",","|"))

        elif isinstance(k, list): fout.write("|".join(k))
        
      fout.write(",")
    fout.write("\n")

    