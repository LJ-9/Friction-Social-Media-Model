""" How to run: change into dir: marketplace/example
    Run using `snakemake`.
    For different running options, e.g., dryrun, specifying number of cores, etc., read documentation here:
    https://snakemake.readthedocs.io/en/v5.1.4/executable.html

    Sweeping through friction params

"""

import infosys.utils as utils


ABS_PATH = ''
DATA_PATH = os.path.join(ABS_PATH, 'data')
#TODO
CONFIG_PATH = os.path.join(ABS_PATH, "config_friction_Dec08_random_nw2")
mode='igraph'
sim_num = 1

config_fname = os.path.join(CONFIG_PATH, 'all_configs.json')
#TODO
exp_type = "vary_friction_and_learning_and_network"
EXPS = json.load(open(config_fname,'r'))[exp_type]
EXP_NAMES = list(EXPS.keys())#[-2:]
# get network names from config file
EXPSdict = json.load(open(config_fname,'r'))[exp_type] # full dict to get network names
# initializing key
nw = "human_network"
# using keys() and values() to extract values
NETWORK_NAMES = [sub[nw] for sub in EXPSdict.values() if nw in sub.keys()]



#TODO
RUN_PATH = f'08122022_friction_{exp_type}_{sim_num}_runs'
RES_PATH = os.path.join(ABS_PATH,'results',RUN_PATH)
TRACKING_PATH = os.path.join(ABS_PATH, 'verbose',RUN_PATH)


rule all:
    input:
        expand(os.path.join(RES_PATH, '{exp_name}.json'), exp_name=EXP_NAMES)
        

rule run_simulation:
    input:
        network = expand(os.path.join(DATA_PATH, "infosys_network_{network_name}.gml"), network_name = NETWORK_NAMES),
        configfile = os.path.join(CONFIG_PATH, exp_type, "{exp_name}.json")
    output:
        measurements = os.path.join(RES_PATH, '{exp_name}.json'),
        tracking = os.path.join(TRACKING_PATH, '{exp_name}.json.gz')
    shell: """
        python3 -m workflow.scripts.driver -i {input.network} -o {output.measurements} -v {output.tracking} --config {input.configfile} --times {sim_num} --mode {mode}
    """

rule init_net:
    input:
        #TODO
        follower = expand(os.path.join(DATA_PATH, {network_name}), network_name = NETWORK_NAMES),
        configfile = os.path.join(DATA_PATH, 'config.json') # to get values for beta and gamma to build network

    output: os.path.join(DATA_PATH, "infosys_network_{network_name}.gml")

    shell: """
            python3 -m workflow.scripts.init_net -i {input.follower} -o {output} --config {input.configfile} --mode {mode}
        """

