#!/bin/sh

#SBATCH --job-name=net
#SBATCH --account=pi-jevans
#SBATCH --partition=bigmem
#SBATCH --tasks=1
#SBATCH --mem=500G
#SBATCH --output=/home/timothyelder/mag/scripts/logs/net.out

# Load the default version of hello.
module load R

# Use R CMD BATCH to run Rhello.R.
R CMD BATCH --no-save --no-restore net.R