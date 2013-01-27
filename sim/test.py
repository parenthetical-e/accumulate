""" Classes from base modified to ease testing. """
from accumulate.sim.base import Trials


class SelectTrials(Trials):
    """ Experiment on a set of select trials whose modeled results should be 
    intuitive, or otherwise easy to analyze for correctness and 
    consistency. """    
    
    def __init__(self, l):
        Trials.__init__(self, l)

        # Over ride max_trial_count...        
        self.max_trial_count = len(self._get_test_trials())
            ## Calling _get_test_trials()
            ## is inefficient (as it always called below too) but, well,
            ## it ensures max_trial_count is over-ridden correctly
            ## without use intervention.  I expect _get_test_trials()
            ## will be tweaked often during development.
    
    
    def _get_test_trials(self):
        """As is says on the label, get em. """
        
        l = int(self.l)
        test_trials = [
            ["A"] * l,  ## All A or B
            ["B"] * l,
            ["B"] + ["A"] * (l-1),  ## One then rest
            ["A"] + ["B"] * (l-1),
            ["A"] * (l/2) + ["B"] * (l/2),  ## Half and half
            ["B"] * (l/2) + ["A"] * (l/2),
            'AB' * (l/2),  ## Alternating A/B
            'BA' * (l/2)
        ]
        
        return test_trials
    
    
    def _generate_trials(self):
        """ Returns a generator of select testing trials. """
    
        self.trial_count = 0
            ## reset
        
        test_trials = self._get_test_trials()
        
        return (t for t in test_trials) 
            ## Returns a generator expression

