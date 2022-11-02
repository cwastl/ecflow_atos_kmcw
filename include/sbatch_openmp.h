#!%SHELL:/bin/ksh%
#-----------------------------------------
#SBATCH --job-name=%NAME%
#SBATCH --account=%ACCOUNT%
#SBATCH --qos=%CLASS%
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=clemens.wastl@zamg.ac.at
#SBATCH --ntasks=%NP%
#SBATCH --hint=nomultithread
#SBATCH --cpus-per-task=4
#SBATCH --output=%ECF_JOBOUT%
#SBATCH --error=%ECF_JOBOUT%
#-----------------------------------------
source /etc/profile
