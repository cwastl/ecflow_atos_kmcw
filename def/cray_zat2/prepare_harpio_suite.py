#!/usr/bin/env python3

import os
import itertools

suite = "harp_io"
runs = ["00", "06", "12"]
ofamil = ["admin","runs"]
tasks_comp = ["complete"]
#famil = ["harp"]
members = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"]
tasks_ez_trigger = ["dummy1"]
tasks_harp = ["harpio_oper","harpio_esuite"]

tasks_harp_param = ["T2m","rhum2m","u10m", "v10m","AccPcp3h","msl","grad","totcc","wgust"]
upper_params = ["T", "rhum"]
level = ["500", "700", "850", "900", "1000"]

for p in itertools.product(upper_params,level):
     tasks_harp_param.append('{0}{1}'.format(p[0],p[1]))

upper_params = ["u", "v"]
level = ["700", "850", "1000"]

for p in itertools.product(upper_params,level):
     tasks_harp_param.append('{0}{1}'.format(p[0],p[1]))

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
              os.symlink(hpath + "scripts/" + t + ".ecf", s + "/" + t + ".ecf")

 
     if s == "runs":

        os.chdir(s)

        if not os.path.lexists("dummy.ecf"):
           os.symlink(hpath + "scripts_harp/dummy.ecf", "dummy.ecf")

        for r in runs:

           if not os.path.exists("RUN_" + r):
              os.mkdir("RUN_" + r)  

           if not os.path.exists("RUN_" + r + "/dummy"):
              os.mkdir("RUN_" + r + "/dummy")  

#           if not os.path.exists("RUN_" + r + "/dummy" + "/ez_trigger"):
#              os.mkdir("RUN_" + r + "/dummy" + "/ez_trigger")  

#           for s in tasks_ez_trigger:
#
#              if not os.path.lexists("RUN_" + r + "/dummy" + "/ez_trigger/" + s + ".ecf"):
#                 os.symlink(hpath + "scripts_harp/" + s + ".ecf", "RUN_" + r + "/dummy" + "/ez_trigger/" + s + ".ecf")

 #          for f in famil:
#
#              if not os.path.exists("RUN_" + r + "/" + f):
#                 os.mkdir("RUN_" + r + "/" + f)
#
#              if f == "harp":
#
           for t in tasks_harp:
              
              if not os.path.exists("RUN_{0}/check_{1}".format(r,t)):
                 os.mkdir("RUN_{0}/check_{1}".format(r,t))
 
              if not os.path.lexists("RUN_{0}/check_{1}/dummy2.ecf".format(r,t)):
                 os.symlink(hpath + "scripts_harp/dummy2.ecf", "RUN_{0}/check_{1}/dummy2.ecf".format(r,t))

              if not os.path.exists("RUN_{0}/{1}".format(r,t)):
                 os.mkdir("RUN_{0}/{1}".format(r,t))
                    
              for p in tasks_harp_param:

                 if not os.path.lexists("RUN_{0}/{1}/{2}.ecf".format(r,t,p)):
                    os.symlink(hpath + "scripts_harp/harpio.ecf", "RUN_{0}/{1}/harpio_{2}.ecf".format(r,t,p))
 
           if not os.path.lexists("RUN_{0}/transfer_oper.ecf".format(r)):
              os.symlink(hpath + "scripts_harp/transfer.ecf", "RUN_{0}/transfer_oper.ecf".format(r))
           if not os.path.lexists("RUN_{0}/transfer_esuite.ecf".format(r)):
              os.symlink(hpath + "scripts_harp/transfer.ecf", "RUN_{0}/transfer_esuite.ecf".format(r))
