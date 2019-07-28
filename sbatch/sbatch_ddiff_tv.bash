#!/bin/bash
#SBATCH --array=1-1295%500
#SBATCH --time=2-00:00:00
#SBATCH --open-mode=truncate
#SBATCH --output=sbatch_ddiff_tv_out.txt

. /etc/profile

module load lang/python/3.6.2
python3.6 ../python/sbatch_ddiff_tv.py ${SLURM_ARRAY_TASK_ID}

