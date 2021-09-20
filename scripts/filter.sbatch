#!/bin/sh

#SBATCH --job-name=filter-mag
#SBATCH --account=pi-jevans
#SBATCH --partition=caslake
#SBATCH --ntasks-per-node=1  # number of tasks
#SBATCH --cpus-per-task=20    # number of threads per task

# LOAD MODULES
module load python

# LOAD CONDA ENVIRONMENT
source activate soc_of_soc

# DO COMPUTE WORK
python filter_mag.py
