""" A submodule for processing/exporting results from Trials. """

import csv
from collections import defaultdict
from accumulate.stats import correct

# TODO test
def combine(results_list):
    """ Combine results by trial. """
    
    trials = results_list[0].keys()
    combined = defaultdict(dict)
    for trial in trials:
        for res in results_list:
            mod, data = res[trial].items()[0]
            combined[trial][mod] = data
    
    return combined


def tabulate(filename, trials, model_results, include_acc):
    """ Use the Trials instance <trials> and the <model_results> from
    a call of trials.categorize() to generate a tabulated (csv) set of trial
    level results and meta-data suitable for import into another analysis
    package, e.g. R. 
    
    The format mirrors a data.table in R. """

    # Open and prep the csv filehandle,
    # write the header info too
    fid = open(filename, 'w')
    writer = csv.writer(fid, delimiter=',')

    header = ["trial", "model", "decision", "score", "altscore", "rt",
        "distance", "countA", "countB", "maxcount", 
        "maxspeed_front", "maxspeed_back"]
    
    if include_acc:
        header = header + ["correct_model", "acc"]
    
    writer.writerow(header)
    
    # Extract meta-data from trials
    distances = trials.distances()
    counts = trials.counts()
    l = int(trials.l)
    maxspeed_front = trials.maxspeed(0, l/2-1)
    maxspeed_back = trials.maxspeed(l/2, l)

    # HOW TO LOOP OVER IT ALL SENSIBLY?
    all_trials = model_results.keys()
    all_models = model_results[all_trials[0]].keys()
    for trial in all_trials:
        for model in all_models:
            data = model_results[trial][model]
            row_part_1 = [
                    trial,
                    model,
                    data['decision'],
                    data['chosen_score'],
                    data['unchosen_score'],
                    data['rt'],
                    distances[trial],
                    counts[trial][0],
                    counts[trial][1],
                    max(counts[trial][0], counts[trial][1]),
                    maxspeed_front[trial],
                    maxspeed_back[trial]
                    ]
            if include_acc:
                acc = correct(model, model_results)
                for alt_model, acc in acc[trial].items():
                    row_part_2 = [alt_model, acc]
                    writer.writerow(row_part_1 + row_part_2)
            else:
                writer.writerow(row_part_1)

    # Clean up            
    fid.close()

