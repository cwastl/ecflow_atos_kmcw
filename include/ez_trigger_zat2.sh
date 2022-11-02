#!/bin/ksh
#SBATCH --job-name=ef06h012
#SBATCH --account=atlaef
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=clemens.wastl@zamg.ac.at
#SBATCH --output=/home/kmcw/CLAEF/suite/claef/ez_trigger_zat2.txt

##### Start with ecaccess-job-submit -ni ef12h036 -queueName hpc -mp "nothing to be done" -rc 1 ./ez_trigger.sh ######

set -ex

##--- Set date variables for actual model run
lagg=6
lagg2=9
HPROD=$MSJ_BASETIME

(( HRUN = $HPROD + $lagg))
if [[ $HRUN -ge 24 ]]
then
   (( HRUN = $HRUN - 24))
fi

HRJ=$(printf "%02d" $HRUN)

(( HRUN2 = $HPROD + $lagg2))
if [[ $HRUN2 -ge 24 ]]
then
   (( HRUN2 = $HRUN2 - 24))
fi

HRJ2=$(printf "%02d" $HRUN2)

# Set task complete for ecFlow
module load ecflow
export ECF_HOST=ecflow-tc2-zat2-001
export ECF_PORT=3141
suiteName='claef'
if [[ ${HPROD} == "12" ]]
then
   ecflow_client --requeue /${suiteName}/admin/dummy3
fi

if [[ ${HPROD} == "18" ]]
then
   ecflow_client --resume /${suiteName}/admin/dummy3
else
   ecflow_client --resume /${suiteName}/runs/RUN_${HRJ}/dummy/ez_trigger/dummy1 
   ecflow_client --resume /${suiteName}/runs/RUN_${HRJ2}/dummy/ez_trigger/dummy1 
fi
exit
