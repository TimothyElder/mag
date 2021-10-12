#!/bin/sh

#SBATCH --job-name=filter-mag
#SBATCH --account=pi-jevans
#SBATCH --partition=caslake
#SBATCH --ntasks-per-node=1  # number of tasks
#SBATCH --cpus-per-task=20    # number of threads per task
#SBATCH --output=/home/timothyelder/Documents/scripts/logs/return_cited.out
#SBATCH --mail-user=timothyelder@uchicago.edu

# LOAD MODULES
module load python

# LOAD CONDA ENVIRONMENT
source activate soc_of_soc

# DO COMPUTE WORK
python /home/timothyelder/mag/scripts/filter_mag_corpus.py
