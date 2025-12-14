import subprocess
import sys

ENV_NAME = "uni-distrib"


def run_command(command):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)


def main():
    # Check if conda is installed
    try:
        subprocess.check_call(["conda", "--version"], shell=True)
    except subprocess.CalledProcessError:
        print("Conda is not installed or not in PATH.")
        sys.exit(1)

    print(f"Creating conda environment '{ENV_NAME}'...")
    # Create environment with Python 3.12
    # Using -y to automatically say yes to prompts
    run_command(f"conda create -n {ENV_NAME} python=3.12 -y")

    print(f"Installing mpi4py in '{ENV_NAME}'...")
    # Install mpi4py using conda to ensure binary compatibility with mpiexec
    run_command(f"conda install -n {ENV_NAME} mpi4py -y")

    print("\nSetup complete!")
    print(f"To activate the environment, run:\n    conda activate {ENV_NAME}")
    print("Then you can run your MPI scripts like this:")
    print("    mpiexec -n 2 python pw3/file_transfer.py")


if __name__ == "__main__":
    main()
