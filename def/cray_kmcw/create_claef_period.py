#!/usr/bin/env python3
#
#CREATE C-LAEF SUITE DEFINITION FILE
#
#OUTPUT: claef.def and *.job0 - task files
#
#CREATED: 2019-01-14
#
#AUTHOR: C. Wastl
###########################################################

#load modules
import os
from ecflow import *
import datetime

# get current date
now = datetime.datetime.now()

# ecFlow home and include paths
home = os.path.join(os.getenv("HOME"),"ecf");
incl = os.path.join(os.getenv("HOME"),"ecf/include");

# to submit jobs remotely
schedule = "/usr/local/apps/schedule/1.4/bin/schedule";

################################
### top level suite settings ###
################################

#suite name
suite_name = "claef_2"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [13]

# forecasting range
fcst = 21

# forecasting range control member
fcstctl = 21

# coupling frequency
couplf = 3

# use 15min output for precipitation
step15 = False 

# use GL Tool yes/no, if no - 901 is used
gl = True

# assimilation switches
assimi = False   #assimilation yes/no
assimm = 0      #number of members without 3DVar
assimc = 6      #assimilation cycle in hours
eda = False      #ensemble data assimilation
seda = False     #surface eda

# use EnJK method of Endy yes/no
enjk = True

# use stochastic physics model error representation yes/no
stophy = True

# SBU account, cluster and user name, logport
account = "atlaef";
schost  = "cca";
user    = "kmcw";
logport = 36652;

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# user date (default is system date)
start_date = 20160701
end_date = 20160731

###########################################
#####define Families and Tasks#############
###########################################

def family_lbc():

    # Family LBC
    return Family("lbc",

       Edit(
          GL=gl),

       # Task getlbc
       [
          Task("getlbc",
             Trigger(":GL == 0"),
             Complete(":GL == 1"),
             Event("a"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getlbc",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", ""),
          )
       ],

       # Family MEMBER
       [

         Family("MEM_{:02d}".format(mem),

          # Task divlbc
          [
             Task("divlbc",
                Trigger(":GL == 0 and ../getlbc:a"),
                Complete(":GL == 1 or :MEMBER == 00"),
                Event("b"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   MEMBER="{:02d}".format(mem),
                   NAME="divlbc{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task 901
          [
             Task("901",
                Trigger(":GL == 0 and divlbc:b"),
                Complete(":GL == 1 or :MEMBER == 00"),
                Event("c"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   MEMBER="{:02d}".format(mem),
                   NAME="901_{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
                Label("error", ""),
             )
          ],

          # Task getlbc_gl
          [
             Task("getlbc_gl",
                Trigger(":GL == 1"),
                Complete(":GL == 0"),
                Edit(
                   NP=1,
                   CLASS='ns',
                   SUITENAME=suite_name,
                   MEMBER="{:02d}".format(mem),
                   NAME="getlbcgl{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
             )
          ],

          # Task GL
          [
             Task("gl",
                Trigger(":GL == 1 and getlbc_gl == complete"),
                Complete(":GL == 0"),
                Edit(
                   MEMBER="{:02d}".format(mem),
                   NP=1,
                   CLASS='nf',
                   NAME="gl{:02d}".format(mem),
                ),
                Label("run", ""),
                Label("info", ""),
             )
          ],

        ) for mem in members

      ]
    )

def family_obs() :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1"),
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="getobs",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],

       # Task assim/pregps
       [
          Task("pregps",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="pregps",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", "")
          )
       ],

       # Task assim/bator
       [
          Task("bator",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", "")
          )
       ],

       # Task assim/bator3D
       [
          Task("bator3D",
             Trigger(":ASSIM == 1 and pregps == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="bator3D",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],
    )

def family_main():

   # Family MAIN
   return Family("main",

      Edit(
         GL=gl,
         ASSIM=assimi,
         LEADT=fcst),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

            # Task 927atm
            [
               Task("927",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
                  Event("d"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='nf',
                     NAME="927_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

#            # Task 927/PGD
#            [
#              Task("pgd",
#                 Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
#                 Edit(
#                    MEMBER="{:02d}".format(mem),
#                    NP=1,
#                    CLASS='nf',
#                    NAME="pgd{:02d}".format(mem),
#                 ),
#                 Label("run", ""),
#                 Label("info", ""),
#               )
#            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger(":GL == 1 and ../../lbc/MEM_{:02d}/gl == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901 == complete or :GL == 0 and ../../lbc/MEM_{:02d}/901:c".format(mem,mem,mem)),
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     NAME="927surf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task assim/sstex
            [
               Task("sstex",
                  Trigger(":ASSIM == 1 and ../MEM_{:02d}/927:d".format(mem)),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="sstex{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/addsurf
            [
               Task("addsurf",
                  Trigger(":ASSIM == 1 and sstex == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="addsurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/screening 3D
            [
               Task("screen",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator3D == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     CLASS='np',
                     EDA=eda,
                     NAME="screen{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/screening surface
            [
               Task("screensurf",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='np',
                     NAME="screensurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/canari
            [
               Task("canari",
                  Trigger(":ASSIM == 1 and screensurf == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     SEDA=seda,
                     NAME="canari{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/minimization
            [
               Task("minim",
                  Trigger(":ASSIM == 1 and screen == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     CLASS='np',
                     ASSIMM=assimm,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 001
            [
               Task("001",
                  Trigger("927 == complete and minim == complete and canari == complete"),
                  Event("e"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=360,
                     CLASS='np',
                     STOCH=stophy,
                     STEPS15=step15,
                     NAME="001_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Trigger("../MEM_{:02d}/001:e".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     STEPS15=step15,
                     NAME="progrid{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task ADDGRIB
            [
               Task("addgrib",
                  Trigger("../MEM_{:02d}/progrid:f".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     STEPS15=step15,
                     NAME="addgrib{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

           ) for mem in members
         ]
       )

###########################
### create C-LAEF suite ###
###########################

print("\n=> creating suite definition\n");

defs = Defs().add(

          # Suite C-LAEF
          Suite(suite_name).add(

             Edit(
                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path
                ECF_TRIES=1,           # number of reruns if task aborts

                # suite configuration variables
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,
 
                # Running jobs remotely on HPCF
                ECF_OUT = '/scratch/ms/at/' + user + '/ECF', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             Family("runs",

                RepeatDate("DATUM",start_date,end_date),

                # Main Runs per day (00, 06, 12, 18)
                Family("RUN_00",
                   Edit( LAUF='00', VORHI=0, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
                   family_lbc(),
                   family_obs(),
                   family_main(),
                ),

#                Family("RUN_06",
#                   Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
#                   Trigger("RUN_00 == complete"), 
#
#                   # add suite Families and Tasks
#                   family_lbc(),
#                   family_obs(),
#                   family_main(),
#                ),
#
#                Family("RUN_12",
#                   Edit( LAUF='12',VORHI=0, LEAD=fcst, LEADCTL=fcst ),
#                   Trigger("RUN_06 == complete"), 
#   
#                   # add suite Families and Tasks
#                   family_lbc(),
#                    family_obs(),
#                    family_main(),
#                ),
#
#                Family("RUN_18",
#                   Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
#                   Trigger("RUN_12 == complete"), 
#
#                   # add suite Families and Tasks
#                   family_lbc(),
#                   family_obs(),
#                   family_main(),
#                ),
             )             
          )
       )

###################################
### check and save C-LAEF suite ###
###################################

print("=> checking job creation: .ecf -> .job0");
print(defs.check_job_creation());
print("=> saving definition to file " + suite_name + ".def\n");
defs.save_as_defs(suite_name + ".def");
exit(0);

