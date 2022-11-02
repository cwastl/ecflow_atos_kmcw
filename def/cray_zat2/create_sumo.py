#!/usr/bin/env python3
#
#CREATE SUMO SUITE DEFINITION FILE
#
#OUTPUT: sumo.def and *.job0 - task files
#
#CREATED: 2022-02-04
#
#AUTHOR: C. Weidle, most parts stolen from C.Wastl
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
suite_name = "sumo"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [0,1]

# forecasting range
fcst = 60

# forecasting range control member
fcstctl = 60 

# coupling frequency
couplf = 1

# block transfer to speed up
blocks = 6             #block size

#archive Files to ECFS
ecfs = False

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
  'o00_1' : '0545',
  'o00_2' : '1255',
  'o12_1' : '1745',
  'o12_2' : '2155',
  'c00_1' : '07:30',
  'c00_2' : '11:00',
  'c12_1' : '19:30',
  'c12_2' : '22:00',
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

#def family_operator():
#
#   return Family("operator", 
#
#      [
#         Task("switch_schost",
#             Edit(
#                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
#                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
#                NAME="switch_sc",
#             ),
#             Label("info", ""),
#             Defstatus("suspended"),
#          )
#      ],
#
#      [
#         Task("switch_sthost",
#             Edit(
#                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
#                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
#                NAME="switch_st",
#             ),
#             Label("info", ""),
#             Defstatus("suspended"),
#          )
#       ],
#    )
#
def family_dummy(startc1,startc2):

    # Family dummy
    return Family("dummy",

#       # Family ez_trigger
#       [
#         Family("ez_trigger",
#
#            # Task dummy1
#            [
#               Task("dummy1",
#                  Edit(
#                     NP=1,
#                     CLASS='ns',
#                     NAME="dummy1",
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Defstatus("suspended"),
#               )
#            ]
#         )
#       ],
#
#       # Family check_obs
#       [
#         Family("check_obs",
#
#            # Task dummy2
#            [
#               Task("dummy2",
#                  Complete("../../obs == complete"),
#                  Edit(
#                     NP=1,
#                     CLASS='ts',
#                     NAME="dummy2",
#                  ),
#                  Label("run", ""),
#                  Label("error", ""),
#                  Time(startc1),
#               )
#            ]
#         )
#       ],

       # Family check_main
       [
         Family("check_main",

            # Task dummy2
            [
               Task("dummy2",
                  Complete("../../main == complete"),
                  Edit(
                     NP=1,
                     CLASS='ns',
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

def family_cleaning(startc1):

   return Task("cleaning",
             Trigger("./main == complete"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="cleaning",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

#def family_mirror():
#
#   return Task("mirror",
#             Trigger("main == complete"),
#             Edit(
#                NP=1,
#                CLASS='ns',
#                NAME="mirror",
#                ANZMEMB=anzmem,
#             ),
#             Label("run", ""),
#             Label("info", ""),
#
#          )
#
#def family_sumo():
#
#   # Family SUMO
#   return Family("sumo",
#
#      Edit(LEADT=fcst,
#           ACCOUNT=account,
#           HARPI=harpi,
#           VERIF=verifm),
#
#         # Task harpio
#         [
#            Task("harpio",
#                Trigger(":HARPI == 1 and ../main == complete"),
#                Complete(":LEAD < :LEADT or :HARPI == 0"),
#                Edit(
#                   ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
#                   ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
#                   NAME="harpio",
#                ),
#                Label("run", ""),
#                Label("info", ""),
#            ) 
#         ],
#
#         # Task verif
#         [
#            Task("verif",
#               Trigger(":VERIF == 1 and ../main == complete"),
#               Complete(":LEAD < :LEADT or :VERIF == 0"),
#               Edit(
#                  NP=1,
#                  CLASS='ns',
#                  NAME="verif",
#               ),
#               Label("run", ""),
#               Label("info", ""),
#            )
#         ],
#      )
#
#def family_obs(starto1,starto2) :
#
#    # Family OBS
#    return Family("obs",
#
#       Edit(ASSIM=assimi),
#
#       # Task assim/getobs
#       [
#          Task("getobs",
#             Trigger(":ASSIM == 1 and /claef:TIME > {} and /claef:TIME < {}".format(starto1,starto2)),
#             Complete(":ASSIM == 0"),
#             Meter("obsprog", -1, 3, 3),
#             Edit(
#                NP=1,
#                CLASS='ns',
#                NAME="getobs",
#             ),
#             Label("run", ""),
#             Label("info", ""),
#          )
#       ],
#
#       # Task assim/pregps
#       [
#          Task("pregps",
#             Trigger(":ASSIM == 1 and getobs == complete"),
#             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
#             Edit(
#                NP=1,
#                CLASS='ns',
#                NAME="pregps",
#             ),
#             Label("run", ""),
#             Label("info", ""),
#             Label("error", "")
#          )
#       ],
#
#       # Task assim/bator
#       [
#          Task("bator",
#             Trigger(":ASSIM == 1 and getobs == complete"),
#             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
#             Edit(
#                NP=1,
#                CLASS='ns',
#                NAME="bator",
#             ),
#             Label("run", ""),
#             Label("info", ""),
#             Label("error", "")
#          )
#       ],
#
#       # Task assim/bator3D
#       [
#          Task("bator3D",
#             Trigger(":ASSIM == 1 and pregps == complete"),
#             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
#             Edit(
#                NP=1,
#                CLASS='ns',
#                NAME="bator3D",
#             ),
#             Label("run", ""),
#             Label("info", ""),
#          )
#       ],
#    )

def family_main(starttime1,starttime2):

   # Family MAIN
   return Family("main",
      Trigger("/sumo:TIME > {} and /sumo:TIME < {}".format(starttime1,starttime2)),
      Edit(
         LEADT=fcst,
         ARCHIV=ecfs),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

#            # Task 927atm
#            [
#               Task("927",
#                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
#                  Event("d"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=16,
#                     CLASS='nf',
#                     NAME="927_{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task 927/surf
#            [
#               Task("927surf",
#                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
##                  Trigger("pgd == complete"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='nf',
#                     NAME="927surf{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Label("error", ""),
#               )
#            ],
#
#            # Task assim/sstex
#            [
#               Task("sstex",
#                  Trigger(":ASSIM == 1 and ../../obs/getobs == complete and ../MEM_{:02d}/927:d".format(mem)),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     NAME="sstex{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task assim/addsurf
#            [
#               Task("addsurf",
#                  Trigger(":ASSIM == 1 and sstex == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     NAME="addsurf{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task assim/varbccomb
#            [
#               Task("varbccomb",
#                  Trigger(":ASSIM == 1 and addsurf == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     NAME="varbccomb{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task assim/screening 3D
#            [
#               Task("screen",
#                  Trigger(":ASSIM == 1 and varbccomb == complete and ../../obs/bator3D == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=36,
#                     CLASS='tp',
#                     EDA=eda,
#                     NAME="screen{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Label("error", "")
#               )
#            ],
#
#            # Task assim/screening surface
#            [
#               Task("screensurf",
#                  Trigger(":ASSIM == 1 and varbccomb == complete and ../../obs/bator == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='tp',
#                     NAME="screensurf{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Label("error", "")
#               )
#            ],
#
#            # Task assim/canari
#            [
#               Task("canari",
#                  Trigger(":ASSIM == 1 and screensurf == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ts',
#                     SEDA=seda,
#                     NAME="canari{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task assim/minimization
#            [
#               Task("minim",
#                  Trigger(":ASSIM == 1 and screen == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=36,
#                     CLASS='tp',
#                     ASSIMM=assimm,
#                     ENSJK=enjk,
#                     NAME="minim{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
#            # Task assim/pertsurf
#            [
#               Task("pertsurf",
#                  Trigger(":ASSIM == 1 and canari == complete"),
#                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0 or :PERTS == 0 or :MEMBER == 00"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     NAME="pertsurf{:02d}".format(mem),
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
            # Task FPOS
            [
               Task("sumofpos",
#                  Trigger("927 == complete and minim == complete and canari == complete and pertsurf == complete"),
#                  Event("e"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     CLASS='np',
                     NAME="fpos_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task SURF2netcdf 
            [
               Task("convsurf2ncdf",
                  Trigger("../MEM_{:02d}/sumofpos == complete".format(mem)),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
          #           STEPS15=step15,
                     NAME="convsurf2ncdf_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task save to ECFS
            [
               Task("mv2ecfs",
                  Trigger("../MEM_{:02d}/convsurf2ncdf == complete".format(mem)),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
          #           STEPS15=step15,
                     NAME="mv2ecfs_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

#            # Task ADDGRIB
#            [
#               Task("addgrib",
#                  Trigger("../MEM_{:02d}/progrid:f".format(mem)),
#                  Complete(":LEAD < :LEADT"),
#                  Event("g"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='nf',
#                     STEPS15=step15,
#                     NAME="addgrib{:02d}".format(mem),
#                     BLOCKS=blocks,
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Label("error", ""),
#               )
#            ],
#
#            # Task Transfer 
#            [
#               Task("transfer",
#                  Trigger(":TRANSF == 1 and ../MEM_{:02d}/addgrib:g".format(mem)),
#                  Complete(":LEAD < :LEADT or :TRANSF == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     STEPS15=step15,
#                     NAME="transfer{:02d}".format(mem),
#                     BLOCKS=blocks,
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Label("error", ""),
#               )
#            ],
#
#            # Task MARS Archiv 
#            [
#               Task("archmars",
#                  Trigger(":ARCHIV == 1 and transfer == complete"),
#                  Complete(":LEAD < :LEADT or :ARCHIV == 0"),
#                  Edit(
#                     MEMBER="{:02d}".format(mem),
#                     NP=1,
#                     CLASS='ns',
#                     NAME="archmars{:02d}".format(mem),
#                     ANZMEMB=anzmem,
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#               )
#            ],
#
           ) for mem in members
         ]
       )

###########################
### create SUMO suite ###
###########################

print("\n=> creating suite definition\n");

defs = Defs().add(

          # Suite SUMO 
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

                ## suite variables
                #KOPPLUNG=couplf,
                #ASSIMC=assimc,
# 
#                # some variables for MARS archive
                MARS_FOR_BOND_DATASET=345,
                BOND_DHS_DRY_RUN_RETRIEVE=0,
                MARS_DOUBLE_ARCHIVE=0,
                ECFS_DOUBLE_ARCHIVE=0,

                # Running jobs remotely on HPCF
                ECF_OUT ='/%STHOST%/tcwork/' + user + '/sb/CLAEF/SUMO', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             Family("admin",

#                # Task clean logfile
#                Task("cleanlog",Date("28.*.*"),Time(timing['clean']),
#                   Edit(
#                      ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
#                      ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
#                      NAME="cleanlog"),
#                   Label("info", ""),
#                ),

                # Task complete if something went wrong on the previous day
                Task("complete", Cron(timing['comp']),
                   Edit( NAME="complete", CLASS="ns", NP=1, SUITENAME=suite_name ),
                   Label("run", ""),
                   Label("info", ""),
                ),

#                # Family operator if something goes wrong
#                family_operator(),

             ),

             Family("runs",

                RepeatDate("DATUM",start_date,end_date),
                # Task dummy
                Task("cleaning",
                  Trigger("./RUN_00 == complete and ./RUN_12 == complete and /sumo:TIME > 2300"),
                  Edit(
                     NP=1,
                     CLASS='ns',
                     NAME="cleaning",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                ),

                # Main Runs per day (00, 03, 06, 09,  12, 15, 18, 21)
                Family("RUN_00",
                   Edit( LAUF='00', VORHI=6, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
#                   family_dummy(timing['c00_1'],timing['c00_2']),
#                   family_cleaning(),
#                   family_obs(timing['o00_1'],timing['o00_2']),
                   family_main(timing['o00_1'],timing['o00_2']),
#                   family_harp(),
                ),

#                Family("RUN_03",
#                   Edit( LAUF='03', VORHI=9, LEAD=assimc, LEADCTL=assimc ),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['c03_1'],timing['c03_2']),
##                   family_cleaning(),
#                   family_obs(timing['o03_1'],timing['o03_2']),
#                   family_main(),
#                   family_harp(),
#                ),

#                Family("RUN_06",
#                   Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['c06_1'],timing['c06_2']),
#                   family_cleaning(),
#                   family_obs(timing['o06_1'],timing['o06_2']),
#                   family_main(),
##                   family_mirror(),
#                   family_harp(),
#                ),
#
#                Family("RUN_09",
#                   Edit( LAUF='09', VORHI=9, LEAD=assimc, LEADCTL=assimc ),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['c09_1'],timing['c09_2']),
#                   family_cleaning(),
#                   family_obs(timing['o09_1'],timing['o09_2']),
#                   family_main(),
#                   family_harp(),
#                ),

                Family("RUN_12",
                   Edit( LAUF='12',VORHI=6, LEAD=48, LEADCTL=48 ),
   
                   # add suite Families and Tasks
#                   family_dummy(timing['c12_1'],timing['c12_2']),
#                   family_cleaning(),
#                   family_obs(timing['o12_1'],timing['o12_2']),
                   family_main(timing['o12_1'],timing['o12_2']),
##                   family_mirror(),
#                   family_harp(),
                ),

#                Family("RUN_15",
#                   Edit( LAUF='15', VORHI=9, LEAD=assimc, LEADCTL=assimc ),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['c15_1'],timing['c15_2']),
#                   family_cleaning(),
#                   family_obs(timing['o15_1'],timing['o15_2']),
#                   family_main(),
#                   family_harp(),
#                ),
#
#                Family("RUN_18",
#                   Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
# 
#                   # add suite Families and Tasks
#                   family_dummy(timing['c18_1'],timing['c18_2']),
#                   family_cleaning(),
#                   family_obs(timing['o18_1'],timing['o18_2']),
#                   family_main(),
##                   family_mirror(),
#                   family_harp(),
#               ),
#
#                Family("RUN_21",
#                   Edit( LAUF='21', VORHI=9, LEAD=assimc, LEADCTL=assimc ),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['c21_1'],timing['c21_2']),
#                   family_cleaning(),
#                   family_obs(timing['o21_1'],timing['o21_2']),
#                   family_main(),
#                   family_harp(),
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

