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

    # Is the threshold met or exceed? 
    if (score_A >= threshold) or (score_B >= threshold):
        _result_return(score_A, score_B, trial_counter)
        
    # Not met? Return None.
    else:
        return None
        

def difference(score_A, score_B, threshold, trial_counter):
    """ Decide between the difference of the  scores based on <threshold>. 
    This is just a helper function, it is not always used. """
    
    diff = abs(score_A - score_B)
    
    # Is the threshold met or exceed? 
    if diff >= threshold:
        _result_return(score_A, score_B, trial_counter)

    # Not met? Return None.
    else:
        return None
