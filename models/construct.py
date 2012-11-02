from accumulate.models.models import abscount


def lba(self, trial, threshold):
    pass 
    # TODO


def create_first_n(n):
    """ 
    Use count() and only the last <n> exemplars to make the 
    decision on <trial>.  Params should contain <n>.
    """
    
    def first_n(trial, threshold):
        return abscount(self, trial[0:n], threshold)
        
    return first_n


def create_last_n(n):
    """ 
    Use count() and only the first <n> exemplars to make the 
    decision on <trial>.  Params should contain <n>.
    """
    
    def last_n(trial, threshold):
        return abscount(self, trial[-n:], threshold)
        
    return last_n

