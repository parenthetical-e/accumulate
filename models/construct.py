# TODO:
# Add urgency gating and lba, leaky lba, race
# LBAs
# scipy.stats.binom.sf or scipy.stats.binom_test to do a binomial test
# and ....
# Add noise to all functions below.... 

""" Many many models of 2 category accumulation.  Each is a function closure
that constructs the final model, which should only take on argument, the trial sequence. """
import numpy as np
from accumulate.models.deciders import _create_d_result
from accumulate.models.noise import dummy


def _check_threshold(threshold):
    """ Checks the threshold is in bound. """

    # Threshold is valid?
    if threshold >= 1 or threshold <= 0:
        raise ValueError('<threshold> must be between 0 - 1.')


def _p_response(trial, i, letter):
    """ Use Cisek's method to calculate the p(correct response) for <letter>
    (i.e. A or B) for <trial> sliced from 0 to <i>. """
    
    from math import factorial
    
    # Find the counts for A or B
    # from 0:i
    cA = 0
    cB = 0
    for t in trial[0:i+1]:
        if t == 'A':
            cA += 1
        else:
            cB += 1
    
    # And the number of unseen   
    cN = len(trial) - cB + cB

    # Use letter to decide the sum
    # index, in part anyway
    if letter == 'A':
        sumlim = cA
    elif letter == 'B':
        sumlim = cB
    else:
        raise ValueError('letter must be A or B not (0}).'.format(letter))
    
    # Create the summation index
    sumindex = range(min(cN, 7 - sumlim))
    
    # Finally calculate the p(correct response)
    # for either A or B depending on letter 
    # (i.e. letter)
    p_r = (cN / (2.0 ** cN)) * sum(
        [1.0 / (factorial(k) * factorial((cN - k))) for k in sumindex]
    )
    
    return p_r
    
    
def create_abscount(threshold, decider):
    """ Create a decision function that use the counts of A and B to 
    decide. """
    
    _check_threshold(threshold)
    
    def abscount(trial):
        """ Return a category (A, B, or N (neutral)) for <trial> 
        based on number of As versus Bs. """
        
        import random
    
        score_A = 0
        score_B = 0
        l = float(len(trial))
    
        for ii, t in enumerate(trial):
            # Update scores based on t
            if t == 'A':
                score_A += 1
            else:
                score_B += 1

            # Norm them
            score_A_norm = score_A / l
            score_B_norm = score_B / l     
            
            # print("({0}). {1}, {2}".format(ii, score_A_norm, score_B_norm))
            
            # And see if a decision can be made
            decision = decider(score_A_norm, score_B_norm, threshold, ii+1)
            if decision != None:
                return decision
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)
    
    return abscount

    
def create_relcount(threshold, decider):
    """ Create a decision function that use the relative difference
    in A and B counts to decide. """
        
    _check_threshold(threshold)
        
    def relcount(trial):
        """ Return a category (A, B, or N (neutral)) for <trial> 
            based on proportion of As to Bs. """
        
        cA = 0.0
        cB = 0.0
        for ii, t in enumerate(trial):
            # Update scores based on t
            if t == 'A':
                cA += 1
            else:
                cB += 1
        
            if (cA > 0) and (cB > 0):
                score_A = cA / (cA + cB)
                score_B = 1 - score_A

                # And see if a decision can be made
                decision = decider(score_A, score_B, threshold, ii+1)
                if decision != None:
                    return decision
            else:
                continue
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return relcount


def create_naive_probability(threshold, decider):      
    """ Create a decision function using naive (multiplicative)
    probability estimates. """
    
    _check_threshold(threshold)
    
    def naive_probability(trial):
        """ Calculate the likelihood of the continuous sequence of either
        A or B in <trial>, decide when p_sequence(A) or (B) exceeds 
        <threshold>. """
        
        from copy import deepcopy

        ## Init
        score_A = 0
        score_B = 0        
        lastcat = trial[0]
        p = 0.5

        # Loop over trial calculating scores.
        for ii,  hht in enumerate(trial[1:]):
            if t == lastcat:
                # If t is the same, 
                # decrease the likelihood (p).
                p = p * 0.5
                
                # Assign p to a score, also reflect it
                if t == 'A':
                    score_A = 1 - deepcopy(p)
                else:
                    score_B = 1 - deepcopy(p)
                
                # And see if a decision can be made
                decision = decider(score_A, score_B, threshold, ii+1)
                if decision != None:
                    return decision
            else:
                # Otherwise reset
                lastcat = deepcopy(t)
                p = 0.5
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return naive_probability
    

def create_information(threshold, decider):
    """ Create a information theory based decision function. """
    
    _check_threshold(threshold)
    
    def information(trial):
        H_a = 0
        H_b = 0
        l = float(len(trial))
        norm_const = np.log2(l) / l
        for ii,t in enumerate(trial):
            if t == 'A':
                H_a +=  -0.5 * np.log2(0.5)
                    ## For a binary alphabet, b-ary entropy is
                    ## H(A) = sum_i(b*log_2(b))
                    ## where b is the probability a letter
                    ## in the alphabet
                    ## appears at slot i (i.e. = t above).
                    ## In this case b = p(A) = p(b) = 0.5 for all i.
            else:
                H_b +=  -0.5 * np.log2(0.5)

            # And see if a decision can be made
            decision = decider(H_a * norm_const, 
                    H_b * norm_const, threshold, ii+1)
            if decision != None:
                return decision
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return information


def create_likelihood_ratio(threshold, decider):
    """ Create a likelihood_ratio function. """
    
    _check_threshold(threshold)

    def likelihood_ratio(trial):
        """ Use a version of the sequential ratio test to decide (log_10). """
        from math import log, fabs
    
        # Transform threshold to suitable deciban
        # equivilant.
        dthreshold = threshold * 2.0
            ## 2 decibans is 99% confidence,
            ## so use that to map threshold (0-1)
            ## to the deciban threshold (dthreshold).

        cA = 0.0
        cB = 0.0
        logLR = 0.0
        l = float(len(trial))
        for ii,t in enumerate(trial):
            if t == 'A':
                cA += 1
            else:
                cB += 1
        
            if (cA > 0) and (cB > 0):
                logLR += log(cA/cB, 10)
            else:
                continue
                ## This implementaion can't decide on all
                ## A or B trials.  Live with this edge case for now?
        
            # A custom decision function
            # was necessary:
            if fabs(logLR) >= dthreshold:
                if logLR > 0:
                    return _create_d_result('A', logLR, 0, ii+1)
                elif logLR < 0:
                    return _create_d_result('B', logLR, 0, ii+1)
                elif logLR == 0:
                    return _create_d_result('N', logLR, 0, ii+1)
                else:
                    # It should be impossible to get here, however
                    # just in case something very odd happens....
                    raise ValueError(
                            "Something is very wrong with the scores.")
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return likelihood_ratio

    
def create_urgency_gating(threshold, decider, gain=0.4):
    """ Create a urgency gating function (ala Cisek et al 2009.). """
    
    _check_threshold(threshold)
    
    def urgency_gating(trial):
        """ Decide using Cisek's (2009) urgency gating algorithm. """
        
        l = float(len(trial))
        for ii, t in enumerate(trial):
            urgency = ii / l
            
            pA_ii = _p_reponse(trial, ii, 'A')
            pB_ii = _p_reponse(trial, ii, 'B')
            
            score_A = gain * urgency * (pA_ii - 0.5)
            score_B = gain * urgency * (pB_ii - 0.5)
            
            decision = decider(score_A, score_B, threshold, ii+1)
            if decision != None:
                return decision
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return urgency_gating


def create_incremental_lba(threshold, decider, k, d):
    """ Create a version of Brown and Heathcote's (2008) LBA 
    model modified so A/B updates are exclusive rather than simultaneous. 
    
    Input
    -----
    k - the start point.
    d - the drift rate.
    """ 
    
    _check_threshold(threshold)
    
    def incremental_lba(trial):
        """ Use Brown and Heathcote's (2008) LBA model, modified so A/B updates 
        are exclusive rather than simultanous, to make the decision. """
        
        k = float(k)
        d = float(d)
            ## Just in case 
            ## they're int
    
        # Init
        score_A = k
        score_B = k
        for t in trial:
            if t == 'A':
                # An incremental version of LBA.
                # that recognizes the balistic updates 
                # are exclusive.  A and B updates happen
                # at each time step.  In this form
                # updates are exclusive to A or B
                # but still ballistic.
                score_A += d
            else:
                score_A += d
                
            decision = decider(score_A, score_B, threshold, ii+1)
            if decision != None:
                return decision
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)            
    
    return incremental_lba
    
    
def create_incremental_lb(threshold, decider, k, d, leak):
    """ Next! """
    
    _check_threshold(threshold)
    
    def incremental_lb(trial):
        pass
    
    return incremental_lb


# # TODO Need to be redone, they're incompatible with the new constructor scheme
# def create_first_n(n):
#     """ 
#     Use count() and only the last <n> exemplars to make the 
#     decision on <trial>.  Params should contain <n>.
#     """
#     
#     def first_n(trial, threshold, decider):
#         return abscount(self, trial[0:n], threshold, decider)
#         
#     return first_n
# 
# 
# def create_last_n(n):
#     """ 
#     Use count() and only the first <n> exemplars to make the 
#     decision on <trial>.  Params should contain <n>.
#     """
#     
#     def last_n(trial, threshold, decider):
#         return abscount(self, trial[-n:], threshold, decider)
#         
#     return last_n
