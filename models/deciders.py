# TODO Rework code so either an abs or relative (i.e. difference) dicider can be used interchangably.


def _create_d_result(decision, chosen_score, unchosen_score, rt):
    """ Converts the decision data to a dictionary. """
    
    return {
        'decision' : decision,
        'chosen_score' : chosen_score,
        'unchosen_score' : unchosen_score,
        'rt' : rt
    }


def _result_return(score_A, score_B, trial_counter):
    """ To be run after a succesful threshold check. Returns the result. """
    
    if score_A > score_B:
        return _create_d_result('A', score_A, score_B, trial_counter)
    elif score_A < score_B:
        return _create_d_result('B', score_B, score_A, trial_counter)
    elif score_A == score_B:
        return _create_d_result('N', score_A, score_B, trial_counter)
     ## It is unlikely that this case will
     ## ever occur however I feel it is 
     ## better to deal with this case explictly,
     ## just in case
    else:
    # It should be impossible to get here, however
    # just in case something very odd happens....
        raise ValueError("Something is very wrong with the scores")


def absolute(score_A, score_B, threshold, trial_counter):
    """ Decide between the (normalized) scores based on <threshold>. 
    This is just a helper function, it is not always used. """

    # Is the threshold met or exceeded? 
    if (score_A >= threshold) or (score_B >= threshold):
        return _result_return(score_A, score_B, trial_counter)
        
    # Not met? Return None.
    else:
        return None
        

def difference(score_A, score_B, threshold, trial_counter):
    """ Decide between the difference of the  scores based on <threshold>. 
    This is just a helper function, it is not always used. """
    
    diff = abs(score_A - score_B)
    
    # Is the threshold met or exceeded? 
    if diff >= threshold:
        return _result_return(score_A, score_B, trial_counter)

    # Not met? Return None.
    else:
        return None


def tied(score_A, threshold, trial_counter):
    """ Decide assuming that score_A and score_B are tied such
    that score_A = 1 - score_B.  As they are tied we only need score_A.
    
    Note: this would give equivilant results if score_A and score_B were
    run through absolute() instead, but is made explicit for clarity
    and readablity.
    """

    # Is the threshold met of exceeded?
    if score_A >= threshold:
        return _result_return(score_A, (1-score_A), trial_counter)
    elif (1-score_A) >= threshold:
        return _result_return((1-score_A), score_A), trial_counter)
    # Not met, Return None.
    else:
        return None


