
import random

class Meme:
    def __init__(self, id, truncation_interval, is_by_bot=0, phi=1):
        self.id = id
        self.is_by_bot = is_by_bot
        self.phi = phi 
        self.truncation_interval = truncation_interval
        quality, fitness  = self.get_values()
        self.quality = quality
        self.fitness = fitness
        
    
    # return (quality, fitness, id) meme tuple depending on bot flag
    # using https://en.wikipedia.org/wiki/Inverse_transform_sampling
    # default phi = 1 is bot deception; >= 1: meme fitness higher than quality 
    # id: unique IDs

    # Nov 2022: sample quality and fitness (in paper: engagement) independently for human agents.
    def get_values(self):

        if self.is_by_bot==1:
            exponent = 1 + (1 / self.phi) # why 1+?
        else:
            exponent = 1 + self.phi # why 1+?
            
        u = random.random() # sample from between 0 to 1
        fitness = 1 - (1 - u)**(1 / exponent)

        if self.is_by_bot==1:
            quality = 0
        else:
            # quality = fitness
            u = random.random()
            quality = 1 - (1 - u)**(1 / exponent)

    # new addition to introduce some correlation of quality and fitness 
    # if sampled quality and fitness are do not fall within a truncated space of the distribution, 
    # then quality is moved to within the truncated space
        if self.truncation_interval > 0:
            if ((fitness - self.truncation_interval) <= quality <= (fitness + self.truncation_interval)) == False:
                if quality > fitness:
                    quality = fitness + self.truncation_interval
                    if quality > 1:
                        quality = 1
                if quality < fitness:
                    quality = fitness - self.truncation_interval
                    if quality < 0:
                        quality = 0
    
        return quality, fitness

            
