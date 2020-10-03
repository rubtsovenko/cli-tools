import subprocess
from argparse import ArgumentParser



def build_args(parser: ArgumentParser):
    """Constructs the command-line arguments"""
    parser.add_argument(
        '-p', '--partition',
        default='gpu_v100',
        choices=['cpu', 'gpu_p100', 'gpu_v100', 'gpu_v100_big', 'gpu_rtx2080'],
        help="Partition of the cluster"
    )
    parser.add_argument(
        '--ngpu',
        type=int,
        default=1,
        help='Number of gpus'
    )
    parser.add_argument(
        '--ncpu',
        type=int,
        default=4,
        help='Number of cpu'
    )
    parser.add_argument(
        '-m', '--memory',
        type=int,
        default=40,
        help='Number of RAM GBs'
    )

    return parser

def parse_args():
    """Parses the command line arguments and returns arguments"""
    parser = ArgumentParser(description='BQ clicks extraction')
    build_args(parser)
    args, unknown_args = parser.parse_known_args()

    return args, unknown_args

def main(args, unknown_args):
    if args.partition == 'cpu':
        command = f"""
        cd ~/ &&
        sbatch \
            --job-name=jupyter \
            --output=/home/srubtsovenko/logs/jupyter/jupyter_%j.log \
            --partition={args.partition} \
            --cpus-per-task=6 \
            --mem=100gb \
            ~/scripts/jupyter_job.sh
        """
    else:
        command = f"""
        cd ~/ &&
        sbatch \
            --job-name=jupyter \
            --output=/home/srubtsovenko/logs/jupyter/jupyter_%j.log \
            --partition={args.partition} \
            --cpus-per-task={args.ncpu} \
            --gres=gpu:{args.ngpu} \
            --mem={args.memory}gb \
            ~/scripts/jupyter_job.sh
        """

    output = subprocess.check_output(command, shell=True).decode()
    print(output)


if __name__ == "__main__":
    args, unknown_args = parse_args()
    main(args, unknown_args)

