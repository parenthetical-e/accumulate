""" Top-level control for test/experimental functions. """
import pprint
from accumulate.sim.base import Trials
from accumulate.stats import (divergence, divergence_by_trial, 
        correct, reaction_time_difference, mean_rt)
from accumulate.models import construct
from accumulate.sim.results import tabulate, combine
from accumulate.models.deciders import absolute


def simple_run(l, threshold, decider):
    """ A simple test run. """

    # Take the constructed models, and any param free models
    # add them all the the list of models to run, i.e. to 
    # use to categorize the trials in Trials.
    info = construct.create_information(threshold, decider)
    lratio = construct.create_likelihood_ratio(threshold, decider)
    absc = construct.create_abscount(threshold, decider)
    relc = construct.create_relcount(threshold, decider)
    naive = construct.create_naive_probability(threshold, decider)
    # TODO - rest of models not here, 
    # but for leaky also do one with
    # comp at zero (with leak) and seperatly one 
    # with leak at 0 (with comp valued)
    
    run_models = [info, lratio, absc, relc, naive]
    # print(run_models)
    # Create the experimental instance
    exp = Trials(l)

    # Loop over each model and categorize it.
    results_list = list()
    [results_list.append(exp.categorize(mod)) for mod in run_models]
    
    # Reformat the results
    result = combine(results_list)

    # And analyze it.
    # stats_l = scores(res_l)
    # divs = divergence_by_trial(result)
    # meandivs = divergence(result)
    speeds = exp.maxspeed(0, 5)
    
    # pp = pprint.PrettyPrinter(indent=4,depth=6)
    # pp.pprint(result.items())
    # pp.pprint(meandivs.items())

    # dists = exp.distances()
    # pp.pprint(dists)
    # pp.pprint(speeds)
    
    # print("Mean RTs:")
    # pp.pprint(mean_rt(result))    
    for model in run_models:
        model_name = model.__name__
        print(model_name)
        # print("ACC:")
        # pp.pprint(correct(model_name, result))
    #     print("Delta RT:")
    #     pp.pprint(reaction_time_difference(model_name, result))

    print("Saving the results....")
    tabulate('./testdata/test_tab.csv', exp, result, False)
    tabulate('./testdata/test_tab_acc.csv', exp, result, True)
    
    
if __name__ == "__main__":
    simple_run(8, 0.65, absolute)

