""" 
A module to calculate aggregate statistics for AccumulationExp() results.
"""
from collections import defaultdict

def correct_trial(trial, correct_model, model_results):
    """ 
    Given a <correct_model>, how accurate are the remaining <model_names>
    in <model_results> for the given <trial>.
    """
    
    acc = dict()
    
    trial_results = model_results[trial]
    correct_answer = trial_results[correct_model]['decision']
    
    for alt_model, result in trial_results.items():
        # Don't consider the correct_model
        # when averaging; it is always 1.
        if alt_model == correct_model:
            continue

        # This model's name's answer is:
        answer = result['decision']            
        if (answer == correct_answer) and (correct_answer != 'N'):
            acc.update({alt_model : 1})
        elif (answer == correct_answer) and (correct_answer == 'N'):
            acc.update({alt_model : -1})
                ## Correct Ns as -1
        else:
            acc.update({alt_model : 0})
        
    return acc


def correct(correct_model, model_results):
    """ 
    Given a <correct_model>, how accurate are the remaining <model_names>
    in <model_results>.
    """

    # Count how many times each model was right
    # and wrong campared to <correct_model>
    acc = defaultdict(dict)
    
    # Loop over each trial:
    for trial, trial_results in model_results.items():
        correct_answer = trial_results[correct_model]['decision']
        for alt_model, result in trial_results.items():
            # Don't consider the correct_model
            # when averaging; it is always 1.
            if alt_model == correct_model:
                continue

            # This model's name's answer is:
            answer = result['decision']            
            if (answer == correct_answer) and (correct_answer != 'N'):
                acc[trial].update({alt_model : 1})
            elif (answer == correct_answer) and (correct_answer == 'N'):
                acc[trial].update({alt_model : -1})
                    ## Correct Ns as -1
            else:
                acc[trial].update({alt_model : 0})

    # and return it
    return acc


def mean_rt(model_results):
    """ Return the average reaction time for each model in 
    <model_results>. """
    
    # Init
    mrt = dict()
    
    # Loop over the results average (online) the rts
    # for each model, or if that fails (KeyError)
    # initialize instead.  Ignore Nones.
    for trial_results in model_results.values():
        for name, result in trial_results.items():
            rt = result['rt']
            if rt != None:
                try:
                    mrt[name] = (mrt[name] + rt) / 2.0
                        ## mean!
                except KeyError:
                    mrt[name] = float(rt)
                        ## Init, force type
    return mrt
    
    
def reaction_time_difference(correct_model, model_results):
    """ Calculate the mean 'reaction time' differences, comparing 
    the <correct_model> to the rest of the <model_results>. """

    meanrt = mean_rt(model_results)
    correct_rt = meanrt[correct_model]
    
    rt_diff = dict()
    for name, rt in meanrt.items():
        if name == correct_model:
            continue
        
        rt_diff[name] =  rt - correct_rt
            ## Want a signed value here:
            ## If rt is less, the time difference
            ## is positive, and the reverse.
        
    return rt_diff


def divergence_by_trial(model_results):
    """ For <model_names> in <model_results> find where the models diverge
    in their predictions.  Consider all possible pairs. """

    divergent = dict()  ## To store divergent models
                        ## as: divergent[name][model][...]
                        ## where ... is D, T, or DT

    for trial, models_data in model_results.items():
        divergent[trial] = dict()
        for name, result in models_data.items():
            divergent[trial][name] = {'D' : 0, 'T' : 0, 'DT' : 0}
                ## and divergent is fully intialized...
            
            num_models = float(len(models_data))
            # Compare name to all the other names/models
            for name_compare, result_compare in models_data.items():
                # Don't check the same names though.
                if name == name_compare:
                    continue

                # Rename result, for brevity.
                r = result
                rc = result_compare
                
                # Check decision,
                if r['decision'] != rc['decision']:
                    divergent[trial][name]['D'] += 1 / num_models
                
                # then time only,
                if (r['decision'] == rc['decision']) and (r['rt'] != rc['rt']):
                    divergent[trial][name]['T'] += 1 / num_models
                
                # and time and decision go last.
                if (r['decision'] != rc['decision']) and (r['rt'] != rc['rt']):
                    divergent[trial][name]['DT'] += 1 / num_models
    
    return divergent


def divergence(model_results):
    """ Return the average divergence measures for each model in 
    <model_results. """

    # Make a copy of model_results, so we can pop off
    # of it safely, initializing mean_div.
    divs = divergence_by_trial(model_results)
    mean_div = dict()
    trial, mean_div = divs.popitem()
        ## Init by pop

    # Loop over divs, averaging each divergence measure
    for trial, model_data in divs.items():
        for model, divs in model_data.items():
            mean_div[model]['D'] = (mean_div[model]['D'] + divs['D']) / 2.
            mean_div[model]['T'] = (mean_div[model]['T'] + divs['T']) / 2.
            mean_div[model]['DT'] = (mean_div[model]['DT'] + divs['DT']) / 2.
            

    return mean_div

