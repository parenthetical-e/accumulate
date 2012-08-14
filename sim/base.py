import itertools
import numpy as np
from accumulate import models

class Exp():
    """ Simulate and analyze 2 category accumulation designs. """
    
    def __init__(self,l):
        if (l % 2) == 0:
            self.l = float(l)
        else:
            raise ValueError('l must be even.')
        
        self.trials = list(
                itertools.product('AB',repeat=l))
            ## Calculate all possible unique combinations 
            ## for a given trial length.
    

    def _hamming(self,trial):
        """ 
        Return the minumum hamming distance between the two 'undecidable'
        trials (e.g. ABAB, BABA when l is 4) and <trial>.
        """

        # Create the two undecidable trials
        refA = ('A','B') * int(self.l/2)
        refB = ('B','A') * int(self.l/2)

        # Calculate the 
        # two Hamming Ds
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


    def _count(self,trial):
        """ Return a count of As and Bs for <trial>. """
        cA = 0
        for t in trial:
            if t == 'A': 
                cA += 1
        
        # cB is the l - cA...
        return cA, (int(self.l) - cA)

     
    def categorize(self,decide='count',threshold=0.5,params=None):
        """ 
        Return category decisions, scores for both the chosen and 
        the not, the number of exemplars experienced, using the 
        decision criterion <decide> ('count', 'bayes', 'likelihood', 
        'drift', 'information' or 'last') and <threshold> (0-1).

        If the decider requires extra parameters, include them in the 
        params dictionary, e.g. the drift decider needs a weight, w,
        so params would be {'w':0.25} if w was 0.25. 
        """

        # Threshold is valid?
        if threshold >= 1 or threshold <= 0:
            raise ValueError('<threshold> must be between 0 - 1.')

        # OK. Run the decider (of form self._d_*)
        decider = getattr(models, decide)
        if params == None:
            return [decider(self,trial,threshold) for trial in self.trials]
        else:
            return [decider(self,trial,threshold,**params) 
                    for trial in self.trials]


    def distances(self):
        """ 
        Return the minimum Hamming Distance between the two 
        'undecidable' trials types (e.g. ABAB, BABA when l is 4).  

        This may be used an objective measure of trial difficulty.  
        
        Low scores suggest greater difficulty.
        """

        return [self._hamming(trial) for trial in self.trials]


    def counts(self):
        """  Return the number of As and Bs. """
        
        return [self._count(trial) for trial in self.trials]


    def correct(self):
        """ 
        Return the right answer if the particiapnt always waited 
        to the end and only counted.  This (it is assumed) is the 
        most accurate strategy.
        """

        cs = self.counts()
        corr = []
        for c in cs:
            if c[0] > c[1]:
                corr.append('A')
            elif c[0] < c[1]:
                corr.append('B')
            else:
                corr.append('N')

        return corr


    def write_trials(self,encoding=None):
        """ 
        Write out trials, each row is a trial.  

        If <encoding> is a list of length 2 the first entry will be used to 
        encode 'A' the second for 'B'.
        """
        import csv

        # Re-encode... if not None
        # and of length 2
        en_trials = []
        if encoding != None:
            if len(encoding) == 2:
                # Loop over trials and each element,
                # appending the re-encoded elements.
                for trial in self.trials:
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

