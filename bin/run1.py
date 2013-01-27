""" Top-level control for test/experimental functions. """
import os
from multiprocessing import Pool
from accumulate.sim.base import Trials
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
    exp = Trials(l)
    
    # Construct the needed models
    # ----
    # No params
    info = construct.create_information(
            "information", threshold, decider)
    lratio = construct.create_likelihood_ratio(
            "likelihood_ratio", threshold, decider)
    absc = construct.create_abscount(
            "abscount", threshold, decider)
    relc = construct.create_relcount(
            "relcount", threshold, decider)
    naive = construct.create_naive_probability(
            "naive", threshold, decider)
    snr = construct.create_snr(
            "snr", threshold, decider)
    
    # ----
    # Has params:
    
    # --
    # The p_r calc is bugged, so this model was exlcuded
    # from run1...
    # * Urgency gating
    # gating1 = construct.create_urgency_gating(
            # "gating_g04", threshold, decider, gain=0.4)
    
    # --
    # * Linear balistic
    lba_k0_d006 = construct.create_incremental_lba(
            "lba_k01_d006", threshold, decider, k=0, d=0.06)            
    lba_k0_d0125 = construct.create_incremental_lba(
            "lba_k01_d0125", threshold, decider, k=0, d=0.125)
    lba_k0_d025 = construct.create_incremental_lba(
            "lba_k01_d025", threshold, decider, k=0, d=0.25)
    lba_k0_d050 = construct.create_incremental_lba(
            "lba_k01_d050", threshold, decider, k=0, d=0.50)
            
    # --    
    # * Ballistic leaky competing accumulator.
    blca1 = construct.create_blca(
            "blca_k01_wi01_leak01_beta01",
            threshold, decider, length=l, k=0, wi=0.4, leak=0.1, beta=0.1)

    
    # And put all the model in list to run that all
    run_models = [info, lratio, absc, relc, naive, snr, 
            lba_k0_d006, lba_k0_d0125, lba_k0_d025, lba_k0_d050, 
            blca1]

    # and then loop over each model and categorize it 
    # using exp().
    results_list = [exp.categorize(mod) for mod in run_models]

    # Then tell us what was done.
    for model in run_models:
        print(model.__name__)
        
    # Reformat the results so they are indexed by trial
    # (in a dict) instead of by the order they appear 
    # in run_models.
    result = combine(results_list)
    
    print("Saving the results....")
    tabulate('./{0}/{1}.csv'.format(basedir, runname), exp, result, False)
    tabulate('./{0}/{1}_acc.csv'.format(basedir, runname), exp, result, True)
    
    
if __name__ == "__main__":
    # For both absolute and difference, try three lengths
    # and a range of thresholds
    
    run_params = [
        ('l8_025_abs', 8, 0.25, absolute),
        ('l8_050_abs', 8, 0.50, absolute),
        ('l8_065_abs', 8, 0.65, absolute),
        ('l8_090_abs', 8, 0.90, absolute),
        ('l8_010_diff', 8, 0.10, difference),
        ('l8_020_diff', 8, 0.20, difference),
        ('l8_030_diff', 8, 0.30, difference),
        ('l8_050_diff', 8, 0.50, difference),
        ('l8_090_diff', 8, 0.90, difference)
        # ('l14_025_abs', 14, 0.25, absolute),
        # ('l14_050_abs', 14, 0.50, absolute),
        # ('l14_065_abs', 14, 0.65, absolute),
        # ('l14_090_abs', 14, 0.90, absolute),
        # ('l14_010_diff', 14, 0.10, difference),
        # ('l14_020_diff', 14, 0.20, difference),
        # ('l14_030_diff', 14, 0.30, difference),
        # ('l14_050_diff', 14, 0.50, difference),
        # ('l14_090_diff', 14, 0.90, difference)
        # ('l18_025_abs', 18, 0.25, absolute),
        # ('l18_050_abs', 18, 0.50, absolute),
        # ('l18_065_abs', 18, 0.65, absolute),
        # ('l18_090_abs', 18, 0.90, absolute),
        # ('l18_010_diff', 18, 0.10, difference),
        # ('l18_020_diff', 18, 0.20, difference),
        # ('l18_030_diff', 18, 0.30, difference),
        # ('l18_050_diff', 18, 0.50, difference),
        # ('l18_090_diff', 18, 0.90, difference)
    ]
    
    # Cretae a worker Pool and run run_params
    # in parallel across ncore cores
    ncore = 2
    pool = Pool(processes=ncore)
    pool.map(main, run_params)
