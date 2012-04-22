This module allows for simulation, analysis and plotting of 2 choice accumulated category designs.  

There are two possible experimental design classes.

	AccumulationExp()

and 
	
	FractionAccumalationExp()

The first simulates all possible designs of length l, under a variety of category decision criteria (below).  The second simulates only those trials whose fraction of As or Bs exceeds some given threshold.  Other than this difference though each has the same methods and capabilities.

A simple use case (run inside ipython):

	import accumulate

Let us consider trials with a max length of 4.  This is shorter than you'll want in practice but allows for easy visualization of the results.  Also, to simplfy implementation l must be even.

First create an exhaustive experiment.  AccumulationExp() takes one argument, the max trial length, l.
	
	exp1 = accumulate.base.AccumulationExp(l)
		
So what do we have?  All possible trial designs live in trials.

	exp1.trials

So first we will assume that the participant makes decisions by counting the number of category A and B examplars, and if that count excceds some threshold (modeled here as a fraction of l) then makes a decision.  

First assume they're in hurry and only wait for a 60% threshold.

	d_fast = exp1.categorize(decide='count',threshold=0.6)

TODO: EXPLAIN d_fast, analysis too.

Now let us compare that to a more patient ideal participant (who is coincidentally wanting statistical significance).

	d_slow = exp1.categorize(decide='count',threshold=0.95)

