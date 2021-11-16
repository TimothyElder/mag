#!/bin/sh

#SBATCH --partition=caslake
#SBATCH --tasks=1

# Load the default version of hello.
source activate soc_of_soc
module load R

# Use R CMD BATCH to run Rhello.R.
R CMD BATCH --no-save --no-restore /home/timothyelder/mag/scripts/analysis/journal_net.R
