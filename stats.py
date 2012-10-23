""" 
A module to calculate aggregate statistics for AccumulationExp() results.
"""
from collections import defaultdict


def correct(correct_model, model_results):
    """ 
    Given a <correct_model>, how accurate are the remaining <model_names>
    in <model_results>.
    """

    # Count how many times each model was right
    # and wrong campared to <correct_model>
    accuracy_counter = defaultdict(int)

    # Loop over each trial:
    for trial_results in model_results.values():
        correct_answer = trial_results[correct_model][0]
        for name, result in trial_results.items():
            # Don't consider the correct_model
            # when averaging; it is always 1.
            if name == correct_model:
                continue

            # This model's name's answer is:
            answer = result[0]

            # Is it right? Increment or decrement as
            # is appropriate
            if (answer != "N") and (correct_answer != 'N'):
                if answer == correct_answer:
                    accuracy_counter[name] += 1
                else:
                    accuracy_counter[name] -= 1

    # Now calculate the mean accuracy
    # for every model,
    num_trials = float(len(model_results))
    accuracy = dict()
    for name, count in accuracy_counter.items():
        accuracy[name] = count / num_trials

    # and return it
    return accuracy


def reaction_time_difference(correct_model, model_results):
    """ Calculate the mean 'reaction time' differences, comparing 
    the <correct_model> to the rest of the <model_results>. """

    # Calculate the mean rt difference between the correct_model
    # the all the others in model_results
    rt_diff = defaultdict(float)

    # Loop over each trial:
    for trial_results in model_results.values():
        correct_rt = trial_results[correct_model][3]
        for name, result in trial_results.items():
            # Don't consider the correct_model
            # when averaging; it is always 1.
            if name == correct_model:
                continue

            # This model's name's rt is:
            rt = result[3]

            # If both rts aren't None
            # calculate online the rt difference
            if (rt != None) and (correct_rt != None):
                diff = rt - correct_rt
                rt_diff[name] = (rt_diff[name] + diff) / 2.0
                    ## old + new / 2 in the online mean...

    return rt_diff


def divergence(model_results):
    """ For <model_names> in <model_results> find where the models diverge
    in their predictions.  Consider all possible pairs. """

    divergent = dict()  ## To store divergent models
                        ## as: divergent[name][model][...]
                        ## where ... is D, T, or DT

    for trial, models_data in model_results.items():
        divergent[trial] = dict() 
        for name, result in models_data.items():
            divergent[trial][name] = {'D':list(), 'T':list(), 
                    'DT':list()}
                ## and divergent is fully intialized...

            # Compare name to all the other names/models
            for name_compare, result_compare in models_data.items():
                # Don't check the same names though.
                if name == name_compare:
                    continue

                # Rename result, for brevity.
                r = result
                rc = result_compare
                
                # Check decision,
                if r[0] != rc[0]:
                    divergent[trial][name]['D'].append(name_compare)
                
                # then time only,
                if (r[0] == rc[0]) and (r[3] != rc[3]):
                    divergent[trial][name]['T'].append(name_compare)
                
                # and time and decision go last.
                if (r[0] != rc[0]) and (r[3] != rc[3]):
                    divergent[trial][name]['DT'].append(name_compare)
    
    return divergent

