"""
A module for handling and analyzing data produced by Kepler X-ray burst models.

The `xrb` module provides a few classes for encapsulating X-ray burst data,
analyzing that data, and if you would rather not plot it yourself, plotting that
data.
"""
#NOTE: For now, I'm just dumping all code here.  As things grow, we can discuss
#refactoring and creating new submodules and such.

from collections.abd import Mapping
# This is my stab at a class I've been wanted for a long while: DefinedDict.  My
# intuition is that something must already exist that does this, but I just
# can't find it/figure it out, so I'm trying to make it on my own.  If it works,
# I'll move it out of this project into something stand-alone, as I want it for
# multiple projects.
#
# DefinedDict is a restricted variation on Python's dict.  It has a defined set
# of keys/fields that is established on creation and cannot be changed
# afterward.  However, the data the keys point to CAN be updated, changed.  I
# could make a class, but by subclassing Mapping I get lots of stuff (including
# dict-like syntax) and performance for free.  I subclass Mapping instead of
# MutableMapping because MM suggests the ability to add, change, remove keys,
# which I don't want.
class DefinedDict(Mapping):
    pass

#Do I want/need this? Leaving here for reference for now.
#DefinedDict.register(dict)

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
