#!/bin/sh

#SBATCH --job-name=network-projection
#SBATCH --account=pi-jevans
#SBATCH --partition=caslake
#SBATCH --ntasks-per-node=1  # number of tasks
#SBATCH --cpus-per-task=20    # number of threads per task
#SBATCH --output=network_projection.out

source activate soc_of_soc

module load R

# DO COMPUTE WORK
R CMD BATCH --no-save --no-restore net_pro.R
