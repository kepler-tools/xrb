"""
A module for handling and analyzing data produced by Kepler X-ray burst models.

The `xrb` module provides a few classes for encapsulating X-ray burst data,
analyzing that data, and if you would rather not plot it yourself, plotting that
data.
"""
#NOTE: For now, I'm just dumping all code here.  As things grow, we can discuss
#refactoring and creating new submodules and such.

# XRBData class for loading in, storing, and saving data pertinent to X-ray
# bursts.  
#
# The python scripts included with Kepler already provide facilities
# for doing much of this, and we'll make use of these.  However, we still want
# this class as a way of standardizing the data we have so that our other code
# knows how to use it.  It also curates the data for X-ray burst analysis.
# Kepler's tools give you the kitchen sink and often require some understanding
# of Kepler conventions and source code.
class XRBData(object):
    """
    A class for loading, storing, and saving X-ray burst data.
    """
    #TODO: Add Parameters and Examples sections to docstring when ready.
    pass

class XRBAnalysis(object):
    """
    A class for performing analysis on XRBData.
    """
    pass
    
class XRBPlot(object):
    """
    A class for plotting X-ray burst data.
    """
    pass

if __name__ == "__main__":
    """
    Any driver, debug code goes here. Tests should use the testing framework.
    """
    pass
