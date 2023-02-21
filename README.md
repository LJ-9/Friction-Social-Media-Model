# Friction Interventions to Curb the Spread of Misinformation on Social Media

This repository contains code to reproduce the results in the paper *Friction Interventions to Curb the Spread of Misinformation on Social Media* by Laura Jahn, Rasmus K. Rendsvig, Alessandro Flammini, and Filippo Menczer.

```
  @article{Jahn23Friction,  
    author = {{Jahn, Laura and Rendsvig, Rasmus~K., and Flammini, Alessandro, and Menczer, Filippo}},
    title = {{Detecting Coordinated Inauthentic Behavior in Likes on Social Media: Proof of Concept}},  
    year = {2023},   
  }
 ```

This work is based on the minimal social media simulation model [SimSom: A Simulator for Social Media](https://github.com/osome-iu/SimSoM) and based on the paper *Vulnerabilities of the Online Public Square to Manipulation* by Bao Tran Truong, Xiaodan Lou, Alessandro Flammini, and Filippo Menczer.


## Data
Networks created for the simulation: TODO
[Script to create network](workflow/make_network.py)

## Environment

Our code is based on **Python3.6+**.

## Notes

The results in the paper are based on averages across multiple simulation runs. To reproduce those results, we suggest running the simulations in parallel, for example on a cluster.

## Notes on revised code:
Activate virtualenv and run `pip install -e .` for the module imports to work correctly.

Run minimal example with `workflow/example/run_simulation.py`

How to multiple experiments: TODO
- run `workflow/scripts/make_finalconfig.py` (this creates config files for different sets of param combination you want to test)
- run `workflow/final_rules/<exp_type>.smk` (exp_type: [strategies_beta, vary_thetabeta, etc.])




# License
This project is licensed under the terms of the GNU General Public License v3.0 (gpl-3.0). See [LICENSE](https://github.com/humanplayer2/get-twitter-likers-data/blob/main/LICENSE.md) for rights and limitations.
