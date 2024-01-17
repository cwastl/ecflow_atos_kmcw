#!/usr/bin/env python3
#
#CREATE C-LAEF SUITE DEFINITION FILE
#
#OUTPUT: claef.def and *.job0 - task files
#
#CREATED: 2022-05-03
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
home = os.path.join(os.getenv("HOME"),"CLAEF/suite");
incl = os.path.join(os.getenv("HOME"),"CLAEF/suite/include");

# to submit jobs remotely
schedule = "/usr/local/apps/schedule/1.4/bin/schedule";

################################
### top level suite settings ###
################################

#suite name
suite_name = "claef"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
#members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
#members = [41,42,43,44,45,46,47,48,49,50]
#members = [0]

# forecasting range
fcst = 3

# forecasting range control member
fcstctl = 3

# coupling frequency
couplf = 3

# use 15min output for precipitation
step15 = False

# assimilation switches
assimi = True   #assimilation yes/no
assimm = 0      #number of members without 3DVar
assimc = 3      #assimilation cycle in hours
eda = True      #ensemble data assimilation
seda = True     #surface eda
pertsurf = True #perturbation of sfx files

# use EnJK method of Endy yes/no
enjk = True

# use stochastic physics model error representation yes/no
stophy = True

# block transfer to speed up
blocks = 6             #block size

#transfer Files to ZAMG
trans = False

#archive Files to MARS
arch = False

#IO Server
n_io_serv=0

# SBU account, cluster and user name, logport
account = "atlaef";
schost  = "hpc";
user    = "kmcw";

# main runs time schedule
timing = {
  'comp' : '00:15',
  'clean' : '05:00',
  'o00_1' : '0145',
  'o00_2' : '0155',
  'o03_1' : '0445',
  'o03_2' : '0455',
  'o06_1' : '0745',
  'o06_2' : '0755',
  'o09_1' : '1045',
  'o09_2' : '1055',
  'o12_1' : '1345',
  'o12_2' : '1355',
  'o15_1' : '1645',
  'o15_2' : '1655',
  'o18_1' : '1945',
  'o18_2' : '1955',
  'o21_1' : '2245',
  'o21_2' : '2255',
  'c00_1' : '02:30',
  'c00_2' : '06:00',
  'c00_3' : '00:20',
  'c03_1' : '05:30',
  'c03_2' : '08:00',
  'c06_1' : '08:30',
  'c06_2' : '11:00',
  'c09_1' : '11:30',
  'c09_2' : '14:00',
  'c12_1' : '14:30',
  'c12_2' : '18:00',
  'c15_1' : '17:30',
  'c15_2' : '20:00',
  'c18_1' : '20:30',
  'c18_2' : '23:00',
  'c21_1' : '23:45',
  'c21_2' : '00:10',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# date to start the suite
#start_date = int(now.strftime('%Y%m%d'))
start_date = 20230509
end_date = 20230509

###########################################
#####define Families and Tasks#############
###########################################

def family_dummy(startc1,startc2):

    # Family dummy
    return Family("dummy",

       # Family ez_trigger
       [
         Family("ez_trigger",

            # Task dummy1
            [
               Task("dummy1",
                  Edit(
                     NP=1,
                     CLASS='nf',
                     NAME="dummy1",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Complete("1 == 1"),
               )
            ]
         )
       ]
     )

def family_obs(starto1,starto2) :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1 and ../dummy/ez_trigger/dummy1 == complete"),
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='nf',
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
                CLASS='nf',
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
                NPRGPNS=1,
                NPRGPEW=1,
                CLASS='nf',
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
                NPRGPNS=1,
                NPRGPEW=1,
                CLASS='nf',
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
         ASSIM=assimi,
         LEADT=fcst,
         PERTS=pertsurf,
         ARCHIV=arch,
         TRANSF=trans),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

            # Task 927atm
            [
               Task("927",
                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
                  Event("d"),
                #  Complete(":ASSIM == 1 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     NPRGPNS=16,
                     NPRGPEW=1,
                     CLASS='nf',
                     NAME="927_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
                  Complete(":ASSIM == 1 or :ASSIM == 0"),
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     NPRGPNS=1,
                     NPRGPEW=1,
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
                  Trigger(":ASSIM == 1 and ../../obs/getobs == complete and ../MEM_{:02d}/927:d".format(mem)),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
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
                     NPRGPNS=1,
                     NPRGPEW=1,
                     CLASS='nf',
                     NAME="addsurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/varbccomb
            [
               Task("varbccomb",
                  Trigger(":ASSIM == 1 and addsurf == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     NAME="varbccomb{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/screening 3D
            [
               Task("screen",
                  Trigger(":ASSIM == 1 and varbccomb == complete and ../../obs/bator3D == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     NPRGPNS=36,
                     NPRGPEW=1,
                     NNODES=2,
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
                  Trigger(":ASSIM == 1 and varbccomb == complete and ../../obs/bator == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     NPRGPNS=1,
                     NPRGPEW=1,
                     CLASS='nf',
                     SEDA=seda,
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
                     NPRGPNS=1,
                     NPRGPEW=1,
                     CLASS='nf',
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
                     NPRGPNS=36,
                     NPRGPEW=1,
                     CLASS='np',
                     NNODES=2,
                     ASSIMM=assimm,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/pertsurf
            [
               Task("pertsurf",
                  Trigger(":ASSIM == 1 and canari == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0 or :PERTS == 0 or :MEMBER == 00"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     NAME="pertsurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 001
            [
               Task("001",
                  Trigger("927 == complete and minim == complete and canari == complete and pertsurf == complete"),
                  Event("e"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=96,
                     NPRGPNS=8,
                     NPRGPEW=12,
                     CLASS='np',
                     STOCH=stophy,
                     PERTSU=pertsurf,
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
                  Complete(":ASSIM == 1 or :ASSIM == 0"),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     NPRGPNS=1,
                     NPRGPEW=1,
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
                  Complete(":ASSIM == 1 or :ASSIM == 0"),
                  Event("g"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     STEPS15=step15,
                     NAME="addgrib{:02d}".format(mem),
                     BLOCKS=blocks,
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task Transfer 
            [
               Task("transfer",
                  Trigger(":TRANSF == 1 and ../MEM_{:02d}/addgrib:g".format(mem)),
                  Complete(":LEAD < :LEADT or :TRANSF == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     STEPS15=step15,
                     NAME="transfer{:02d}".format(mem),
                     BLOCKS=blocks,
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task MARS Archiv 
            [
               Task("archmars",
                  Trigger(":ARCHIV == 1 and transfer == complete"),
                  Complete(":LEAD < :LEADT or :ARCHIV == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='nf',
                     NAME="archmars{:02d}".format(mem),
                     ANZMEMB=anzmem,
                  ),
                  Label("run", ""),
                  Label("info", ""),
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
                ECF_TRIES=2,           # number of reruns if task aborts

                # suite configuration variables
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,
                NIO=n_io_serv,
 
                ECF_JOB_CMD='troika -c /home/%USER%/CLAEF/suite/include/troika.yml submit -o %ECF_JOBOUT% %SCHOST% %ECF_JOB%',
                ECF_KILL_CMD='troika -c /home/%USER%/CLAEF/suite/include/troika.yml kill %SCHOST% %ECF_JOB%',
                ECF_STATUS_CMD='troika -c /home/%USER%/CLAEF/suite/include/troika.yml monitor %SCHOST% %ECF_JOB%',

             ),

             Family("runs",

                RepeatDate("DATUM",start_date,end_date),

                # Main Runs per day (00, 03, 06, 09,  12, 15, 18, 21)
                Family("RUN_00",
#                   RepeatString("LAUF",["00", "03", "06", "09", "12", "15", "18", "21" ]),
                   RepeatString("LAUF",["00"]),
                   Edit( VORHI=0, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
                   family_dummy(timing['c00_1'],timing['c00_2']),
#                   family_cleaning(),
                   family_obs(timing['o00_1'],timing['o00_2']),
                   family_main(),
                ),
                
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

