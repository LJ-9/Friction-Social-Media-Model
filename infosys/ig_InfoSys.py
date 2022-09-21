
"""
Code to (re)produce results in the paper
"Manipulating the Online Marketplace of Ideas" (Lou et al.)
https://arxiv.org/abs/1907.06130

Requirements: python>=3.6
link direction is following (follower -> friend), opposite of info spread!

Input: igraph .graphml file
Implementation using igraph library
"""

from infosys.User import User
from infosys.Meme import Meme
from infosys.profileit import profile
import infosys.utils as utils
import infosys.ig_utils as ig_utils
import igraph as ig

import networkx as nx
import random
import numpy as np
from collections import Counter, defaultdict


class InfoSystem:
    #TODO: change default track_forgotten to False
    ## Epsilon value was tested and fixed. To ensure convergence, epsilon <= 0.0001
    ## Rho >= 0.5
    def __init__(self, graph_gml,
                track_forgotten=True,
                trackmeme=True, # Cannot be False if we calculate diversity and tau
                tracktimestep=True,
                verbose=False,
                epsilon=0.0001, # Don't change this value
                rho=0.8, # Don't change this value, check note above
                mu=0.5,
                phi=1,
                alpha=15,
                theta=1,
                mu_friction = 0.1, # Likelihood that friction is triggered when about to repost/retweet,
                                   # (1-mu-mu_friction) = likelihood that no friction is triggered, just normally repost
                pass_friction = 0.5, # Agent "passes" friction quiz, on to repost/retweet after exposore to friction
                learning_friction = 0.01): # Learning after exposure to friction (no matter whether pass or no pass).
                                           # learning_friction determined the probabiliy that agents "learn to see quality"
                                           # when choosing which meme to repost

        self.network = None #TODO: can remove this
        self.verbose = verbose
        self.track_forgotten = track_forgotten
        if self.track_forgotten is True: #aggregate in and outflux caused by all agents
            print('Tracking forgotten memes')
        self.trackmeme = trackmeme
        self.tracktimestep = tracktimestep
        self.quality_timestep=[]
        self.meme_all_changes = defaultdict(lambda:[])
        # track the influx and outflux of memes globally. #TODO: Might not need this later
        # All changes happening in simulation: max num_memes= alpha * num_agents * num_followers (avg)
        # structure: {"bot_in":[], "bot_out": [], "human_in":[], "human_out":[]} - items in list correspond to each timestep

        self.meme_popularity = None

        self.epsilon=epsilon
        self.rho=rho
        self.mu=mu
        self.phi=phi
        self.alpha=alpha
        self.theta=theta
        self.mu_friction=mu_friction
        self.pass_friction=pass_friction
        self.learning_friction=learning_friction

        #Keep track of number of memes globally
        self.meme_dict = [] # list of dicts, contains of {"meme_id": meme.__dict__ and popularity information updated from self.meme_popularity}
        self.all_memes = [] # list of Meme objects
        self.num_memes=0 # for verbose debug
        self.num_meme_unique=0 # for verbose debug
        self.memes_human_feed = 0 # for verbose debug
        self.quality_diff = 1
        self.quality = 1
        self.time_step=0
        self.agent_friction_exposure={}

        if trackmeme is True:
            self.meme_popularity = {}
            # dict of popularity (all memes), structure: {"meme_id": {"is_by_bot": meme.is_by_bot, "human_shares":0, "bot_shares":0, "spread_via_agents":[]}}

        try:
            self.network = ig.Graph.Read_GML(graph_gml)
            print(self.network.summary())

            self.n_agents = self.network.vcount()
            #debug
            # self.agent_feeds = {}
            # agents = [agent for agent in self.network.vs]
            # for agent in agents:
            #     self.agent_feeds[agent['uid']]=[]
            # #
            self.agent_feeds = {agent['uid']:[] for agent in self.network.vs} #init an empty feed for all agents

            self.meme_net_change_timestep = {"bot_in":[], "bot_out": [], "human_in":[], "human_out":[]}
            # track the influx and outflux of memes globally.
            # All changes happening in simulation: max num_memes= alpha * num_agents
            # structure: {"bot_in":[], "bot_out": [], "human_in":[], "human_out":[]} - items in list correspond to each timestep

            if verbose:
                in_deg = [self.network.degree(n, mode='in') for n in self.network.vs]#number of followers
                print('Graph Avg in deg', round(sum(in_deg)/len(in_deg),2))

        except Exception as e:
            print(e)
            print(f'Graph file: {graph_gml}')

    # @profile
    def simulation(self):
        while self.quality_diff > self.epsilon:
            if self.verbose:
                # print('time_step = {}, q = {}, diff = {}'.format(self.time_step, self.quality, self.quality_diff), flush=True)
                print('time_step = {}, q = {}, diff = {}, unique/human memes = {}/{}, all memes created={}'.format(self.time_step, self.quality, self.quality_diff, self.num_meme_unique, self.memes_human_feed, self.num_memes), flush=True)

            self.time_step += 1
            if self.tracktimestep is True:
                self.quality_timestep+= [self.quality]

            self.meme_all_changes_timestep = defaultdict(lambda: 0)
            # structure: {"bot_in":0, "bot_out": 0, "human_in":0, "human_out":0}

            self.meme_replacement = {agent['uid']: {"bot_in":0, "bot_out": 0, "human_in":0, "human_out":0} for agent in self.network.vs if agent['bot']==0}

            for _ in range(self.n_agents):
                # simulation
                self.num_memes = sum([len(f) for f in self.agent_feeds.values() if len(f)>0])
                influx_by_agent_all = self.ig_simulation_step() # meme in outflux per agent {"bot_in":0, "bot_out": 0, "human_in":0, "human_out":0}
                # ^ self.meme_replacement is modified at this step
                #print(influx_by_agent_all)

                if self.track_forgotten is True:
                    # add meme flow done by this agent (on all their followers) to the total changes by all agents in this cycle
                    for key in influx_by_agent_all.keys():
                        self.meme_all_changes_timestep[key] += influx_by_agent_all[key]
            # book keeping
            for key in dict(self.meme_all_changes_timestep).keys():
                # add total meme changes by all agents to the timeline
                self.meme_all_changes[key] +=[ self.meme_all_changes_timestep[key] ]

            for flow_type in self.meme_net_change_timestep.keys():
                # update meme net change at the end of cycle to the timeline
                total_flow = sum([self.meme_replacement[agent][flow_type] for agent in self.meme_replacement.keys()])
                self.meme_net_change_timestep[flow_type] += [total_flow]

            self.update_quality()

        all_feeds = self.agent_feeds # dict of {agent['uid']:[Meme()] } each value is a list of Meme obj in the agent's feed

        # b: Save feed info of agent & meme popularity
        # convert self.agent_feed into dict of agent_uid - [meme_id]
        feeds = {}
        for agent, memelist in all_feeds.items():
            feeds[agent] = [meme.id  for meme in memelist]

        # return feeds, self.meme_popularity, self.quality

        #b: return all values in a dict & meme popularity
        # save meme_popularity
        self.meme_dict = self._return_all_meme_info() #need to call this before calculating tau and diversity!!

        measurements = {
            'quality': self.quality,
            'diversity' : self.measure_diversity(),
            'discriminative_pow': self.measure_kendall_tau(),
            'quality_timestep': self.quality_timestep,
            'all_memes': self.meme_dict,
            'all_feeds': feeds,
            'meme_influx': self.meme_all_changes,
            'meme_netchange': self.meme_net_change_timestep
        }

        return measurements

    # @profile
    def ig_simulation_step(self):
        # returns dict: influx_by_agent_all: the number of memes changed in this cycle by all human agents

        agent = random.choice(self.network.vs)
        agent_id = agent['uid']
        feed = self.agent_feeds[agent_id]
        print("selected agent")

        if len(feed)>0 and random.random() > self.mu:
            # pick and share a meme unless friction prevents you to do so:
            # if agent has had exposure to friction, pick qual meme (with low probability)
            if self.agent_friction_exposure.get(agent_id, 0) > 0 and random.random() < self.learning_friction: # TODO: Do we want exposed agents also to improve passing the quiz? Meachnism to up the number of memes out there agein?
                if sum([m.quality for m in feed]) > 0:
                    meme = random.choices(feed, weights=[m.quality for m in feed], k=1)[0]# agent has learned to make choice based on quality (some of the time: learning_friction)
                else:
                    # TODO: Do nothing if no qual memes around? Threshold? Pick at random? Choose according to fitness?
                    #meme = random.choices(feed, weights=[m.fitness for m in feed], k=1)[0]
                    meme = None

            else:
                meme = random.choices(feed, weights=[m.fitness for m in feed], k=1)[0] #random choices return a list

            if random.random() < self.mu_friction: # friction is triggered
                # TODO: log exposure to friction
                print("friction triggered")
                if agent_id in self.agent_friction_exposure:
                    self.agent_friction_exposure[agent_id]+=1
                else:
                    self.agent_friction_exposure[agent_id]=1

                if random.random() < self.pass_friction: # if frictiion is passed, share post
                    pass
                    print("meme was shared despite friction")
                else:
                    meme = None # if friction is not passed, don't do anything, friction prevented sharing
                    print("friction prevented sharing")
        else:
            # new meme
            self.num_meme_unique+=1
            meme = Meme(self.num_meme_unique, is_by_bot=agent['bot'], phi=self.phi)

            self.all_memes += [meme]
            print("create new meme")
        # book keeping
        # TODO: add forgotten memes per degree
        influx_by_agent_all = {"bot_in":0, "bot_out": 0, "human_in":0, "human_out":0} # update meme_all_changes_timestep
        if meme is not None:
            if self.trackmeme is True:
                self._update_meme_popularity(meme, agent)



            print("meme was shared or posted, not None")
            # spread (truncate feeds at max len alpha)
            follower_idxs = self.network.predecessors(agent) #return list of int
            follower_uids = [n['uid'] for n in self.network.vs if n.index in follower_idxs]

            humfollower_uids = [n['uid'] for n in self.network.vs if (n.index in follower_idxs) and (n['bot']==0)]


            for follower in follower_uids:
                #print('follower feed before:', ["{0:.2f}".format(round(m[0], 2)) for m in G.nodes[f]['feed']])
                # add meme to top of follower's feed (theta copies if poster is bot to simulate flooding)

                if agent['bot']==1:
                    follower_influx = self._add_meme_to_feed(follower, meme, n_copies = self.theta)
                else:
                    follower_influx = self._add_meme_to_feed(follower, meme)

                assert(len(self.agent_feeds[follower]) <= self.alpha)

                # only track in-outflux for human agents
                if (self.track_forgotten is True) and (follower in humfollower_uids):
                    for flowtype in follower_influx.keys():
                        influx_by_agent_all[flowtype] += follower_influx[flowtype]

                    for flowtype in follower_influx.keys():
                        self.meme_replacement[follower][flowtype] = follower_influx[flowtype]

        return influx_by_agent_all


    def update_quality(self):
        # use exponential moving average for convergence
        # new_quality = 0.8 * self.quality + 0.2 * self.measure_average_quality()
        new_quality = self.rho * self.quality + (1-self.rho) * self.measure_average_quality()  #b: forget the past slowly
        self.quality_diff = abs(new_quality - self.quality) / self.quality if self.quality > 0 else 0
        self.quality = new_quality


    def measure_kendall_tau(self):
        # calculate discriminative power of system
        # Call only after self._return_all_meme_info() is called

        quality_ranked = sorted(self.meme_dict, key=lambda m: m['quality'])
        for ith, elem in enumerate(quality_ranked):
            elem.update({'qual_th':ith})

        share_ranked = sorted(quality_ranked, key=lambda m: m['human_shares'])
        for ith, elem in enumerate(share_ranked):
            elem.update({'share_th':ith})

        idx_ranked = sorted(share_ranked, key=lambda m: m['id'])
        ranking1 = [meme['qual_th'] for meme in idx_ranked]
        ranking2 = [meme['share_th'] for meme in idx_ranked]
        tau, p_value = utils.kendall_tau(ranking1, ranking2)
        return tau, p_value

    def measure_average_quality(self):
        # calculate average quality of memes in system
        # count_bot=False
        # calculate meme quality for tracked Users
        total=0
        count=0

        human_uids = [n['uid'] for n in self.network.vs if n['bot']==0]
        for u in human_uids:
            for meme in self.agent_feeds[u]:
                total+= meme.quality
                count+=1

        self.memes_human_feed = count
        return total / count if count >0 else 0


    def measure_diversity(self):
        # calculate diversity of the system using entropy (in terms of unique memes)
        # Call only after self._return_all_meme_info() is called

        humanshares = []
        for human, feed in self.agent_feeds.items():
            for meme in feed:
                humanshares += [meme.id]
        meme_counts = Counter(humanshares)
        count_byid = sorted(dict(meme_counts).items()) #return a list of [(memeid, count)], sorted by id
        humanshares = np.array([m[1] for m in count_byid])

        # humanshares = np.array([meme["human_shares"] for meme in self.meme_dict])
        # humanshares = np.array([meme["human_shares"] for meme in self.meme_dict])
        # botshares = np.array([meme["bot_shares"] for meme in self.meme_dict])

        hshare_pct = np.divide(humanshares, sum(humanshares))
        diversity = utils.entropy(hshare_pct)*-1
        # Note that (np.sum(humanshares)+np.sum(botshares)) !=self.num_memes because a meme can be shared multiple times
        return diversity


    def measure_average_zero_fraction(self):
        # calculate fraction of low-quality memes in system (for tracked User)
        count = 0
        zero_memes = 0

        human_uids = [n['uid'] for n in self.network.vs if n['bot']==0]
        for u in human_uids:
            zero_memes += sum([1 for meme in self.agent_feeds[u] if meme.quality==0])
            count += len(self.agent_feeds[u])

        return zero_memes / count

    def _add_meme_to_feed(self, agent_id, meme, n_copies=1):
        # Insert meme to feed. Forget if feed size exceeds alpha (Last in last out)

        feed = self.agent_feeds[agent_id]
        feed[0:0] = [meme] * n_copies

        meme_influx = {"bot_in":0, "bot_out": 0, "human_in":0, "human_out":0}

        if meme.is_by_bot==1:
            meme_influx["bot_in"] = n_copies
        else:
            meme_influx["human_in"] = n_copies

        if len(feed) > self.alpha:
            if self.track_forgotten is True:
                forgotten = self.agent_feeds[agent_id][self.alpha:] # keep track of forgotten memes
                n_bot_out= len([meme for meme in forgotten if meme.is_by_bot==1])
                n_human_out= len(forgotten) - n_bot_out

                meme_influx["bot_out"] = n_bot_out
                meme_influx["human_out"] = n_human_out

            self.agent_feeds[agent_id] = self.agent_feeds[agent_id][:self.alpha] # we can make sure dict values reassignment is correct this way
            # Remove memes from popularity info & all_meme list if extinct
            for meme in set(self.agent_feeds[agent_id][self.alpha:]):
                _ = self.meme_popularity.pop(meme.id, 'No Key found')
                self.all_memes.remove(meme)
            return dict(meme_influx)
        else:
            return dict(meme_influx)


    def _return_all_meme_info(self):
        for meme in self.all_memes:
            assert isinstance(meme, Meme)
        #Be careful
        memes = [meme.__dict__ for meme in self.all_memes] #convert to dict to avoid infinite recursion
        for meme_dict in memes:
            meme_dict.update(self.meme_popularity[meme_dict['id']])
        return memes

    def _update_meme_popularity(self, meme, agent):
        # meme_popularity is a value in a dict: list (is_by_bot, human popularity, bot popularity)
        # (don't use tuple! tuple doesn't support item assignment)
        if meme.id not in self.meme_popularity.keys():
            self.meme_popularity[meme.id] = {"is_by_bot": meme.is_by_bot, "human_shares":0, "bot_shares":0, "spread_via_agents":[]}

        self.meme_popularity[meme.id]["spread_via_agents"] += [int(agent['id'])] #index needs to be int

        if agent['bot']==0:
            self.meme_popularity[meme.id]["human_shares"] += 1
        else:
            self.meme_popularity[meme.id]["bot_shares"] += self.theta
        return
