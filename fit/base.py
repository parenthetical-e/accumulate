""" A subclass for fitting category decision models to behavioral data. """
from accumulate.sim.base import AccumulationExp

class AccumulateModelFit(AccumulationExp):
	def __init__(self):
		AccumulationExp.__init__(self)

	# TODO - way to add behave data (in same format as self.trials)
	# Optimizaiton routines for fitting params for the various models.
	pass

