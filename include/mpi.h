export KMP_STACKSIZE=4G
export KMP_BLOCKTIME=12
export KMP_MONITOR_STACKSIZE=1G
export KMP_AFFINITY=scatter,granularity=fine
export FI_PROVIDER=mlx
export FI_MLX_TLS=dc_x,shm,self
export UCX_TLS=dc_x,sm,self
export TBB_MALLOC_SET_HUGE_SIZE_THRESHOLD=0
export TBB_MALLOC_USE_HUGE_PAGES=1
export HUGETLB_DEFAULT_PAGE_SIZE=2M
export TBB_MALLOC_SET_NEVER_RELEASING_THRESHOLD=8
export HUGETLB_NO_PREFAULT=yes
export HUGETLB_MORECORE=yes



# Software default environment variables :
# --------------------------------------
export DR_HOOK_IGNORE_SIGNALS=-1
export DR_HOOK_SILENT=1
export DR_HOOK_SHOW_PROCESS_OPTIONS=0
export MPL_MBX_SIZE=2048000000
export EC_PROFILE_HEAP=0
export EC_PROFILE_MEM=0
export EC_MPI_ATEXIT=0
export EC_MEMINFO=0







## MPI, openMP env, etc.
##-----------------------
#export PSM2_RANKS_PER_CONTEXT=2
#
#export MPI_DSM_CPULIST="0-35:allhosts"
#export MPI_DSM_DISTRIBUTE=1
#export MPI_DSM_VERBOSE=1
#
#export MPI_MEM_ALIGN=128
#export MPI_BUFFER_MAX=2000000
#export MPI_BUFS_PER_PROC=1024
#export MPI_REQUEST_MAX=400000
#
#export MKL_DYNAMIC=FALSE
#export F_UFMTENDIAN=big
#export FORT_BUFFERED=true
#export FORT_BLOCKSIZE=1048576
#
#export OMP_NUM_THREADS=1
##export OMP_DYNAMIC=FALSE
#export KMP_STACKSIZE=500m
#export KMP_MONITOR_STACKSIZE=500m
#export KMP_AFFINITY=disabled

