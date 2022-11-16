""" How to run: change into dir: marketplace/example
    Run using `snakemake`.
    For different running options, e.g., dryrun, specifying number of cores, etc., read documentation here:
    https://snakemake.readthedocs.io/en/v5.1.4/executable.html

    Sweeping through friction params

"""

import infosys.utils as utils


ABS_PATH = ''
DATA_PATH = os.path.join(ABS_PATH, 'data')
CONFIG_PATH = os.path.join(ABS_PATH, "config_friction_Nov8_3")
mode='igraph'
sim_num = 6

config_fname = os.path.join(CONFIG_PATH, 'all_configs.json')
exp_type = "vary_friction_and_learning"
# get network names corresponding to the strategy
EXPS = json.load(open(config_fname,'r'))[exp_type]

EXP_NAMES = list(EXPS.keys())#[-2:]
RUN_PATH = f'07112022_friction_{exp_type}_{sim_num}_runs'
RES_PATH = os.path.join(ABS_PATH,'results',RUN_PATH)
TRACKING_PATH = os.path.join(ABS_PATH, 'verbose',RUN_PATH)


rule all:
    input:
        expand(os.path.join(RES_PATH, '{exp_name}.json'), exp_name=EXP_NAMES)

rule run_simulation:
    input:
        network = os.path.join(DATA_PATH, "infosys_network.gml"),
        configfile = os.path.join(CONFIG_PATH, exp_type, "{exp_name}.json")
    output:
        measurements = os.path.join(RES_PATH, '{exp_name}.json'),
        tracking = os.path.join(TRACKING_PATH, '{exp_name}.json.gz')
    shell: """
        python3 -m workflow.scripts.driver -i {input.network} -o {output.measurements} -v {output.tracking} --config {input.configfile} --times {sim_num} --mode {mode}
    """

rule init_net:
    input:
        #follower = os.path.join(DATA_PATH, 'follower_network.gml'),
        follower = os.path.join(DATA_PATH, 'Amended_BA_Friction_m=3_n=1000_coeff=.29.gml'),
        configfile = os.path.join(DATA_PATH, 'config.json')

    output: os.path.join(DATA_PATH, "infosys_network.gml")

    shell: """
            python3 -m workflow.scripts.init_net -i {input.follower} -o {output} --config {input.configfile} --mode {mode}
        """
