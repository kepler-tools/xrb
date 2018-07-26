"""
A module for handling and analyzing data produced by Kepler X-ray burst models.

The `xrb` module provides a few classes for encapsulating X-ray burst data,
analyzing that data, and if you would rather not plot it yourself, plotting that
data.
"""
#NOTE: For now, I'm just dumping all code here.  As things grow, we can discuss
#refactoring and creating new submodules and such.

from defdict import DefinedDict
from tfile import TemplateFile

# XRBData class for loading in, storing, and saving data pertinent to X-ray
# bursts.
#
# The python scripts included with Kepler already provide facilities
# for doing much of this, and we'll make use of these.  However, we still want
# this class as a way of standardizing the data we have so that our other code
# knows how to use it.  It also curates the data for X-ray burst analysis.
# Kepler's tools give you the kitchen sink and often require some understanding
# of Kepler conventions and source code.
class XRBSensData(object):
    """
    A class for loading, storing, and saving X-ray burst sensitivity data.
    """

    #TODO: Add Parameters and Examples sections to docstring when ready.
    def __init__(self, grid_label, grid_desc):
        """
        Initialize a minimal XRBSensData with mostly empty data.

        Only a label and description of the grid is required.  Use print_fields() to
        see the set of fields defined for the grid.
        """
        self._grid_data = self._initGridDict()
        self._grid_data['grid_label'] = grid_label
        self._grid_data['grid_desc']  = grid_desc

    def _initGridDict(self):
        """Initialize a DefinedDict describing grid data."""
        from collections import OrderedDict
        field_descriptions = OrderedDict({
            'grid_label': 'Label for the grid, should be a valid filename' +
                          'as it will be used in creating directory structures.',
            'grid_desc': 'Brief description of the grid',
            'x': 'Accreted hydrogen mass fraction',
            'z': 'Accreted metallicity mass fraction, all as X_n14',
            'qb': 'Base heating in MeV/nucleon, models energy released at' +
                  'base per accreted nucleon',
            'eddf': 'Eddington fraction, expresses accretion rate as a ' +
                    'fraction of the Eddington accretion rate',
            'xi': 'A factor that scales the accretion rate, was introduced ' +
                  'to capture anisotropy effects',
            'acc_lum': 'The luminosity generated at the base in response ' +
                       'to accretion, given in erg/s',
            'acc_rate': 'Accretion rate in M_sol / yr',
            'gee': 'Surface gravity of the model in cm / s^2',
            'vary_list': "array of tuples ('rxn_label', scale_fac), one for each variation in the grid",
            'model_data': "Mapping (dict) of model labels to DefinedDicts of model data."})
        init_dict = dict.fromkeys(field_descriptions.keys())
        return DefinedDict(init_dict, field_descriptions)

    def print_fields(self):
        """Print the fields and their descriptions."""
        print(self._grid_data.fields_str())

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
