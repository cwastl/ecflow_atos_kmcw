#!%SHELL:/bin/ksh%
#-----------------------------------------
#SBATCH --job-name=%NAME%
#SBATCH --account=%ACCOUNT%
#SBATCH --qos=%CLASS%
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=clemens.wastl@zamg.ac.at
#SBATCH --ntasks=%NP%
#SBATCH --threads-per-core=1
#SBATCH --cpus-per-task=1
#SBATCH --output=%ECF_JOBOUT%
#SBATCH --error=%ECF_JOBOUT%
#SBATCH --mem-per-cpu=16GB
#-----------------------------------------
source /etc/profile
