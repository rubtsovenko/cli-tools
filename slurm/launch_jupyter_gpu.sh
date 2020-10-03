#!/bin/sh

cd "$HOME"
sbatch --job-name=jupyter \
       --output=/home/srubtsovenko/logs/jupyter/jupyter_%j.log \
       --partition=gpu_v100 \
       --gres=gpu:1 \
       --cpus-per-task=4 \
       --mem=40gb \
       $HOME/scripts/jupyter_job.sh

