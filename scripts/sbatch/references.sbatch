#!/bin/sh

#SBATCH --job-name=return-references
#SBATCH --account=pi-jevans
#SBATCH --partition=caslake
#SBATCH --ntasks-per-node=1  # number of tasks
#SBATCH --cpus-per-task=20    # number of threads per task
#SBATCH --output=return_references.out

# LOAD MODULES
module load python

# LOAD CONDA ENVIRONMENT
source activate soc_of_soc

# DO COMPUTE WORK
python /home/timothyelder/mag/scripts/filter_references.py
