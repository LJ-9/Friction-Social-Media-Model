
ABS_PATH = '/N/slate/baotruon/marketplace'
DATA_PATH = '/N/slate/baotruon/marketplace/data'

print(os.getcwd())
exp_configs = json.load(open(os.path.join(DATA_PATH, 'all_configs.json'),'r'))
EXPS = list(exp_configs['vary_thetaphi'].keys())

GAMMA = [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.02, 0.05, 0.1, 0.2, 0.5]
TARGETING = [None, 'hubs', 'partisanship', 'conservative', 'liberal', 'misinformation']

#get network corresponding with the exp
exp_network = {}

gamma = 0.02 # gamma in the range where targeting has some effect
for exp in EXPS:
    if 'none' in exp:
        networkname = '%s%s' %(TARGETING.index(None), GAMMA.index(gamma))
    else: 
        networkname = '%s%s' %(TARGETING.index(exp.split('_')[0]), GAMMA.index(gamma) )
    exp_network[exp] = networkname


sim_num = 1
mode='igraph'
RES_DIR = os.path.join(ABS_PATH,'results', 'vary_thetaphi_%sruns' %sim_num)

rule all:
    input: expand(os.path.join(RES_DIR, '{exp_no}.json'), exp_no=EXPS)

rule run_simulation:
    input: 
        network = os.path.join(DATA_PATH, mode, 'vary_targetgamma', "network_{exp_network[exp_no]}.gml"),
        configfile = os.path.join(DATA_PATH, "vary_thetaphi", "{exp_no}.json")
    output: os.path.join(RES_DIR, '{exp_no}.json')
    shell: """
        python3 -m workflow.driver -i {input.network} -o {output} --config {input.configfile} --mode {mode} --times {sim_num}
    """

rule init_net:
    input: 
        follower=os.path.join(DATA_PATH, 'follower_network.gml'),
        configfile = os.path.join(DATA_PATH, 'vary_targetgamma', "network_{exp_network[exp_no]}.gml")
        
    output: os.path.join(DATA_PATH, mode, 'vary_targetgamma', "network_{exp_network[exp_no]}.gml")

    shell: """
            python3 -m workflow.init_net -i {input.follower} -o {output} --config {input.configfile} --mode {mode}
        """ 