#!/bin/bash
#
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=moco_tac
#SBATCH --partition=trc
#SBATCH --time=96:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=/home/users/currier/job_outputs/%x.%j.out
#SBATCH --open-mode=append

module use /home/groups/trc/modules
module load antspy/0.2.2

python3 /home/users/asmart/projects/timmoco/motion_correction.py /oak/stanford/groups/trc/data/Ashley2/imports/20210709

#python3 /home/users/asmart/projects/timmoco/motion_correction.py /oak/stanford/groups/trc/data/Tim/ImagingData/processed/20210824/TSeries-20210824-002
