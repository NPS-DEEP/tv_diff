#!/bin/bash
#SBATCH --qos=qos_hamming
#SBATCH --partition=primary
#SBATCH --array=1-1135%700
#SBATCH --time=4-00:00:00
#SBATCH --open-mode=truncate
#SBATCH --output=sbatch_ddiff_tv_out.txt

. /etc/profile

module load lang/python/3.6.2
python3.6 ../python/sbatch_ddiff_tv.py ${SLURM_ARRAY_TASK_ID} -f "/smallwork/bdallen/executable_files_512/*/*.tv"

