#!/bin/bash 
#SBATCH --partition=serial

#SBATCH --qos=84c-1d_serial
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1 
#SBATCH --mem=128G

#SBATCH --mail-type=ALL

#SBATCH --job-name=abm_covid19_simulations-24
#SBATCH --output=abm_covid19_simulations-24.out
#SBATCH --error=abm_covid19_simulations-24.err

#SBATCH --mail-user=jminoza@up.edu.ph 
#SBATCH --mail-type=ALL 
#SBATCH --requeue

echo "SLURM_JOBID="$SLURM_JOBID 
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST 
echo "SLURM_NNODES"=$SLURM_NNODES 
echo "SLURMTMPDIR="$SLURMTMPDIR 
echo "working directory = "$SLURM_SUBMIT_DIR 

ulimit -s unlimited

module load anaconda/3-5.3.1
module load python/3.8.2
module load openmpi/4.0.3_gcc-8.4.0
module load cuda/9.0_cudnn-7.0.5
module load mpich/3.3.2
module load netcdf/4.7.3
module load libpng/1.6.37
module load openmpi/4.0.2
module load gcc/8.4.0
module load scilab/6.1.0
module load curl/7.69.1
module load hdf5/1.12.0
module load netcdf-fortran/4.5.2
module load make/4.3

cd ~/scratch2/Bangsamoro-ABM-COVID19-Vaccine-Distribution-Optimization/

pip install -r requirements.txt --user

srun jupyter nbconvert --to notebook --execute --inplace "experiments/notebooks/Sensitivity Analysis on Vaccination with All Prioritizations - 100% Vaccine Hesitants.ipynb" --ExecutePreprocessor.timeout=86400
