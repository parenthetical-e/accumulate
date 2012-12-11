from accumulate.models.models import abscount

# TODO:
# Add urgency gating and
# LBAs
# scipy.stats.binom.sf or scipy.stats.binom_test to do a binomial test
# and ....

""" Many many models of 2 category accumulation. """
import numpy as np
from accumulate.models.deciders import _create_d_result
from accumulate.models.noise import dummy

# Add noise to all functions below.... 


def create_abscount(threshold, decider):
    """ Return a category (A, B, or N (neutral)) for <trial> 
    based on number of As versus Bs. """
    
    def abscount(trial):
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
    """ Return a category (A, B, or N (neutral)) for <trial> 
        based on proportion of As to Bs. """
        
    def relcount(trial):
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
    """ Calculate the likelihood of the continuous sequence of either
    A or B in <trial>, decide when p_sequence(A) or (B) exceeds <threshold>. """
    
    def naive_probability(trial):
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
                    return _create_d_result(lastcat, score, 0.5, ii+2)
            else:
                # Otherwise reset
                lastcat = t
                p = 0.5

        # If threshold is never met,
        # we end up here...
        # this is a neutral trial.
        return _create_d_result('N', None, None, None)

    return naive_probability
    

def create_information(threshold, decider):
    """ Incrementally calculate the binary entropy of the sequence 
    of As and Bs in <trial>, decide when H(A) or H(B) exceeds 
    <threshold>. """
    
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


def create_likelihood_ratio(threshold, decider):
    """ Use a version of the sequential ratio test to decide (log_10). """
    
    def likelihood_ratio(trial):
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
                    raise ValueError("Something is very wrong with the scores.")
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return likelihood_ratio


def create_urgency_gating(threshold, decider):
    """ TODO """
        
    def urgency_gating(trial):
        
    
    return urgency_gating


def create_lba(threshold, decider, params):
""" In progress. """ 
   
    def lba(trial):
        pass 
        # TODO

    return lba
    
    
def create_leaky_lba(threshold, decider, ):
    
    def leaky_lba(trial):
        pass
    
    return leaky_lba


def create_first_n(n):
    """ 
    Use count() and only the last <n> exemplars to make the 
    decision on <trial>.  Params should contain <n>.
    """
    
    def first_n(trial, threshold, decider):
        return abscount(self, trial[0:n], threshold, decider)
        
    return first_n


def create_last_n(n):
    """ 
    Use count() and only the first <n> exemplars to make the 
    decision on <trial>.  Params should contain <n>.
    """
    
    def last_n(trial, threshold, decider):
        return abscount(self, trial[-n:], threshold, decider)
        
    return last_n


# TODO: I is borken, do not use.
# def bayes(trial, threshold, **params):
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
#         decision = decider(pA_X, pB_X, threshold, ii+1)
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
#         return _create_d_result('N', None, None, None)
