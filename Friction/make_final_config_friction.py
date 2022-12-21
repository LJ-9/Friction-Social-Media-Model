""" Config for the first set of exps (vary mu_friction and learning_friction, keep all else constant)"""
import os
print(os.getcwd())
import infosys.utils as utils
import infosys.final_configs as configs
import numpy as np
import os
import json
import glob

infosys_default_friction = {
    "beta": 0,
    "gamma": 0,
    "targeting_criterion": None,
    "trackmeme": True,
    "verbose": False,
    "epsilon": 0.0001,
    "mu": 0.5,
    "phi": 1,
    "alpha": 15,
    "theta": 1,
    "mu_friction": 0.05,
    "pass_friction": 0,
    "learning_friction": 0.05,
    "human_network": "Amended_BA_Friction_m=3_n=1000_coeff=.29.gml",
    "truncation_interval": 0,
    "check_conv": True
}
# Nov 18: added variable: "check-conv" = True # if True, then the simulation continues for another 50 steps after the convergence criterion is reached
# Nov 18: parameter: truncation_interval, how much sampling of quality and fitness will be correlated
def make_exps(saving_dir, default_infosys_config):
    all_exps = {}

    #vary beta & gamma, keep constant targeting strategy
    all_exps["vary_friction_and_learning_and_network"] = {}

    def make_single_config(mu_friction, learning_friction, human_network):
        cf = {'mu_friction':mu_friction, 'learning_friction':learning_friction, 'human_network': human_network, 'targeting_criterion': configs.DEFAULT_STRATEGY}
        config = utils.update_dict(cf, infosys_default_friction)

        config_name = f'mu_fr_{mu_friction}-learn_fr_{learning_friction}'
        all_exps["vary_friction_and_learning_and_network"][config_name] = config

        if utils.make_sure_dir_exists(saving_dir, 'vary_friction_and_learning_and_network'):
            fp = os.path.join(saving_dir, 'vary_friction_and_learning_and_network', f'{config_name}.json')
            json.dump(config,open(fp,'w'))


    MU_FRICTION = sorted(list([0.01,0.05,0.1])+list(np.arange(.2, 1.1, .1)))#sorted(list([0.01,0.05,0.1])+list(np.arange(.2, 1.1, .1)))
    LEARNING_FRICTION =  sorted(list([0,0.01,0.05,0.1])+list(np.arange(.2, 1.1, .1)))
    # Make lists of networks to use: new network for each parameter combination (future task: for each sim rep new network? Now sim rep of parameter combi will be run on same network)
    # folder path
    NETWORKPATH = os.path.join(ABS_PATH, 'Friction/data')
    # list to store network names
    NETWORKS = []
    # Iterate directory
    for path in os.listdir(NETWORKPATH):
        # check if current path is a file
        if os.path.isfile(os.path.join(NETWORKPATH, path)):
            NETWORKS.append(path)
    list.sort(NETWORKS)

    make_single_config(0.0, 0.0, NETWORKS[0])

    # pair each parameter combination with a random pre-generated network 
    i = 1
    for idx,mu_friction in enumerate(MU_FRICTION):
        for jdx, learning_friction in enumerate(LEARNING_FRICTION):
            make_single_config(mu_friction, learning_friction, NETWORKS[i])
            i+=1

    fp = os.path.join(saving_dir, 'all_configs.json')
    json.dump(all_exps,open(fp,'w'))
    print(f'Finish saving config to {fp}')

if __name__=='__main__':

    ABS_PATH = '/Users/laurajahn/Documents/Git/Marketplace-of-ideas'

    saving_dir = os.path.join(ABS_PATH, "Friction/config_friction_Dec13_random_rho99_eps0.0001")
    make_exps(saving_dir, configs.infosys_default)