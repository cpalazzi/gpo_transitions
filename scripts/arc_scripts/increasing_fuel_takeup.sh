#! /bin/bash
#SBATCH --chdir='/data/engs-df-green-ammonia/engs2523/global-port-optimisation'
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --partition=medium
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=carlo.palazzi@eng.ox.ac.uk

# After SBATCH section of script

module load Anaconda3/2022.05
module load Gurobi/9.5.2-GCCcore-11.3.0
which python
source activate $DATA/geo-env
which python

# Your Python commands here...
python main.py

