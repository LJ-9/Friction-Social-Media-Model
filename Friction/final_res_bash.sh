#!/bin/bash
#####  Constructed by HPC everywhere #####
#SBATCH --mail-user=
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --time=3-23:59:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --job-name=finalrun

######  Module commands #####
source /N/u/*user*/Quartz/miniconda3/etc/profile.d/conda.sh 
conda activate snakemake

######  Job commands go below this line #####
cd /N/u/*user*/Quartz/marketplace/Friction
echo '###### RUNDec28 ######'
snakemake --nolock --cores 40