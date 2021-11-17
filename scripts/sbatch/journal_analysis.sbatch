#!/bin/sh

#SBATCH --account=pi-jevans
#SBATCH --partition=bigmem
#SBATCH --tasks=1
#SBATCH --mem=300G
#SBATCH --output=/home/timothyelder/mag/scripts/logs/journal_analysis.out

# Load virtual environment and R
source activate soc_of_soc
module load R/4.0.3

# Use R CMD BATCH to run Rscript.
R CMD BATCH --no-save --no-restore /home/timothyelder/mag/scripts/analysis/journal_net.R
