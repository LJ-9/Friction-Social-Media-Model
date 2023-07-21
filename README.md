# Friction Interventions to Curb the Spread of Misinformation on Social Media

This repository contains code to reproduce the results in the paper *Friction Interventions to Curb the Spread of Misinformation on Social Media* by [Laura Jahn](https://www.linkedin.com/in/laura-jahn/), [Rasmus K. Rendsvig](https://rends.dk), [Alessandro Flammini](https://cnets.indiana.edu/aflammin/), [Filippo Menczer](https://cnets.indiana.edu/fil/) and [Vincent Hendricks](https://comm.ku.dk/staff/?pure=en/persons/30701). 

```
  @article{Jahn23Friction,  
    author = {{Jahn, Laura and Rendsvig, Rasmus~K., and Flammini, Alessandro, and Menczer, Filippo, and Hendricks, Vincent}},
    title = {{Friction Interventions to Curb the Spread of Misinformation on Social Media}},  
    year = {2023},   
  }
 ```

This work is based on the minimal social media simulation model [SimSom: A Simulator for Social Media](https://github.com/osome-iu/SimSoM) and based on the paper *Vulnerabilities of the Online Public Square to Manipulation* by Bao Tran Truong, Xiaodan Lou, Alessandro Flammini, and Filippo Menczer.


## Structure of the Repository

To reproduce the results of the paper on friction, scripts for data generation (networks), running the simulation, and data analysis can be found in [`Friction/`](https://github.com/LJ-9/Friction-Social-Media-Model/tree/master/Friction)


## Data
Networks are created before the simulation runs. The script to create networks [`Generate_networks.py`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/data/Generate_networks.py) is called through the script `bash-nw`.  

Configs (parameter combinations) are generated with [`make_final_config_friction.py`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/make_final_config_friction.py).



## Running the simulation

### Environment

Our code is based on **Python3.6+**.
Activate virtualenv with the required packages and run `pip install -e .` for the module imports to work correctly.
We use `conda`, a package manager to manage the environments. Please make sure you have [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) or [mamba](https://mamba.readthedocs.io/en/latest/installation.html#) installed on your machine.

A snakemake file [`Snakefile`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/Snakefile) controls the workflow and is called in  [`final_res_bash.sh`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/final_res_bash.sh) to start the simulation. Outputs are saved to `Friction/results` and `Friction/verbose`.

Installation times for packages and package managers are standard and shouldn't be a problem to a normal computer, and available to all standard operating systems. Runtime varies depending on parameters, and is faster when the simulation is deployed on multiple cores (as specified in bash and snakefiles).

## Data Analysis

Data is analysed in [`Analysis_results.ipynb`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/Analysis_results.ipynb). 


## Notes

The results in the paper are based on averages across multiple simulation runs. To reproduce those results, we suggest running the simulations in parallel, for example on a cluster. This decreases runtime significantly. Runtime increases with network size, number of runs, and convergence/stability parameters as described in the paper.


Run minimal example with `workflow/example/run_simulation.py` with the specified test follower network. 



## License
This project is licensed under the terms of the GNU General Public License v3.0 (gpl-3.0). See [LICENSE](https://github.com/humanplayer2/get-twitter-likers-data/blob/main/LICENSE.md) for rights and limitations.

## Contact
The corresponding author can be contacted at laurajahn [at] outlook [dot] de.

