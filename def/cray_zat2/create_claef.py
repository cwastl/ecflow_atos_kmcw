#!/usr/bin/env python3
#
#CREATE C-LAEF SUITE DEFINITION FILE
#
#OUTPUT: claef.def and *.job0 - task files
#
#CREATED: 2021-10-25
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
suite_name = "claef"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [0,1]

# forecasting range
fcst = 48

# forecasting range control member
fcstctl = 48

# coupling frequency
couplf = 1

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

#run harp
harpi = False

#save Files vor Ment verif tool
verifm = False

# SBU account, cluster and user name, logport
account = "atlaef";
schost  = "cca";
sthost  = "sc1";
user    = "zat2";
logport = 38776;

# main runs time schedule
timing = {
  'comp' : '00:20',
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
  'c00_1' : '03:30',
  'c00_2' : '07:00',
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
  'c21_1' : '23:30',
  'c21_2' : '00:15',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# date to start the suite
start_date = int(now.strftime('%Y%m%d'))
#start_date = 20190415
end_date = 20221231

###########################################
#####define Families and Tasks#############
###########################################

def family_operator():

   return Family("operator", 

      [
         Task("switch_schost",
             Edit(
                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                NAME="switch_sc",
             ),
             Label("info", ""),
             Defstatus("suspended"),
          )
      ],

      [
         Task("switch_sthost",
             Edit(
                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                NAME="switch_st",
             ),
             Label("info", ""),
             Defstatus("suspended"),
          )
       ],
    )

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
                     CLASS='ts',
                     NAME="dummy1",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Defstatus("suspended"),
               )
            ]
         )
       ],

       # Family check_obs
       [
         Family("check_obs",

            # Task dummy2
            [
               Task("dummy2",
                  Complete("../../obs == complete"),
                  Edit(
                     NP=1,
                     CLASS='ts',
                     NAME="dummy2",
                  ),
                  Label("run", ""),
                  Label("error", ""),
                  Time(startc1),
               )
            ]
         )
       ],

       # Family check_main
       [
         Family("check_main",

            # Task dummy2
            [
               Task("dummy2",
                  Complete("../../main == complete"),
                  Edit(
                     NP=1,
                     CLASS='ts',
                     NAME="dummy2",
                  ),
                  Label("run", ""),
                  Label("error", ""),
                  Time(startc2),
               )
            ]
         )
       ]
    )

def family_cleaning():

   return Task("cleaning",
             Trigger("dummy/ez_trigger/dummy1 == complete"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="cleaning",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_mirror():

   return Task("mirror",
             Trigger("main == complete"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="mirror",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_harp():

   # Family HARP
   return Family("harp",

      Edit(LEADT=fcst,
           ACCOUNT=account,
           HARPI=harpi,
           VERIF=verifm),

         # Task harpio
         [
            Task("harpio",
                Trigger(":HARPI == 1 and ../main == complete"),
                Complete(":LEAD < :LEADT or :HARPI == 0"),
                Edit(
                   ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                   ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                   NAME="harpio",
                ),
                Label("run", ""),
                Label("info", ""),
            ) 
         ],

         # Task verif
         [
            Task("verif",
               Trigger(":VERIF == 1 and ../main == complete"),
               Complete(":LEAD < :LEADT or :VERIF == 0"),
               Edit(
                  NP=1,
                  CLASS='ns',
                  NAME="verif",
               ),
               Label("run", ""),
               Label("info", ""),
            )
         ],
      )

def family_obs(starto1,starto2) :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1 and /claef:TIME > {} and /claef:TIME < {}".format(starto1,starto2)),
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='ts',
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
                CLASS='ts',
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
                CLASS='ts',
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
                CLASS='ts',
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
         SEDA=seda,
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
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='tf',
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
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
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
                     CLASS='ts',
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
                     CLASS='ts',
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
                     CLASS='ts',
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
                     CLASS='tp',
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
                     CLASS='tp',
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
                     CLASS='ts',
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
                     CLASS='tp',
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
                     CLASS='ts',
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
                     NP=360,
                     CLASS='tp',
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
                  Complete(":LEAD < :LEADT"),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
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
                  Event("g"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
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
                     CLASS='ts',
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
                     CLASS='ts',
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
                STHOST=sthost,
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,
 
                # some variables for MARS archive
                MARS_FOR_BOND_DATASET=345,
                BOND_DHS_DRY_RUN_RETRIEVE=0,
                MARS_DOUBLE_ARCHIVE=0,
                ECFS_DOUBLE_ARCHIVE=0,

                # Running jobs remotely on HPCF
                ECF_OUT ='/%STHOST%/tcwork/' + user + '/sb/CLAEF', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             Family("admin",

                # Task clean logfile
                Task("cleanlog",Date("28.*.*"),Time(timing['clean']),
                   Edit(
                      ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                      ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                      NAME="cleanlog"),
                   Label("info", ""),
                ),

                # Task complete if something went wrong on the previous day
                Task("complete", Cron(timing['comp']),
                   Edit( NAME="complete", CLASS="ts", NP=1, SUITENAME=suite_name ),
                   Label("run", ""),
                   Label("info", ""),
                ),

                # Family operator if something goes wrong
                family_operator(),

             ),

             Family("runs",

                RepeatDate("DATUM",start_date,end_date),

                # Task dummy
                Task("dummy",
                  Edit(
                     NP=1,
                     CLASS='ns',
                     NAME="dummy",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Defstatus("suspended"),
                ),

                # Main Runs per day (00, 03, 06, 09,  12, 15, 18, 21)
                Family("RUN_00",
                   Edit( LAUF='00', VORHI=6, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
                   family_dummy(timing['c00_1'],timing['c00_2']),
                   family_cleaning(),
                   family_obs(timing['o00_1'],timing['o00_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_03",
                   Edit( LAUF='03', VORHI=9, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c03_1'],timing['c03_2']),
                   family_cleaning(),
                   family_obs(timing['o03_1'],timing['o03_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_06",
                   Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c06_1'],timing['c06_2']),
                   family_cleaning(),
                   family_obs(timing['o06_1'],timing['o06_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_09",
                   Edit( LAUF='09', VORHI=9, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c09_1'],timing['c09_2']),
                   family_cleaning(),
                   family_obs(timing['o09_1'],timing['o09_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_12",
                   Edit( LAUF='12',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c12_1'],timing['c12_2']),
                   family_cleaning(),
                   family_obs(timing['o12_1'],timing['o12_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_15",
                   Edit( LAUF='15', VORHI=9, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c15_1'],timing['c15_2']),
                   family_cleaning(),
                   family_obs(timing['o15_1'],timing['o15_2']),
                   family_main(),
                   family_harp(),
                ),

                Family("RUN_18",
                   Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c18_1'],timing['c18_2']),
                   family_cleaning(),
                   family_obs(timing['o18_1'],timing['o18_2']),
                   family_main(),
                   family_harp(),
               ),

                Family("RUN_21",
                   Edit( LAUF='21', VORHI=9, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c21_1'],timing['c21_2']),
                   family_cleaning(),
                   family_obs(timing['o21_1'],timing['o21_2']),
                   family_main(),
                   family_harp(),
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

