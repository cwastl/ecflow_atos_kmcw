#!/usr/bin/env python3
#
#CREATE SUITE DEFINITION FILE FOR WASARCHIVE
#
#OUTPUT: wasarchiv.def and *.job0 - task files
#
#CREATED: 2022-02-08
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
suite_name = "wasarchiv"

#ensemble members
members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
#members = [0,1]

# forecasting range
fcst = 60

# forecasting range control member
fcstctl = 60 

# coupling frequency
couplf = 1

#archive Files to ECFS
ecfs = False

# assimilation switches
assimc = 3      #assimilation cycle in hours

# SBU account, cluster and user name, logport
account = "atlaef";
schost  = "cca";
sthost  = "sc1";
user    = "zat2";
logport = 38776;

# main runs time schedule
timing = {
  'comp' : '01:40',
  'o00_1' : '0800',
  'o00_2' : '0900',
  'o12_1' : '2000',
  'o12_2' : '2100',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

# date to start the suite
start_date = int(now.strftime('%Y%m%d'))
#start_date = 20190415
end_date = 20221231

###########################################
#####define Families and Tasks#############
###########################################

def family_cleaning():

   return Task("cleaning",
             Trigger("main == complete"),
             Edit(
                NP=1,
                CLASS='ns',
                NAME="cleaning",
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_main(starttime1,starttime2):

   # Family MAIN
   return Family("main",
      Trigger("/wasarchiv:TIME > {} and /wasarchiv:TIME < {}".format(starttime1,starttime2)),

      # Fetch trigger file
      [
         Task("gettrig",
            Edit(
               NP=1,
               CLASS='ns',
               NAME="gettrig",
            ),
            Label("run", ""),
            Label("info", ""),
            Label("error", "")
         )
      ],


      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

            # Task copy to sc1
            [
               Task("copy",
                  Trigger("../gettrig == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="copy_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task save to ECFS
            [
               Task("mv2ecfs",
                  Trigger("copy == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="mv2ecfs_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

           ) for mem in members
         ]
       )

###########################
### create WASARCHIV suite ###
###########################

print("\n=> creating suite definition\n");

defs = Defs().add(

          # Suite WASARCHIV 
          Suite(suite_name).add(

             Edit(
                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path
                ECF_TRIES=1,           # number of reruns if task aborts

                # suite configuration variables
                STHOST=sthost,
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,

                # Running jobs remotely on HPCF
                ECF_OUT ='/%STHOST%/tcwork/' + user + '/sb/CLAEF/WASARCHIV', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             Family("admin",

                # Task complete if something went wrong on the previous day
                Task("complete", Cron(timing['comp']),
                   Edit( NAME="complete", CLASS="ns", NP=1, SUITENAME=suite_name ),
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

                # Main Runs per day (00, 12)
                Family("RUN_00",
                   Edit( LAUF='00', VORHI=6, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
                   family_main(timing['o00_1'],timing['o00_2']),
                   family_cleaning(),
                ),

                Family("RUN_12",
                   Edit( LAUF='12',VORHI=6, LEAD=48, LEADCTL=48 ),
   
                   # add suite Families and Tasks
                   family_main(timing['o12_1'],timing['o12_2']),
                   family_cleaning(),
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

