#SBATCH --qos=express
#SBATCH --job-name=%TASK%_%FAMILY1:NOT_DEF%
#SBATCH --account=%ACCOUNT%
#SBATCH --output=%ECF_JOBOUT%
#SBATCH --error=%ECF_JOBOUT%
