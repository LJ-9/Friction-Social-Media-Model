""" Config for the first set of exps (vary mu_friction and learning_friction, keep all else constant)"""
import os
print(os.getcwd())
import infosys.utils as utils
import infosys.final_configs as configs
import numpy as np
import os
import json

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
    "human_network": "Amended_BA_Friction_m=3_n=1000_coeff=.29.gml"
}

def make_exps(saving_dir, default_infosys_config):
    all_exps = {}

    #vary beta & gamma, keep constant targeting strategy
    all_exps["vary_friction_and_learning"] = {}

    def make_single_config(mu_friction, learning_friction):
        cf = {'mu_friction':mu_friction, 'learning_friction':learning_friction, 'targeting_criterion': configs.DEFAULT_STRATEGY}
        config = utils.update_dict(cf, infosys_default_friction)

        config_name = f'mu_fr_{mu_friction}-learn_fr_{learning_friction}'
        all_exps["vary_friction_and_learning"][config_name] = config

        if utils.make_sure_dir_exists(saving_dir, 'vary_friction_and_learning'):
            fp = os.path.join(saving_dir, 'vary_friction_and_learning', f'{config_name}.json')
            json.dump(config,open(fp,'w'))


    MU_FRICTION = sorted(list([0.01,0.05,0.1])+list(np.arange(.2, 1.1, .1)))#(.005, .505, .005)#(.005, .505, .005)
#(.005, .505, .005)#(.005, .505, .005)
 #sorted(list(np.arange(.01, .105, .01))+list(np.arange(.2, .6, .1)))#(.005, .505, .005)#(.005, .505, .005)
    LEARNING_FRICTION =  sorted(list([0,0.01,0.05,0.1])+list(np.arange(.2, 1.1, .1)))#(0, .505, .005)#(0, .505, .005)#sorted(list(np.arange(.0, .105, .01))+list(np.arange(.2, .6, .1)))#(0, .505, .005)

    make_single_config(0.0, 0.0)

    for idx,mu_friction in enumerate(MU_FRICTION):
        for jdx,learning_friction in enumerate(LEARNING_FRICTION):
            make_single_config(mu_friction, learning_friction)


    fp = os.path.join(saving_dir, 'all_configs.json')
    json.dump(all_exps,open(fp,'w'))
    print(f'Finish saving config to {fp}')


if __name__=='__main__':

    ABS_PATH = '/Users/laurajahn/Documents/Git/Marketplace-of-ideas'

    saving_dir = os.path.join(ABS_PATH, "example/config_friction_Nov8_3")
    make_exps(saving_dir, configs.infosys_default)
