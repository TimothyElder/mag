#!/bin/sh

#SBATCH --job-name=split_authors
#SBATCH --account=pi-jevans
#SBATCH --partition=caslake
#SBATCH --ntasks-per-node=1                   # number of tasks
#SBATCH --cpus-per-task=40                    # number of threads per task
#SBATCH --output=/home/timothyelder/mag/scripts/logs/split_authors.out

# LOAD MODULES
module load python

# LOAD CONDA ENVIRONMENT
source activate soc_of_soc

# DO COMPUTE WORK
python /home/timothyelder/mag/scripts/split_authors_csv.py