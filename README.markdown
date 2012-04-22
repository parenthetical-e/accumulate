This module allows for simulation and analysis of 2 choice accumulated category experimental designs.

# Preliminaries

A/B coding. exmpalars bieng irrelavant. ?

# Introduction

There are two possible experimental design classes.

	AccumulationExp()

and 
	
	FractionAccumalationExp()

The first simulates all possible designs of length *l*, under a variety of category decision criteria (below).  The second simulates only those trials whose fraction of As or Bs exceeds some given threshold.  Other than this difference though each has the same methods and capabilities.

# A simple use case (run inside ipython):

So bring in the module...

	import accumulate

Now we can do some work...

Let us consider trials with a max length of 4.  This is shorter than you'll want in practice but allows for easy visualization of the results.  Also, to simplfy implementation *l* must be even.

First create an exhaustive experiment.  AccumulationExp() takes one argument, the max trial length, *l*.
	
	exp1 = accumulate.base.AccumulationExp(l)
		
So what do we have?  All possible trial designs live in trials.

	exp1.trials

Is....

	[('A', 'A', 'A', 'A'),
	 ('A', 'A', 'A', 'B'),
	 ('A', 'A', 'B', 'A'),
	 ('A', 'A', 'B', 'B'),
	 ('A', 'B', 'A', 'A'),
	 ('A', 'B', 'A', 'B'),
	 ('A', 'B', 'B', 'A'),
	 ('A', 'B', 'B', 'B'),
	 ('B', 'A', 'A', 'A'),
	 ('B', 'A', 'A', 'B'),
	 ('B', 'A', 'B', 'A'),
	 ('B', 'A', 'B', 'B'),
	 ('B', 'B', 'A', 'A'),
	 ('B', 'B', 'A', 'B'),
	 ('B', 'B', 'B', 'A'),
	 ('B', 'B', 'B', 'B')]

So first we will assume that the participant makes decisions by counting the number of category A and B examplars, and if that count excceds some threshold (modeled here as a fraction of l) then makes a decision.  

First assume they're in hurry and only wait for a 60% threshold.

	d_fast = exp1.categorize(decide='count',threshold=0.6)

d_fast is:

	[('A', 0.75, 0.0, 3),
	 ('A', 0.75, 0.0, 3),
	 ('A', 0.75, 0.25, 4),
	 ('N', -1, -1, -1),
	 ('A', 0.75, 0.25, 4),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('B', 0.75, 0.25, 4),
	 ('A', 0.75, 0.25, 4),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('B', 0.75, 0.25, 4),
	 ('N', -1, -1, -1),
	 ('B', 0.75, 0.25, 4),
	 ('B', 0.75, 0.0, 3),
	 ('B', 0.75, 0.0, 3)]

Each set of paranthesis is 
	
	(decision, score for that decision, score for the unchosen option, how many exemplars were experienced until decision was made)

'N' trials had no decsion (-1 in these models means None of NA)

Now let us compare that to a more patient ideal participant (who is coincidentally wanting statistical significance).

	d_slow = exp1.categorize(decide='count',threshold=0.95)

d_slow is:

	[('A', 1.0, 0.0, 4),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('N', -1, -1, -1),
	 ('B', 1.0, 0.0, 4)]

 Bieng so careful they only could reach a decision on the 2 completly A and B trials....

 
# More on decision models

 The other decision models are 'likelihood', 'bayes', 'drift', 'last', and 'drift'.

 1. 'count' see above

 2. 'likelihood':  you can think of this as the scantron strategy.  In it we assume the Ss is mostly senstiive to local probability changes. It calculates the probability of the number of As (or Bs) in row.  When the probability excceds threshold, a decision is made. For example:

 *p* begins at 0.5.  Assume we had an A to sart. If examplar 2 is A, *p* becomes 0.25.  If examplar 2 is A, *p* is 0.12.  So if the threshold was 0.7 it would the subject would have decided on examplar 2, and it is was 0.8, 3 would have done it. And so on....

 3. 'bayes' TODO

 4. 'drift' is very similar to count, except each examplar's wieght is modulated by a parameter (*w*).  If w = 1, these two are identical.

 5. 'last' is the idiot's guess.  It models the case where the Ss waits till the end of the trial the guesses whaever the last examplar was.

# A couple more things, some extras.

To get the total (A,B) counts for all trials do:

	exp1.counts()

Which for l = 4 is:

	[(4, 0),
	 (3, 1),
	 (3, 1),
	 (2, 2),
	 (3, 1),
	 (2, 2),
	 (2, 2),
	 (1, 3),
	 (3, 1),
	 (2, 2),
	 (2, 2),
	 (1, 3),
	 (2, 2),
	 (1, 3),
	 (1, 3),
	 (0, 4)]

Finally in on order to asses overall trial difficulty I implemented a function that returns the Hamming Distance (http://en.wikipedia.org/wiki/Hamming_distance) between each trail and the two 'undecidable' trials.

'Undecidable' trials for l = 4 are A,B,A,B and B,A,B,A.

Thus this distance measure allows you to quantify the objective difficulty of the whole trial, where as the lengths until each decision criterion give 'local' (intra-trial) difficulty estimates.

P.S. 'Undecidable' isn't true for all strategies (e.g. 'last' above), but is the most dificult possible for all strategies.  It is an imperfect term nut still I think a good reference.

Distance by example (l=4).

	exp1.distances()

Gave

	[2, 1, 1, 2, 1, 0, 2, 1, 1, 2, 0, 1, 2, 1, 1, 2]

Smaller numbers mean harder trials; smaller means closer to undecidable.
