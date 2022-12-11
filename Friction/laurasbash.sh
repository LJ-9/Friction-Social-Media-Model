#!/bin/bash
#####  Constructed by HPC everywhere #####
#SBATCH --mail-user=jahnla@iu.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3-23:59:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --job-name=1

######  Module commands #####
source /N/u/jahnla/Quartz/miniconda3/etc/profile.d/conda.sh 
conda activate base
pip install -e.

######  Job commands go below this line #####
cd /N/u/jahnla/Quartz/marketplace/Friction
echo '###### test1 ######'
snakemake --nolock --cores 1