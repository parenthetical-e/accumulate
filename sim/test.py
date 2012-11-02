""" Top-level control for test/experimental functions. """
import pprint
from accumulate.sim.base import Trials
from accumulate.stats import divergence, divergence_by_trial, correct, reaction_time_difference, mean_rt
from accumulate.models import models, construct
from accumulate.sim.results import tabulate


def simple_run(l, threshold):

    # All (?) models names are:
    # Construct models with params
    # TODO
    
    # Take the constructed models, and any param free models
    # add them all the the list of models to run, i.e. to 
    # use to categorize the trials in Trials.
    run_models = [models.information, models.likelihood_ratio, models.abscount, 
            models.relcount, models.naive_probability ]  
                ## TODO add constructed.

    # Create the experimental instance
    exp = Trials(l)
    result = exp.categorize(run_models, threshold)

    # and analyze it.
    # stats_l = scores(res_l)
    divs = divergence_by_trial(result)
    meandivs = divergence(result)
    
    pp = pprint.PrettyPrinter(indent=4,depth=6)
    pp.pprint(result.items())
    pp.pprint(meandivs.items())

    # dists = exp.distances()
    # pp.pprint(dists)
    
    # print("Mean RTs:")
    # pp.pprint(mean_rt(result))    
    for model in run_models:
        model_name = model.__name__
        print(model_name)
        print("ACC:")
        pp.pprint(correct(model_name, result))
    #     print("Delta RT:")
    #     pp.pprint(reaction_time_difference(model_name, result))

    tabulate('test_tab.tsv', exp, result, False)
    tabulate('test_tab_acc.tsv', exp, result, True)
    
if __name__ == "__main__":
    simple_run(8, 0.65)

