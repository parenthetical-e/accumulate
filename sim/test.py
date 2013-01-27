""" Classes from base modified to ease testing. """
from accumulate.sim.base import Trials

class SelectTrials(Trials):
    """ Experiment on a set of select trials whose modeled results should be 
    intuitive, or otherwise easy to analyze for correctness and 
    consistency. """
    
    
    def __init__(self, l):
        Trials.__init__(self, l)
    
    
    def _generate_trials():
        """ Returns a generator of select testing trials. """
    
        self.trial_count = 0
            ## reset
        
        test_trials = [
            ["A"] * l,
            ["B"] * l,
            ["A"] * l/2 + ["B"] * l/2
            ["B"] * l/2 + ["A"] * l/2
        ]
        
        return (t for t in test_trials) 
            ## A Generator expression
            