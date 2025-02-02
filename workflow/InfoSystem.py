import random
from User import User 
from Meme import Meme
import networkx as nx

from profileit import profile
"""
preferential_targeting = ['hubs', 'partisanship', 'misinformation', 'conservative', 'liberal']
or None for no targeting
"""
class InfoSystem:
    def __init__(self, graph_gml,
                preferential_targeting=None,
                return_net=False,
                count_forgotten=False,
                track_meme=False,
                network=None, 
                verbose=False,
                epsilon=0.001,
                mu=0.5,
                phi=1,
                gamma=0.1,
                alpha=15,
                theta=1):

        self.preferential_targeting=preferential_targeting
        # self.return_net = return_net
        self.verbose = verbose

        self.epsilon=epsilon
        self.mu=mu
        self.phi=phi
        self.gamma=gamma 
        self.alpha=alpha
        self.theta=theta
        
        #Keep track of number of memes globally
        self.num_memes=0
        self.num_meme_unique=0
        self.memes_human_feed = 0
        self.quality_diff = 1
        self.quality = 1
        self.time_step=0
        
        # dict of agent ids & list of their follower ids 
        self.follower_info = {}
        # only create a User object if that node is chosen during simulation
        # dict of agent ID - User obj for that agent
        self.tracking_agents = {}
        self.init_agents(graph_gml)
        self.init_followers()

    @profile
    def init_agents(self, graph_file):
        G = nx.read_gml(graph_file)
        
        # Try making 
        # bots = [n for n in G.nodes if G.nodes[n]['bot']==True]
        # humans = [n for n in G.nodes if G.nodes[n]['bot']==False]

        #debug
        # bao_indeg = []

        for agent in G.nodes:
            id = G.nodes[agent]['ID']
            friend_ids= [G.nodes[n]['ID'] for n in G.successors(agent)]
            self.tracking_agents[id] = User(id, friend_ids, feed_size=self.alpha, is_bot=G.nodes[agent]['bot'])

            follower_ids = [G.nodes[n]['ID'] for n in G.predecessors(agent)]
            self.follower_info[id] = follower_ids
            # if self.verbose:
            #     bao_indeg+=[len(follower_ids)]

        self.n_agents = nx.number_of_nodes(G)
        print('Initialized agents, total in original graph: {}, in Infosystem: {}'.format(self.n_agents, len(self.tracking_agents)))
        
        # if self.verbose:
        #     in_deg = [deg for node, deg in G.in_degree(G.nodes())] #number of followers
        #     print('Graph Avg in deg', round(sum(in_deg)/len(in_deg),2))
        #     print('Info Sys in deg: ', round(sum(bao_indeg)/len(bao_indeg),2))

    def init_followers(self):
        for aidx, agent in self.tracking_agents.items():
            # if follower list hasn't been realized into Users(), do it
            if agent.followers is None:
                follower_list = []
                for fid in self.follower_info[aidx]:
                    follower_list += [self.tracking_agents[fid]] # add all User object based on ids from follower list
                agent.set_follower_list(follower_list)
        print('Finish populating followers')


    @profile
    def simulation(self):
        while self.quality_diff > self.epsilon: 
            if self.verbose:
                # print('time_step = {}, q = {}, diff = {}'.format(self.time_step, self.quality, self.quality_diff), flush=True) 
                print('time_step = {}, q = {}, diff = {}, unique/human memes = {}/{}, all memes created={}'.format(self.time_step, self.quality, self.quality_diff, self.num_meme_unique, self.memes_human_feed, self.num_memes), flush=True) 
            self.time_step += 1
            for _ in range(self.n_agents):
                self.simulation_step()
            self.update_quality()

            #TODO: track meme
            # b: Return net: no need because the network doesn't change. 
            # we just need the net we init before 
        return self.quality
    
    @profile
    def simulation_step(self):
        id = random.choice(list(self.tracking_agents.keys())) # convert to list so that it's subscriptable
        agent = self.tracking_agents[id]
            
        # tweet or retweet
        if len(agent.feed) and random.random() > self.mu:
            # retweet a meme from feed selected on basis of its fitness
            meme = random.choices(agent.feed, weights=[m.fitness for m in agent.feed], k=1)[0] #random choices return a list
        else:
            # new meme
            self.num_meme_unique+=1
            meme = Meme(self.num_meme_unique, is_by_bot=agent.is_bot, phi=self.phi)
        #TODO: bookkeeping

        # spread (truncate feeds at max len alpha)
        
        for follower in agent.followers:
            #print('follower feed before:', ["{0:.2f}".format(round(m[0], 2)) for m in G.nodes[f]['feed']])   
            # add meme to top of follower's feed (theta copies if poster is bot to simulate flooding)
            
            if agent.is_bot==1:
                follower.add_meme_to_feed(meme, n_copies = self.theta)
                self.num_memes+=self.theta
            else:
                follower.add_meme_to_feed(meme)
                self.num_memes+=1
            assert(len(follower.feed)<=self.alpha)

    def update_quality(self):
        # use exponential moving average for convergence
        new_quality = 0.8 * self.quality + 0.2 * self.measure_average_quality()
        self.quality_diff = abs(new_quality - self.quality) / self.quality if self.quality > 0 else 0
        self.quality = new_quality

    # calculate average quality of memes in system
    # count_bot=False
    def measure_average_quality(self):
        # calculate meme quality for tracked Users
        total=0
        count=0
        humans = [user for user in self.tracking_agents.values() if user.is_bot==0] 
        for user in humans:
            for meme in user.feed:
                total += meme.quality
                count +=1
        self.memes_human_feed = count
        return total / count if count >0 else 0
    
    # calculate fraction of low-quality memes in system (for tracked User)
    #
    def measure_average_zero_fraction(self):
        count = 0
        zero_memes = 0 

        human_agents = [agent for agent in self.tracking_agents.values() if agent.is_bot==0]
        for agent in human_agents:
            zero_memes += sum([1 for meme in agent.feed if meme.quality==0])
            count += len(agent.feed)
    
        return zero_memes / count