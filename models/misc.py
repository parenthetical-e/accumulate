""" Helper or miscellaneous functions for (accumulate) models. """


class update_name():
    """ A decorator that renames __name__ of model (a function) to <name>. 
    
    Use:
    ----
    @update_name("new_better_name")
    def model(trial):
        pass
    
    >>> model.__name__()
    new_better_name
    """
    
    def __init__(self, name):
        self.name = name
    
    def __call__(self, model):
        model.__name__ = self.name

        return model


def check_threshold(threshold):
    """ Checks the threshold is in bound. """

    # Threshold is valid?
    if threshold >= 1 or threshold <= 0:
        raise ValueError('<threshold> must be between 0 - 1.')

