""" Top-level control for test/experimental functions. """
import os
import pprint
from accumulate.sim.base import Trials
from accumulate.stats import (divergence, divergence_by_trial, 
        correct, reaction_time_difference, mean_rt)
from accumulate.models import construct
from accumulate.sim.results import tabulate, combine
from accumulate.models.deciders import absolute, difference


def main(runname, l, threshold, decider):
    """ Do all the work... """

    # Setup the location the results
    # will be stored (in basedir).
    basedir = "run1"
    try:
        os.mkdir(basedir)
    except OSError:
        pass
    
    # Init the experiment
    exp = Trials(l)
    
    # Take the constructed models, and any param free models
    # add them all the the list of models to run, i.e. to 
    # use to categorize the trials in Trials.

    # ----
    # No params
    info = construct.create_information(
            "information", threshold, decider)
    lratio = construct.create_likelihood_ratio(
            "likelihood_ration", threshold, decider)
    absc = construct.create_abscount(
            "abscount", threshold, decider)
    relc = construct.create_relcount(
            "relcount", threshold, decider)
    naive = construct.create_naive_probability(
            "naive", threshold, decider)
    snr = construct.create_snr(
            "snr", threshold, decider)
    
    # ----
    # Has params
    gating1 = construct.create_urgency_gating(
            "gating_g04", threshold, decider, gain=0.4)
    lba1 = construct.create_incremental_lba(
            "lba_k01_d01", threshold, decider, k=0.1, d=0.1)
    blca1 = construct.create_blca(
            "blca_l10_k01_wi01_leak01_beta01", 
            threshold, decider, length=10, k=0.1, wi=0.1, leak=0.1, beta=0.1)

    run_models = [info, lratio, absc, relc, naive, snr, gating1, lba1, blca1]

    # Loop over each model and categorize it.
    # Then tell us what was done.
    results_list = [exp.categorize(mod) for mod in run_models]
    for model in run_models:
        print(model.__name__)
        
    # Reformat the results
    result = combine(results_list)
    
    print("Saving the results....")
    tabulate('./{0}/{1}.csv'.format(basedir, runname), exp, result, False)
    tabulate('./{0}/{1}_acc.csv'.format(basedir, runname), exp, result, True)
    
    
if __name__ == "__main__":
    # For both absolute and difference, try three lengths
    # and two thresholds
    
    # Do absolute
    main('l8_065_abs', 8, 0.65, absolute)
    main('l8_090_abs', 8, 0.90, absolute)
    # main('l14_065_abs', 14, 0.65, absolute)
    # main('l14_090_abs', 14, 0.90, absolute)
    # main('l18_065_abs', 18, 0.65, absolute)
    # main('l18_090_abs', 18, 0.90, absolute)

    # then difference
    main('l8_065_diff', 8, 0.65, difference)
    main('l8_090_diff', 8, 0.90, difference)
    # main('l14_065_diff', 14, 0.65, difference)
    # main('l14_090_diff', 14, 0.90, difference)
    # main('l18_065_diff', 18, 0.65, difference)
    # main('l18_090_diff', 18, 0.90, difference)
    
