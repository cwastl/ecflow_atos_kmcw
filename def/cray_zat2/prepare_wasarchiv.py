#!/usr/bin/env python3

import os

suite = "wasarchiv"
runs = ["00","12"]
ofamil = ["admin","runs"]
famil = ["main"]
members = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"]
tasks_comp = ["complete"]
tasks_clean = ["cleaning"]
tasks_trig = ["gettrig"]
tasks_main = ["copy","mv2ecfs"]

hpath="/home/ms/at/zat2/ecf/"

if not os.path.exists(hpath + suite):
   os.mkdir(hpath + suite)

os.chdir(hpath + suite)

for s in ofamil:
      
     if not os.path.lexists(s):
        os.mkdir(s)
        
     if s == "admin":

        for t in tasks_comp:

           if not os.path.lexists(s + "/" + t + ".ecf"):
              os.symlink(hpath + "scripts_wasarchiv/" + t + ".ecf", s + "/" + t + ".ecf")

     if s == "runs":

        os.chdir(s)

        if not os.path.lexists("dummy.ecf"):
           os.symlink(hpath + "scripts_wasarchiv/dummy.ecf", "dummy.ecf")

        for r in runs:

           if not os.path.exists("RUN_" + r):
              os.mkdir("RUN_" + r)  

           for t in tasks_clean:

              if not os.path.lexists("RUN_" + r + "/" + t + ".ecf"):
                 os.symlink(hpath + "scripts_wasarchiv/" + t + ".ecf", "RUN_" + r + "/" + t + ".ecf")

           for f in famil:

              if not os.path.exists("RUN_" + r + "/" + f):
                 os.mkdir("RUN_" + r + "/" + f)

              if f == "main":

                 for z in tasks_trig:

                    if not os.path.lexists("RUN_" + r + "/" + f + "/" + z + ".ecf"):
                      os.symlink(hpath + "scripts_wasarchiv/" + z + ".ecf", "RUN_" + r + "/" + f + "/" + z + ".ecf")

                 for m in members:

                    if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                       os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)

                    for t in tasks_main:
 
                       if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                          os.symlink(hpath + "scripts_wasarchiv/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")

