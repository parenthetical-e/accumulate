import itertools
from collections import defaultdict

import numpy as np
from accumulate import models

class Trials():
    """ Simulate and analyze 2 category accumulation designs. """
    
    def __init__(self, l):
        if (l % 2) == 0:
            self.l = float(l)
        else:
            raise ValueError('l must be even.')
        
        self.trial_count = 0
        self.trials = self._generate_trials()
        self.max_trial_count = (2 ** int(l))/2
            ## self.max_trial_count is used to stop self.trials 
            ## iterations.
            ## 
            ## We only want to iterate over the first half of trials
            ## as the second half is the first half's reflection.
            ## Examining the second half would double the needed
            ## computatioans while adding no useful information.


    def _generate_trials(self):
        """ Create a generator of all trial permutations. """

        self.trial_count = 0
            ## reset 

        return itertools.product('AB', repeat=int(self.l))
            ## Calculate all possible unique combinations 
            ## for a given trial length.


    def _hamming(self, trial):
        """ Return the minimum hamming distance between the two 'undecidable'
        trials (e.g. ABAB, BABA when l is 4) and <trial>. """

        # Create the two 
        # undecidable trials
        refA = 'AB' * int(self.l / 2)
        refB = 'BA' * int(self.l / 2)

        # Calculate the two Hamming Ds
        dA = 0 
        dB = 0
        for ii,t in enumerate(trial):
            if t != refA[ii]:
                dA += 1

            if t != refB[ii]:
                dB += 1

        # Return the smallest 
        # of the two Ds
        return min(dA, dB)


    def _count(self, trial):
        """ Return a count of As and Bs for <trial>. """
        
        # cA is the number of As
        cA = 0
        for t in trial:
            if t == 'A': 
                cA += 1
        
        # cB is the l - cA...
        return cA, (int(self.l) - cA)

   
    def print_trials(self):
        """ Print all trials to stdout. """

        # Print then reset trials
        print(list(self.trials))
        self.trials = self._generate_trials()
        

    def categorize(self, model, threshold, decider):
        """ Return category decisions, scores for both the chosen and 
        the not, the number of exemplars experienced, using the 
        decision criterion <decide> ('count', 'bayes', 'likelihood', 
        'drift', 'information' or 'last') and <threshold> (0-1).

        If the decider requires extra parameters, include them in the 
        params dictionary, e.g. the drift decider needs a weight, w,
        so params would be {'w':0.25} if w was 0.25. """

        # Threshold is valid?
        if threshold >= 1 or threshold <= 0:
            raise ValueError('<threshold> must be between 0 - 1.')

        # OK. Run the models.
        model_results = defaultdict(dict)
        while self.trial_count < self.max_trial_count:
            trial = ''.join(self.trials.next())

            # Make a decision
            decision = model(trial, threshold, decider)
                ## If the decider needs parameters construct
                ## via closure, see the code 
                ## accumulate.models.construct for details

            # Then store it in the (2) nested dict, model_results    
            model_results[trial][model.__name__] = decision
                
            # Update the stop counter
            self.trial_count += 1

        # For the next model, refresh trials.
        self.trials = self._generate_trials()

        return model_results


    def distances(self):
        """ 
        Return the minimum Hamming Distance between the two 
        'undecidable' trials types (e.g. ABAB, BABA when l is 4).  

        This may be used an objective measure of trial difficulty.  
        
        Low scores suggest greater difficulty.
        """

        # Calc the and return (in a dict) the distances.
        dist = dict()
        for ii, trial in enumerate(self.trials):
            if ii < self.max_trial_count:
                dist[''.join(trial)] = self._hamming(trial)
            else:
                break
            
        self.trials = self._generate_trials()

        return dist


    def counts(self):
        """  Return the number of As and Bs. """
            
        # Return the A/B counts in a dict
        cnts = dict()
        for ii, trial in enumerate(self.trials):
            if ii < self.max_trial_count:
                cnts[''.join(trial)] = self._count(trial)
            else:
                break
            
        self.trials =self._generate_trials()

        return cnts 


    def write_trials(self, encoding=None):
        """ Write out trials, each row is a trial.  

        If <encoding> is a list of length 2 the first entry will be used to 
        encode 'A' the second for 'B'. """
        import csv

        # Re-encode... if not None
        # and of length 2
        en_trials = []
        if encoding != None:
            if len(encoding) == 2:
                # Loop over trials and each element,
                # appending the re-encoded elements.
                for ii, trial in enumerate(self.trials):
                    if ii < self.max_trial_count:
                        en_t = []
                        for t in trial:
                            if t == 'A':
                                en_t.append(encoding[0])
                            else:
                                en_t.append(encoding[1])
                        en_trials.append(tuple(en_t))
                            ## converting to tuples so it is 
                            ## identical in format to self.trials
                            ## thought I doubt this will ever matter.
                    else:
                        break
            else:
                raise ValueError('<encoding> can only have two entries.')
        else:
            # Assign if encoding was None.
            en_trials = self.trials

        # Write it out...
        f = open(str(int(self.l)) + 'trials.dat', 'wb')
        w = csv.writer(f, delimiter='\t')
        w.writerows(en_trials)
        f.flush()
        f.close()
        
        # Finally reset trials
        self.trials = self._generate_trials()
        
