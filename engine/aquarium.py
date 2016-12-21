from random import choice, sample, randint, random

from engine.inhabitants.plant import WaterPlant
from engine.inhabitants.prey import PreyFish
from engine.inhabitants.predator import PredatorFish
from engine.inhabitants.snail import Snail

from engine.tools import Singleton

        
class Aquarium(metaclass=Singleton):
    """
    Class represents the aquarium
    """
    # python 2 singleton style
    #__metaclass__ = Singleton 
    
    MIN_INHABITANTS = 20
    MAX_INHABITANTS = 100
    
    POSSIBLE_INHABITANTS = (PreyFish, PredatorFish, WaterPlant, Snail)
    
    PAIRS_OF_EATING = [ (PreyFish, WaterPlant), 
                        (Snail, WaterPlant), 
                        (PredatorFish, PreyFish) ]
    
    def __init__(self, quantity):
        if quantity < Aquarium.MIN_INHABITANTS \
                or quantity > Aquarium.MAX_INHABITANTS:
            raise Exception("Quantity of inhabitants must be in [{0}..{1}]"\
                .format(Aquarium.MIN_INHABITANTS, Aquarium.MAX_INHABITANTS))
        self.inhabitants = []
        self.populate(quantity)
        
    def get_random_inhabitant(self, name):
        inhabitant_class = choice(Aquarium.POSSIBLE_INHABITANTS)
        
        weight_rand_difference = random() * (inhabitant_class.MAX_WEIGHT - inhabitant_class.MIN_WEIGHT)
        inhabitant_weight = inhabitant_class.MIN_WEIGHT + weight_rand_difference
        
        return inhabitant_class(name, inhabitant_weight)
    
    def populate(self, quantity): 
        self.inhabitants = [self.get_random_inhabitant(str(i + 1)) for i in range(quantity)]
    
    def evalute_inhabitants(self):
        while self.thing_to_eat():
            subject, food = sample(self.inhabitants, 2)
            remains = subject.eat(food)
            if remains in self.inhabitants:
                self.inhabitants.remove(remains)
            
    def thing_to_eat(self):
        inhabitants_classes = set(inhabitant.__class__ for inhabitant in self.inhabitants)
        return any(set(pair).issubset(inhabitants_classes) for pair in Aquarium.PAIRS_OF_EATING)
    
    def __repr__(self):
        result = 'Aquarium include {0} inhabitants: \n'.format(len(self.inhabitants))
        
        def weight_sorted_output(_class):
            inhabitants = [inhabitant for inhabitant in self.inhabitants if inhabitant.__class__ is _class]
            ranged_inhabitants = sorted(inhabitants, key=lambda x: -x.weight)
            return _class.__name__, ranged_inhabitants
        
        def out_inhabitant_list(inahabitant_list, level='\t', modifier='\t'):
            result = ''
            for inhabitant in inahabitant_list:
                result += level + repr(inhabitant) + '\n'
                if inhabitant.eated:
                    result += level + modifier \
                        + 'eated:\n' + out_inhabitant_list(inhabitant.eated, level + modifier)
            return result
        
        inhabitant_groups = [
            weight_sorted_output(PreyFish),
            weight_sorted_output(PredatorFish),
            weight_sorted_output(Snail),
            weight_sorted_output(WaterPlant) 
            ]
        
        for group in inhabitant_groups:
            inhabitant_type, inhabitants_list = group
            if inhabitants_list:
                result += '\n {0}: \n {1}'.format(inhabitant_type, out_inhabitant_list(inhabitants_list)) 
           
        return result

