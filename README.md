# Friction Interventions to Curb the Spread of Misinformation on Social Media

This repository contains code to reproduce the results in the paper *Friction Interventions to Curb the Spread of Misinformation on Social Media* by Laura Jahn, Rasmus K. Rendsvig, Alessandro Flammini, and Filippo Menczer and Vincent Hendricks.

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


Activate virtualenv and run `pip install -e .` for the module imports to work correctly.

A snakemake file [`Snakefile`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/Snakefile) controls the workflow and is called in  [`final_res_bash.sh`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/final_res_bash.sh) to start the simulation. Outputs are saved to `Friction/results` and `Friction/verbose`.

## Data Analysis

Data is analysed in [`Analysis_results.ipynb`](https://github.com/LJ-9/Friction-Social-Media-Model/blob/master/Friction/Analysis_results.ipynb).

## Environment

Our code is based on **Python3.6+**.

## Notes

The results in the paper are based on averages across multiple simulation runs. To reproduce those results, we suggest running the simulations in parallel, for example on a cluster.


Run minimal example with `workflow/example/run_simulation.py`

How to multiple experiments:
- run `workflow/scripts/make_finalconfig.py` (this creates config files for different sets of param combination you want to test)
- run `workflow/final_rules/<exp_type>.smk` (exp_type: [strategies_beta, vary_thetabeta, etc.])




## License
This project is licensed under the terms of the GNU General Public License v3.0 (gpl-3.0). See [LICENSE](https://github.com/humanplayer2/get-twitter-likers-data/blob/main/LICENSE.md) for rights and limitations.

## Contact
The corresponding author can be contacted at laurajahn [at] outlook [dot] de.

