#!/bin/bash
#SBATCH --array=1-1385%500
#SBATCH --open-mode=truncate
#SBATCH --output=sbatch_calc_tv_out.txt

. /etc/profile

module load lang/python/3.6.2
python3.6 ../python/sbatch_calc_tv.py ${SLURM_ARRAY_TASK_ID} -f "/smallwork/bdallen/executable_files_500/*/*.tmp"


