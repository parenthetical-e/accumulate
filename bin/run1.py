""" Top-level control for test/experimental functions. """
import os
from multiprocessing import Pool
from accumulate.sim.base import Trials
from accumulate.sim.test import SelectTrials
from accumulate.stats import (divergence, divergence_by_trial, 
        correct, reaction_time_difference, mean_rt)
from accumulate.models import construct
from accumulate.sim.results import tabulate, combine
from accumulate.models.deciders import absolute, difference


def main(params):
    """ Do all the work... """
    
    # Process args...
    runname = params[0]
    l = params[1]
    threshold = params[2]
    decider = params[3]
    
    print(runname)  ## ...To monitor progress
    
    # Setup the location the results
    # will be stored (in basedir).
    basedir = "run1"
    try:
        os.mkdir(basedir)
    except OSError:
        pass
    
    # Init the experiment
    exp = SelectTrials(l)
    
    # Construct the needed models
    # ----
    # No params
    # All the models to run go in models
    models = [
        construct.create_information("information", threshold, decider),
        construct.create_likelihood_ratio("likelihood_ratio", threshold, decider),
        construct.create_abscount("abscount", threshold, decider),
        construct.create_relcount("relcount", threshold, decider),
        construct.create_naive_probability("naive", threshold, decider),
    ]
    # ----
    # Has params:
    
    # --
    # SNR with and without the mean default
    models.append(construct.create_snr("snr", threshold, decider, False))
    models.append(construct.create_snr(
            "snr_meandefault", threshold, decider, True))
    
    # --
    # The p_r calc is bugged, so this model was exlcuded
    # from run1...
    # * Urgency gating:
    # models.append(construct.create_urgency_gating(
            # "urgency_gating_g04", threshold, decider, gain=0.4))
    
    # --
    # * Linear balistic
    ds = [0.06, 0.125, 0.25, 0.5]
    for d in ds:
        model_name = "lba_k0_d{0}".format(d)
        models.append(construct.create_incremental_lba(
                model_name, threshold, decider, k=0, d=d))
    
    # --
    # * Ballistic leaky competing accumulator.
    wis = [0.06, 0.125, 0.25]
    leaks = [0.2, 0.2, 0]
    betas = [0.1, 0, 0.1]
    for wi in wis:
        for leak, beta in zip(leaks, betas):
            model_name = "blca_k0_wi{0}_leak{1}_beta{2}".format(wi, leak, beta)
            models.append(
                    construct.create_blca(model_name, threshold, decider, 
                    length=l, k=0, wi=wi, leak=leak, beta=beta))
    
    # ----
    # Loop over each model and categorize it 
    results_list = [exp.categorize(mod) for mod in models]

    # Then tell us what was done.
    for model in models:
        print(model.__name__)
    
    # Reformat the results so they are indexed by trial
    # (in a dict) instead of by the order they appear 
    # in models.
    result = combine(results_list)
    
    print("Saving the results....")
    tabulate('./{0}/{1}.csv'.format(basedir, runname), exp, result, False)
    tabulate('./{0}/{1}_acc.csv'.format(basedir, runname), exp, result, True)
    
    
if __name__ == "__main__":
    # For both absolute and difference, try three lengths
    # and a range of thresholds
    
    run_params = [
        ('l8_051_abs', 8, 0.51, absolute),
        ('l8_065_abs', 8, 0.65, absolute),
        ('l8_090_abs', 8, 0.90, absolute)
        # ('l14_051_abs', 14, 0.51, absolute),
        # ('l14_065_abs', 14, 0.65, absolute),
        # ('l14_090_abs', 14, 0.90, absolute),
        # ('l18_051_abs', 18, 0.51, absolute),
        # ('l18_065_abs', 18, 0.65, absolute),
        # ('l18_090_abs', 18, 0.90, absolute)
    ]
    
    # Cretae a worker Pool and run run_params
    # in parallel across ncore cores
    ncore = 2  ## TODO set to 9 on Cal
    pool = Pool(processes=ncore)
    map(main, run_params)
