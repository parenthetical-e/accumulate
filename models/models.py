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


def _create_d_result(decision, chosen_score, unchosen_score, rt):
    """ Converts the decision data to a dictionary. """
    
    return {
        'decision' : decision,
        'chosen_score' : chosen_score,
        'unchosen_score' : unchosen_score,
        'rt' : rt
    }


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
            return _create_d_result('A', score_A, score_B, trial_counter)
        elif score_A < score_B:
            return _create_d_result('B', score_B, score_A, trial_counter)
        elif score_A == score_B:
            return _create_d_result('N', score_A, score_B, trial_counter)
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


def abscount(trial, threshold):
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

        # And see if a decision can be made
        decision = _decider(score_A_norm, score_B_norm, threshold, ii+1)
        if decision != None:
            return decision
    else:
        # If threshold is never met,
        # we end up here...
        return _create_d_result('N', None, None, None)


def relcount(trial, threshold):
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
            decision = _decider(score_A, score_B, threshold, ii+1)
            if decision != None:
                return decision
        else:
            continue
    else:
        # If threshold is never met,
        # we end up here...
        return _create_d_result('N', None, None, None)
    
      
def naive_probability(trial, threshold):
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
                return _create_d_result(lastcat, score, 0.5, ii+2)
        else:
            # Otherwise reset
            lastcat = t
            p = 0.5

    # If threshold is never met,
    # we end up here...
    # this is a neutral trial.
    return _create_d_result('N', None, None, None)


def information(trial, threshold):
    """ Incrementally calculate the binary entropy of the sequence 
    of As and Bs in <trial>, decide when H(A) or H(B) exceeds 
    <threshold>. """

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
        decision = _decider(H_a * norm_const, 
                H_b * norm_const, threshold, ii+1)
        if decision != None:
            return decision
    else:
        # If threshold is never met,
        # we end up here...
        return _create_d_result('N', None, None, None)


# TODO: test me
def likelihood_ratio(trial, threshold):
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
                raise ValueError("Something is very wrong with the scores.")
    else:
       # If threshold is never met,
       # we end up here...
       return _create_d_result('N', None, None, None)
    

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
#         return _create_d_result('N', None, None, None)
