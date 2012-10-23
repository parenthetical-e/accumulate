""" Top-level control for test/experimental functions. """
import pprint
from accumulate.sim.base import Exp
from accumulate.stats import divergence, correct, reaction_time_difference

def simple_run(l, threshold):

    # All (?) models names are:
    # model_names = ["information", "likelihood_ratio", "count", 
            # "bayes", "naive_probability", "first_n", "last_n"]

    model_names = ["count", "likelihood_ratio", "information"]
    # The experimental parameters
    params = {'n' : 5}

    # Create the experimental instance
    exp = Exp(l)
    result = exp.categorize(model_names, threshold, params)

    # # and analyze it.
    # stats_l = scores(res_l)
    divs = divergence(result)

    pp = pprint.PrettyPrinter(indent=4,depth=6)
    pp.pprint(result.items())
    pp.pprint(divs.items())

    # correct_model = 'count'
    # pp.pprint(correct(correct_model, result))
#    pp.pprint(reaction_time_difference(correct_model, result))


if __name__ == "__main__":
    simple_run(8, 0.65)
