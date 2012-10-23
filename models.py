# TODO:
# Add info_rate (information but each H is divided by ii)
# Add first diriv of rate too.
# Add urgency gating and
# drift...
# LBA
# scipy.stats.binom.sf or scipy.stats.binom_test to do a binomial test
# as well as Sequential test (SPRT, Wald) log-liklihood ratio
# and ....

""" Many many models of 2 category accumulation. """
import numpy as np


def _decider(score_A, score_B, threshold, trial_counter):
    """ Decide between the (normalized) scores based on <threshold>. 
    This is just a helper function, it is not always used. 
    
    Note: this is a convenience function. It is often, but not
    always, used. """

    # Is the threshold met or exceed? 
    if (score_A >= threshold) or (score_B >= threshold):
        # If score_A is bigger, pick it
        # or pick score_B if it is bigger
        # however if they are the same,
        # return neutral
        if score_A > score_B:
            return 'A', score_A, score_B, trial_counter
        elif score_A < score_B:
            return 'B', score_B, score_A, trial_counter
        elif score_A == score_B:
            return 'N', score_A, score_B, trial_counter
                ## It is unlikely that this case will
                ## ever occur however I feel it is 
                ## better to deal with this case explictly
                ## just in case
        else:
            # It should be impossible to get here, however
            # just in case something very odd happens....
            raise ValueError("Something is very wrong with the scores")
            
    # Not met? Return None.
    else:
        return None


def count(self, trial, threshold, **params):
    """ Return a category (A, B, or N (neutral)) for <trial> 
    based on number of As versus Bs. """
    import random
    
    cat = 'N'
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

        # And see if a decision can be made
        decision = _decider(score_A_norm, score_B_norm, threshold, ii+1)
        if decision != None:
            return decision
    else:
        # If threshold is never met,
        # we end up here...
        return 'N', None, None, None


# TODO: I is borken, do not use.
# def bayes(self, trial, threshold, **params):
#     """ Use Bayes rule to calculate p(A) and p(B), deciding on the 
#     category when <threshold> is exceeded. """
#     from copy import deepcopy
# 
#     # Init all the probabilites.
#     pA = 0.5
#     pB = 0.5
#     pA_X = 0.5
#     pB_X = 0.5
# 
#     pX = 1.0 / 2.0 ** float(len(trial))
#     pX_A = pX * 0.5
#     pX_B = pX * 0.5
#         
#     print("----")
#     print(trial)
#     for ii, t in enumerate(trial):
#         # The prior for X (how probable is the 
#         # current sequence) changes
#         # as we walk through the trial.
# 
#         # pX = 1 / ((2.0 ** float(ii)) + 1.0)
#         
#         # Update pA_X or pB_X
#         if t == 'A':
#             pA_X = (pA * pX_A) / pX
#         else:
#             pB_X = (pB * pX_B) / pX
#         
#         print("({5}). pA = {0}, pB = {1}, pX = {2}, pA_X = {3}, pB_X = {4}".format(
#                 pA, pB, pX, pA_X, pB_X, ii))
#         # Try to decide
#         decision = _decider(pA_X, pB_X, threshold, ii+1)
#         if decision != None:
#             return decision
#         
#         # If no decision, 
#         # update pX from pA.
#         pX_A = deepcopy(pA_X)
#         pX_B = deepcopy(pB_X)
#     else:
#         # If threshold is never met,
#         # we end up here...
#         return 'N', None, None, None


def naive_probability(self, trial, threshold, **params):
    """ Calculate the likelihood of the continuous sequence of either
    A or B in <trial>, decide when p_sequence(A) or (B) exceeds <threshold>. """
    
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
    return 'N', None, None, None


def information(self, trial, threshold, **params):
    """ Incrementally calculate the binary entropy of the sequence 
    of As and Bs in <trial>, decide when H(A) or H(B) exceeds 
    <threshold>. """

    H_a = 0
    H_b = 0
    norm_const = np.log2(self.l) / self.l
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
        decision = _decider(H_a * norm_const, 
                H_b * norm_const, threshold, ii+1)
        if decision != None:
            return decision
    else:
        # If threshold is never met,
        # we end up here...
        return 'N', None, None, None


# TODO: test me
def likelihood_ratio(self, trial, threshold, **params):
    """ Use a version of the sequential ratio test to decide (log_10). """
     
    from math import log, fabs
    
    # Transform threshold to suitable deciban
    # equivilant.
    dthreshold = threshold * 2.0
        ## 2 decibans is 99% confidence,
        ## so use that to map threshold (0-1)
        ## to the deciban threshold (dthreshold).

    p_A = 0.5
    p_B = 0.5
    logLR = 0
    for ii,t in enumerate(trial):
        if t == 'A':
            p_A += 1 / self.l
        else:
            p_B += 1 / self.l
        
        logLR += log(p_A/p_B, 10)
        
        # A custom decision function
        # was necessary:
        if fabs(logLR) >= dthreshold:
            if logLR > 0:
                return 'A', logLR, 0, ii+1
            elif logLR < 0:
                return 'B', 0, logLR, ii+1
            elif logLR == 0:
                return 'N', logLR, logLR, ii+1
            else:
                # It should be impossible to get here, however
                # just in case something very odd happens....
                raise ValueError("Something is very wrong with the scores.")
    else:
       # If threshold is never met,
       # we end up here...
       return 'N', None, None, None
    

def drift(self, trial, threshold, **params):
    pass 
    # TODO


def first_n(self, trial, threshold, **params):
    """ 
    Use count() and only the last <n> exemplars to make the 
    decision on <trial>.  params should contain <n>.
    """

    n = params['n']
    return count(self, trial[0:n], threshold)


def last_n(self, trial, threshold, **params):
    """ 
    Use count() and only the first <n> exemplars to make the 
    decision on <trial>.  params should contain <n>.
    """
    
    n = params['n']
    return count(self, trial[-n:], threshold)

