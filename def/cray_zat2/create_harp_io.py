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
import itertools

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
suite_name = "harp_io"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [0,1]

# forecasting range
fcst =60 

# forecasting range control member
fcstctl = 60 

# harp parameter
tasks_harp_param = ["T2m","rhum2m","u10m", "v10m","AccPcp3h","msl","grad","totcc","wgust"]
upper_params = ["T", "rhum"]
level = ["500", "700", "850", "900", "1000"]

for p in itertools.product(upper_params,level):
     tasks_harp_param.append('{0}{1}'.format(p[0],p[1]))

upper_params = ["u", "v"]
level = ["700", "850", "1000"]

for p in itertools.product(upper_params,level):
     tasks_harp_param.append('{0}{1}'.format(p[0],p[1]))

# limit number of parallel jobs
harp_limit = 15

##run harp
harpi = True
#
##save Files vor Ment verif tool
verifm = False

# SBU account, cluster and user name, logport
account = "ata01";
schost  = "cca";
sthost  = "sc1";
user    = "zat2";
logport = 38776;

## main runs time schedule
timing = {
  'comp' : '00:30',
  'clean' : '05:00',
  'ho00_1' : '0710',
  'ho00_2' : '0930',
  'he00_1' : '0810',
  'he00_2' : '1030',
  'he06_1' : '1410',
  'he06_2' : '1630',
  'ho12_1' : '2010',
  'ho12_2' : '2230',
  'he12_1' : '2110',
  'he12_2' : '2335',
  'co00_1' : '12:30',
  'co00_2' : '12:35',
  'ce00_1' : '12:30',
  'ce00_2' : '12:35',
  'ce06_1' : '18:30',
  'ce06_2' : '18:35',
  'co12_1' : '23:30',
  'co12_2' : '23:50',
  'ce12_1' : '23:30',
  'ce12_2' : '23:50',
}
#
## debug mode (1 - yes, 0 - no)
debug = 0;
#
anzmem = len(members)

# date to start the suite
start_date = int(now.strftime('%Y%m%d'))
#start_date = 20190415
end_date = 20530315

###########################################
#####define Families and Tasks#############
###########################################
##
#def family_operator():
##
#   return Family("operator", 
##
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
def family_dummy(startc1,startc2,MODE):

    # Family dummy
    return Family("check_harpio_{0}".format(MODE),

#       # Family ez_trigger
#       [
#         Family("ez_trigger",
#
#            # Task dummy1
#            [
#               Task("dummy1",
#                  Edit(
#                     NP=1,
#                     CLASS='ts',
#                     NAME="dummy1",
#                  ),
#                  Label("run", ""),
#                  Label("info", ""),
#                  Defstatus("suspended"),
#               )
#            ]
#         )
#       ]#,
#
#       # Family check_harpio_
#       [
#         Family("check_harpio_{0}".format(MODE),
#
#            # Task dummy2
            [
               Task("dummy2",
                  Complete("../harpio_{0} == complete".format(MODE)),
                  Edit(
                     ECF_JOBOUT="/scratch/ms/at/zat2/CLAEF/HARP/log_ecf/ecf.out",
                     ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                     NAME="dummy2",
                  ),
                  Label("run", ""),
                  Label("error", ""),
                  Time(startc1),
               )
            ]
         )
#       ],
#
#       # Family check_main
#       [
#         Family("check_main",
#
#            # Task dummy2
#            [
#               Task("dummy2",
#                  Complete("../../main == complete"),
#                  Edit(
#                     NP=1,
#                     CLASS='ts',
#                     NAME="dummy2",
#                  ),
#                  Label("run", ""),
#                  Label("error", ""),
#                  Time(startc2),
#               )
#            ]
#         )
#       ]
#    )

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

def family_transfer(MODE):

   return Task("transfer_{0}".format(MODE),
             Trigger("harpio_{0} == complete".format(MODE)),
             Edit(
               ECF_JOBOUT="/scratch/ms/at/zat2/CLAEF/HARP/log_ecf/transfer_{0}.out".format(MODE),
               ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
               MODE=MODE),
             Label("run", ""),
             Label("info", ""),
          )

def family_harp(starttime1,starttime2, MODE):

   # Family HARP
   return Family("harpio_{0}".format(MODE),
      Trigger("/harp_io:TIME > {} and /harp_io:TIME < {}".format(starttime1,starttime2)),

      Edit(LEADT=fcst,
           ACCOUNT=account,
           HARPI=harpi,
           MODE=MODE),

      InLimit("harp_limit"),
#         # Task harpio
      [
         Task("harpio_{0}".format(par),
            #Trigger(":HARPI == 1 and ../main == complete"),
            #Complete(":LEAD < :LEADT or :HARPI == 0"),
            Edit(
               ECF_JOBOUT="/scratch/ms/at/zat2/CLAEF/HARP/log_ecf/harp_{0}_{1}.out".format(par,MODE),
               ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
               PARAM="{0}".format(par)),
               Label("run", ""),
               Label("info", ""),
            ) for par in tasks_harp_param
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
                #KOPPLUNG=couplf,
                #ASSIMC=assimc,
 
                # Running jobs remotely on HPCF
                ECF_OUT ='/%STHOST%/tcwork/' + user + '/sb/GAGA', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),
             Limit("harp_limit", harp_limit),

             Family("admin",

                # Task complete if something went wrong on the previous day
                Task("complete", Cron(timing['comp']),
                   Edit( NAME="complete", CLASS="ts", NP=1, SUITENAME=suite_name ),
                   Label("run", ""),
                   Label("info", ""),
                ),

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
                   Edit( LAUF='00', VORHI=6, LEAD=fcst),

                   # add suite Families and Tasks
                   family_dummy(timing['co00_1'],timing['co00_2'],'oper'),
                   family_harp(timing['ho00_1'],timing['ho00_2'], 'oper'),
                   family_transfer('oper'),
                   family_dummy(timing['ce00_1'],timing['ce00_2'],'esuite'),
                   family_harp(timing['he00_1'],timing['he00_2'], 'esuite'),
                   family_transfer('esuite'),
                ),

#                Family("RUN_06",
#                   Edit( LAUF='06', VORHI=6, LEAD=fcst),
#
#                   # add suite Families and Tasks
#                   family_dummy(timing['ce06_1'],timing['ce06_2'],'esuite'),
#                   family_harp(timing['he06_1'],timing['he06_2'], 'esuite'),
#                   family_transfer('esuite'),
#                ),

                Family("RUN_12",
                   Edit( LAUF='12', VORHI=6, LEAD=fcst),

                   # add suite Families and Tasks
                   family_dummy(timing['co12_1'],timing['co12_2'], 'oper'),
                   family_harp(timing['ho12_1'],timing['ho12_2'], 'oper'),
                   family_transfer('oper'),
                   family_dummy(timing['ce12_1'],timing['ce12_2'], 'esuite'),
                   family_harp(timing['he12_1'],timing['he12_2'], 'esuite'),
                   family_transfer('esuite'),
                )
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

