#!/bin/sh

# -w bm1-lxslurm23 \

cd "$HOME"
sbatch --job-name=jupyter \
       --output=/home/srubtsovenko/logs/jupyter/jupyter_%j.log \
       --partition=cpu \
       --cpus-per-task=6 \
       --mem=100gb \
       $HOME/scripts/jupyter_job.sh

