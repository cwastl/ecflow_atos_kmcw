# Number of nodes/mpi-tasks/omp-threads:
# -------------------------------------
NNODES=$SLURM_JOB_NUM_NODES
export NUM_NODES=$SLURM_NNODES
# Total number of MPI tasks:
MPI_TASKS=$((SLURM_NTASKS - %NIO%))
# Number of MPI tasks per node:
MPITASKS_PER_NODE=$((MPI_TASKS/NNODES))
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

export NPROC=${MPI_TASKS}
export NSLOTS=$SLURM_NTASKS

export NPROMA=-8
export NPRGPNS=%NPRGPNS%
export NPRGPEW=%NPRGPEW%
export NPRTRV=%NPRGPEW%
export NPRTRW=%NPRGPNS%
export NSTRIN=%NP%
export NSTROUT=%NP%
export N_IO=%NIO%
export NEINI=0

export DR_HOOK=0
export DR_HOOK_SILENT=1
export DR_HOOK_IGNORE_SIGNALS=-1
export EC_PROFILE_HEAP=0
export EC_MPI_ATEXIT=0
