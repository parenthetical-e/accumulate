""" A submodule for processing/exporting results from Trials. """

import csv
from accumulate.stats import correct

# TODO test
def combine(results_list):
    """ Combine results by trial. """
    
    trials = results_list[0].keys()
    combined = defaultdict(dict)
    for trial in trials:
        for res in results_list:
            mod, data = res[trial].items()
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
    
    if include_acc:
        header = ["trial", "model", "decision", "score", "altscore", "rt",
                "distance", "countA", "correct_model", "acc"]
    else:
        header = ["trial", "model", "decision", "score", "altscore", "rt",
                "distance", "countA"]
    
    writer.writerow(header)
    
    # Extract meta-data from trials
    distances = trials.distances()
    counts = trials.counts()

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
                    counts[trial][0]
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
