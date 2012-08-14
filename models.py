""" Many many models of 2 category accumulation. """

def count(self,trial,threshold):
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


def bayes(self,trial,threshold):
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


def likelihood(self,trial,threshold):
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
# Add info_rate (information but each H is divided by ii)
# Add first diriv of rate too.
# Add urgency gating and drift...
def information(self,trial,threshold):
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


def drift(self,trial,threshold):
    pass 
    # TODO


def last(self,trial,threshold):
    """ 
    Use the last exemplar to make the decision on <trial>. 
    <threshold> is ignored (but is included to keep the 
    signature consistent).
    """
    return trial[-1],1,0,len(trial)


def first(self,trial,threshold):
    """ 
    Use the first exemplar to make the decision on <trial>.
    <threshold> is ignored (but is included to keep the
    signature consistent).
    """
    return trial[0],1,0,len(trial)

