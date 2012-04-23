""" 
A module to calculate aggregate statistics for AccumulationExp() results.
"""
import numpy as np


def scores(result):
	"""
	Return the (average, var, SD, n) of scores for 'A' and 'B' and 'N' 
	decisions from a AccumulationExp.categorize() <result>. 
	"""
	from collections import defaultdict

	stats = defaultdict(dict)

	# Regroup the results.
	scores = defaultdict(list)
	off_scores = defaultdict(list)
	lengths = defaultdict(list)
	for r in result:
		scores[r[0]].append(r[1])
		off_scores[r[0]].append(r[2])
		lengths[r[0]].append(r[3])

	# Convert to arrays 
	# the do stats calcs
	cats = ['A','B','N']
	for c in cats:
		arr = np.array(scores[c])
		stats[c]['score'] = (arr.mean(),arr.var(),arr.std(),arr.shape[0])

		arr = np.array(off_scores[c])
		stats[c]['off_score'] = (arr.mean(),arr.var(),arr.std(),arr.shape[0])

		arr = np.array(lengths[c])
		stats[c]['length'] = (arr.mean(),arr.var(),arr.std(),arr.shape[0])

	return stats

