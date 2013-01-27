""" Many many models of 2 category accumulation.  Each is a function closure
that constructs the final model, which should only take one argument: the trial sequence. """
from math import log, fabs
import numpy as np
from accumulate.models.deciders import _create_d_result
from accumulate.models.noise import dummy
from accumulate.models.misc import check_threshold, update_name
    
   
def create_abscount(name, threshold, decider):
    """ Create a decision function that use the counts of A and B to 
    decide. 
    
    This implements the counting model (so far as I can tell, I can't find a
    copy, only other references to it) of Audely and Pike (1965) Some 
    stocastic models of choice, J of Math. and Stat. Psychology, 18, 
    207-225.  """
    
    check_threshold(threshold)
    
    @update_name(name)
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


def create_relcount(name, threshold, decider):
    """ Create a decision function that use the relative difference
    in A and B counts to decide. 
    
    A variation on Audely and Pike (1965, and abscount()) that uses the 
    relative ration of A/B instead of an absolute counter. """
        
    check_threshold(threshold)
    
    @update_name(name)    
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


def create_naive_probability(name, threshold, decider):      
    """ Create a decision function using naive (multiplicative)
    probability estimates. """
    
    check_threshold(threshold)

    @update_name(name)
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
        for ii, t in enumerate(trial[1:]):
            if t == lastcat:
                # If t is the same, 
                # decrease the likelihood (p).
                p = p * 0.5
                
                # Assign p to a score, 
                # also reflect it
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
    

def create_information(name, threshold, decider):
    """ Create a information theory based decision function. """
    
    check_threshold(threshold)
    
    @update_name(name)
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


# TODO - test me!
def create_snr(name, threshold, decider):
    """  Creates a model based on Gardelle et al's mean / SNR model.
    
    Note: This was not the best model in that paper (LLR was) but it was close 
    and in my opinion could be a useful/interesting 'bad model' to approximate 
    LLR, in some cases anyway (see 'Robust Averaging Across Elements in the 
    Decision Space' section in their results for an important caveat).  
    
    Also, we know the brain tracks averages and variances
    in economic tasks.
    
    See:
    De Gardelle, V., & Summerfield, C. (2011). Robust averaging during 
    perceptual judgment. PNAS, 108(32).
    """
    
    check_threshold(threshold)

    @update_name(name)
    def snr(trial):
        """ Gardelle et al's mean / SNR model. """

        cA = 0.0
        cB = 0.0     
        for ii, t in enumerate(trial):
            n = ii + 1  ## reindex needed
                        ## so n is the A/B count
            
            # Update the count (cA or cB)
            # calculate the mean and var
            # treating the trial sequence 
            # as a binomial distibution
            score_A = 0.0
            score_B = 0.0
            if t == 'A':                
                cA += 1
                pA = cA / n
                meanA = cA * pA
                varA = cA * pA * (1 - pA)
                
                # Skip if var is 0 
                if (varA == 0.00):
                    continue
                    
                score_A = meanA/varA
            else:
                cB += 1
                pB = cB / n
                meanB = cB * pB
                varB = cB * pB * (1 - pB)
                
                # Skip if var is 0 
                if (varB == 0.00):
                    continue
                    
                score_B = meanB/varB
            
            # And see if a decision can be made
            decision = decider(score_A, score_B, threshold, n)
            if decision != None:
                return decision
                
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return snr
            
    
def create_likelihood_ratio(name, threshold, decider):
    """ Create a likelihood_ratio function (i.e. sequential probability ratio 
    test).
    
    Empirical support:
    ----
    1. De Gardelle, V., & Summerfield, C. (2011). Robust averaging during 
    perceptual judgment. PNAS, 108(32). """
    
    check_threshold(threshold)

    @update_name(name)
    def likelihood_ratio(trial):
        """ Use a version of the sequential ratio test to decide (log_10). """
    
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


def _p_response(trial, i, letter):
    """ Use Cisek's method to calculate the p(correct response) for <letter>
    (i.e. A or B) for <trial> sliced from 0 to <i>. """
    
    from math import factorial
    
    print("i: {0}".format(i))
    print("trial: {0}".format(trial))
    
    # Find the counts for A or B
    # from 0:i
    cA = 0
    cB = 0
    for t in trial[0:i+1]:
        if t == 'A':
            cA += 1
        else:
            cB += 1
    
    # print("cA: {0}, cB: {1}".format(cA, cB))
    # And the number of unseen   
    l = len(trial)
    # print("l: {0}".format(l))
    # print("cA: {0}".format(cA))
    # print("cB: {0}".format(cB))
    # print("cA+cA: {0}".format(cA+cB))
    cN = l - (cA + cB)

    # Use letter to decide the sum
    # index, in part anyway
    if letter == 'A':
        sumlim = cA
    elif letter == 'B':
        sumlim = cB
    else:
        raise ValueError('letter must be A or B not (0}).'.format(letter))
    # print("sumlim: {0}".format(sumlim))
        
    # Create the summation index
    maxN = (len(trial)/2) - 1
    possN =  int(fabs(maxN - sumlim))

    # print("cN: {0}".format(cN))
    # print("maxN: {0}".format(maxN))
    # print("possN: {0}".format(possN))
    
    sumindex = range(min(cN, possN))
    # print("sumindex: {0}".format(sumindex))
    
    # Finally calculate the p(correct response)
    # for either A or B depending on letter 
    # (i.e. letter)
    factorials = [1.0 / (factorial(k) * factorial((cN - k))) for k in sumindex]
    # print("factorials: {0}".format(factorials))
    remaining_combinations = sum(
        factorials
    )
    # print("remaining_combinations: {0}".format(remaining_combinations))
    
    rescaler = (cN / (2.0 ** cN))
    # print("rescaler: {0}".format(rescaler))
    
    p_r = rescaler * remaining_combinations
    
    
    return p_r
    
        
def create_urgency_gating(name, threshold, decider, gain=0.4):
    """ Create a urgency gating function (i.e. implement: 
    Cisek et al (2009). Decision making in changing 
    conditions: The urgency gating model, J Neuro, 29(37) 
    11560-11571.) """
    
    check_threshold(threshold)

    @update_name(name)    
    def urgency_gating(trial):
        """ Decide using Cisek's (2009) urgency gating algorithm. """
        
        l = float(len(trial))
        for ii, t in enumerate(trial):
            urgency = ii  ## urgency is elapsed "time",
                          ## i.e. a index of trial length
            
            pA_ii = _p_response(trial, ii, 'A')
            pB_ii = _p_response(trial, ii, 'B')
            print("pA_ii: {0}".format(pA_ii))
            print("pB_ii: {0}".format(pB_ii))
            
            score_A = fabs(gain * urgency * (pA_ii - 0.5))
            score_B = fabs(gain * urgency * (pB_ii - 0.5))
            print("score_A: {0}".format(score_A))
            print("score_B: {0}".format(score_B))

            decision = decider(score_A, score_B, threshold, ii+1)
            if decision != None:
                return decision
        else:
            # If threshold is never met,
            # we end up here...
            return _create_d_result('N', None, None, None)

    return urgency_gating


def create_incremental_lba(name, threshold, decider, k=0.1, d=0.1):
    """ Create a version of Brown and Heathcote's (2008) LBA 
    model modified so A/B updates are exclusive rather than simultaneous. 
    
    Input
    -----
    k - the start point.
    d - the drift rate.
    """ 
    k = float(k)
    d = float(d)
        ## Just in case 
        ## they're int

    check_threshold(threshold)

    @update_name(name)
    def incremental_lba(trial):
        """ Use Brown and Heathcote's (2008) LBA model, modified so A/B updates 
        are exclusive rather than simultanous, to make the decision. """
        
                # Init
        score_A = k
        score_B = k
        for ii, t in enumerate(trial):
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
    
# TODO -- test
def create_blca(name, threshold, decider, length=10, k=0.1, wi=0.1, leak=0.1, beta=0.1):
    """ Creates a ballistic leaky competing accumulator model based on,
    
    Usher and McClelland (2001), The time course of perceptual choice: the leaky 
    competing accumulator model. Psychological Review, 108, 550-592, on which 
    this code is based. 
    
    Note: To keep notation consistent with other models in this framework, 
    the notation differs from that in Usher and McClelland.
    
    Input
    ----
    length - Length of the trial
    k - Start point
    wi - Intial connection wieght (same for obth A and B)
    leak - Leak rate
    beta - inhibtion strength
    """
    
    check_threshold(threshold)
    
    @update_name(name)
    def blcba(trial):
        """ Decide using Usher and McClelland's (2001) ballistic leaky
        competing accumulator model. """

        impulse = 1.0 / length  ## Set impulse height to the 
                                ## maximum possible score
                                ## is 1 for all trial lengths

        score = 0.0             ## Init at 0
        for ii, t in enumerate(trial):
            if t == 'A':
                rho = wi *  impulse
            else:
                rho = -wi * impulse

            score += (2 * rho - 1) - (leak - beta)  ## There is time-step
                                                    ## in the org equations
                                                    ## that I am setting to
                                                    ## 1 as these sims are 
                                                    ## temporally unit-less, 
                                                    ## i.e.,
                                                    ## dt / t = 1

            # Make scores explicit, consistent
            # with the notation used herein
            score_A = score
            score_B = 1 - score_A
                ## score is equivilant to score_A
                ## (see rho definition above)
                ## and B is tied to A

            decision = decider(score_A, score_B, threshold, ii+1)
            if decision != None:
                return decision
            else:
                # If threshold is never met,
                # we end up here...
                return _create_d_result('N', None, None, None)
           
    return blcba

  
# TODO -- Once the org is tested, create free x version of Usher
def create_blca_freex():
    pass


# TODO
def create_race(name, threshold, decider):
    """ Create a race to threshhold model as described in 
    
    Rowe et al (2010). Action selection: a race model for the selection and 
    non-selected actions distinguishes the contribution of premotor and 
    prefrontal areas. 

    Input
    -----
     
    """

    check_threshold(threshold)

    @update_name(name)
    def race(trial):
        """ A race to threshold model. """
    
             
            
    return race


def create_maximim(name, threshold, decider):
    """
    TODO
    """

    @update_name(name)
    def maximin(trial):
        pass

    return maximin


def create_robust_satisficing(name, threshold, decider):
    """
    TODO
    """

    @update_name(name)
    def robust_satisficing(trial):
        pass

    return robust_satisficing

