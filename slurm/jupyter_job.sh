#!/bin/sh
echo "################ Parameters ################"
ipnip=$(hostname -I | cut -d ' ' -f1)
echo "Hostname: $(hostname)"
echo "IP: $ipnip"
echo "Job ID: $SLURM_JOB_ID"
echo "Job name: $SLURM_JOB_NAME"
echo "Number of allocated CPUs: $SLURM_CPUS_ON_NODE"
echo "Allocated memory: $((SLURM_MEM_PER_NODE / 1024)) gb"
echo "############################################"
echo ""

echo "################ Job ################"
jupyter notebook --no-browser --port=8888 --ip=$ipnip
