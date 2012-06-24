import itertools
import numpy as np


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

     
    def _d_meta(trial,threshold):
        # TODO: use all sensible algs to produce an average 
        # p(A) and (B),
        # deciding with that average.
        #
        # It would be lovely if this was better than the rest 
        # and the best fit 
        # for actual Ss performance. Hope for neat outcomes.

        pass


    def _d_count(self,trial,threshold):
        """ 
        Return a category (A, B, or N (neutral)) for <trial> 
        based on number of As versus Bs.
         """
         import random

        cat ='N'
        score_A = 0
        score_B = 0
        for ii,t in enumerate(trial):
            if t == 'A':
                score_A += 1
            else:
                score_B += 1

            if score_A/self.l >= threshold:
                return 'A', score_A/self.l, score_B/self.l, ii+1
            elif score_B/self.l >= threshold:
                return 'B', score_B/self.l, score_A/self.l, ii+1

        # If threshold is never met,
        # we end up here...
        # this is neutral trial.
        return 'N', -1, -1, -1


    def _d_bayes(self,trial,threshold):
        """
        Use Bayes rule to calculate p(A) and p(B), deciding on the 
        category when <threshold> is exceeded.
        """
        
        pA = 0.5
        pB = 0.5
        pX = 0.5
        pA_X = 0.5
        pB_X = 0.5
        pX_A = 0.5
        pX_B = 0.5
        pass
        # TODO


    def _d_likelihood(self,trial,threshold):
        """
        Calculate the likelihood of the continuous sequence of either
        A or B in <trial>, decide when p_sequence(A) or (B) 
        exceeds <threshold>.
        """
        
        lastcat = trial[0]
        p = 0.5
            ## Init

        for ii,t in enumerate(trial[1:]):
            if t == lastcat:
                # If t is the same, 
                # decrease the likelihood (p).
                p = p * 0.5

                # Test threshold
                score = 1 - p
                if score >= threshold:
                    return lastcat, score, 0.5, ii+2
            else:
                # Otherwise reset
                lastcat = t
                p = 0.5

        # If threshold is never met,
        # we end up here...
        # this is a neutral trial.
        return 'N', -1, -1, -1

    # TODO:
    # Add _d_info_rate (_d_information but each H is divided by ii)
    # Add first diriv of rate too.
    # Add urgency gating and drift...
    def _d_information(self,trial,threshold):
        """ 
        Incrementally calculate the binary entropy of the sequence 
        of As and Bs in <trial>, decide when H(A) or H(B) exceeds 
        <threshold>.
        """

        H_a = 0
        H_b = 0
        info_scale = np.log2(self.l)/self.l

        for ii,t in enumerate(trial):
            if t == 'A':
                H_a +=  -0.5 * np.log2(0.5)
                    ## For a binary alphabet, b-ary entropy is
                    ## H(A) = sum_ii(b*log_2(b))
                    ## where b is the probability a letter
                    ## in the alphabet
                    ## appears at slot ii (i.e. t above).
                    ## In this case b = p(A) = 0.5 for all ii.
            else:
                H_b +=  -0.5 * np.log2(0.5)
                    ## b = p(B) = 0.5.
            if (H_a * info_scale) >= threshold:
                return 'A', H_a, H_b, ii+1
            elif (H_b * info_scale) >= threshold:
                return 'B', H_b, H_a, ii+1

        # If threshold is never met,
        # we end up here...
        # this is a neutral trial.
        return 'N', -1, -1, -1


    def _d_drift(self,trial,threshold):
        pass 
        # TODO


    def _d_last(self,trial,threshold):
        """ 
        Use the last exemplar to make the decision on <trial>. 
        <threshold> is ignored (but is included to keep the 
        signature consistent).
        """
        return trial[-1],1,0,len(trial)


    def _d_first(self,trial,threshold):
        """ 
        Use the first exemplar to make the decision on <trial>.
        <threshold> is ignored (but is included to keep the
        signature consistent).
        """
        return trial[0],1,0,len(trial)


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
        decider = getattr(self,'_d_' + decide)
        if params == None:
            return [decider(trial,threshold) for trial in self.trials]
        else:
            return [decider(trial,threshold,**params) for trial in self.trials]


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

