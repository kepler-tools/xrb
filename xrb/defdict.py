from collections.abc import Mapping, MutableMapping
# This is my stab at a class I've been wanted for a long while: DefinedDict.
#
# DefinedDict is a restricted variation on Python's dict.  It has a defined set
# of keys/fields that is established on creation and cannot be changed
# afterward.  However, the data the keys point to CAN be updated.  I subclass
# Mapping instead of MutableMapping because MM suggests the ability to add,
# change, remove keys, which I don't want to do.
#
# In developing this and discussing with others, I've come across possible
# alternatives to writing your own class.  None quite gave me what I wanted, but
# for reference check out: `attrs`, `recordclass`, and the new builtin
# dataclasses.  The issues with these include: not quite achieving what I want,
# introducing dependencies without enough of a payoff, and/or requiring as much
# effort to achieve what I want as writing DefinedDict.
#
# TODO: use that __hasattr__ to make mydefdict['key'] and mydefdict.key both
# work?
#
# TODO: __slots__ is a magic that signals a fixed set of attributes will be
# used, instead of the usual __dict__ that allows for adding an arbitrary
# number of attributes and implies a decent amount of overhead.  If this class
# proves a good case, might use this instead to be more memory efficient.
# Mapping may already implement this for us.
#
# Python's documentation and source provides useful info on implementing
# containers, though sadly not a single StackOverflow answer pointed to these
# docs.  I stumbled upon them after much frustration.
# See S 3.3.7 of:
# https://docs.python.org/3/reference/datamodel.html#objects
# In addition, see the source of UserDict, Mapping, MutableMapping. _Environ in
# os module is an example of a MutableMapping implementation.
#
# Recommended methods to implement (* provided by MutableMapping (** abstract)):
#   **keys(), *values(), *items(), *get(), clear(), setdefault(), pop(), popitem(),
#   copy(), and update()
#   __*contains__(), **__iter__(), **__len__(), **__getitem__(),__missing__(),
#   **__setitem__(), **__delitem__(), __repr__(), __str__(), __format__()
#
# Some details on some methods:
#object.__getitem__(self, key)
#Called to implement evaluation of self[key]. [negative keys handled by __getitem__()]. 
#   If key is of an inappropriate type, TypeError may be raised; if of a value outside the set of indexes for the sequence (after any special interpretation of negative values), IndexError should be raised. 
#   For mapping types, if key is missing (not in the container), KeyError should be raised.
#
#   Note for loops expect that an IndexError will be raised for illegal indexes to allow proper detection of the end of the sequence.
#
#object.__missing__(self, key)
#Called by dict.__getitem__() to implement self[key] for dict subclasses when key is not in the dictionary.
#
#object.__setitem__(self, key, value)
#Called to implement assignment to self[key]. Same note as for __getitem__(). 
#This should only be implemented for mappings if the objects support changes to the values for keys, or if new keys can be added, or for sequences if elements can be replaced. 
#The same exceptions should be raised for improper key values as for the __getitem__() method.
#
#object.__delitem__(self, key)
#Called to implement deletion of self[key]. Same note as for __getitem__(). 
#This should only be implemented for mappings if the objects support removal of keys, or for sequences if elements can be removed from the sequence. 
#The same exceptions should be raised for improper key values as for the __getitem__() method.
#
#object.__iter__(self)
#This method is called when an iterator is required for a container. This method should return a new iterator object that can iterate over all the objects in the container. For mappings, it should iterate over the keys of the container.
#
#The membership test operators (in and not in) are normally implemented as an iteration through a sequence. However, container objects can supply the following special method with a more efficient implementation, which also does not require the object be a sequence.
#
#object.__contains__(self, item)
#Called to implement membership test operators. Should return true if item is in self, false otherwise. 
#For mapping objects, this should consider the keys of the mapping rather than the values or the key-item pairs.
#
#For objects that don’t define __contains__(), the membership test first tries iteration via __iter__(), then the old sequence iteration protocol via __getitem__(), see this section in the language reference.
#
# 
# NOTE: Implementation strategy, start with what Mapping gives, take what you
# need from MutableMapping, UserDict
#
# TODO: Implement type hinting for dict items?
# TODO: Enforce key to be string?
class DefinedDict(Mapping):
    """
    A dict-like object which has a restricted set of keys/fields defined on
    creation, each of which includes a human-readable description of the key
    similar to a docstring.
    """

    def __init__(self, init_dict, desc_map):
        """
        DefinedDict(D, desc)
            D: dictionary to initialize DefinedDict with.
            desc: mapping of D's keys to human-readable strings describing each key

        Example:
            D = {'field1': 1, 'field2': 2}
            desc = {'field1': 'The first field, an integer.',
                    'field2': 'The second field, an integer.'}
            mydd = DefinedDict(D,desc)

            f1 = mydd['field1']  # Works
            mydd['field3'] = f1  # Raises KeyError
            mydd['field2'] = f1  # Works
            mydd.desc('field2')  # Prints 'The second field, an integer.'
        """
        #NOTE: key private attributes are:
        #self._data = {} The underlying data dictionary
        #self._desc = {} A mapping of keys from _data to descriptions
        #self._fields = frozenset() Immutable set of the keys for both desc and data.
        #   This is included because the keys() sets for either _data or _desc
        #   can be changed without raising errors. This set provides an
        #   immutable reference for ~O(1) lookups to verify fields.  __init__
        #   guarantees _fields == _desc.keys() == _data.keys()
        self._data = {}

        #Define the fields, must be done before __setitem__ can work.
        if isinstance(desc_map, Mapping):
            for key in desc_map:
                if key not in init_dict:
                    error_message = "keys of init_dict and desc_map don't match"
                    raise KeyError(error_message)
            #TODO: Check that desc_map is all strings, and if copy() should be
            #      guaranteed for mappings
            self._fields = frozenset(desc_map.keys())
            if not (self._fields == set(desc_map.keys()) == set(init_dict.keys())):
                raise ValueError('init_dict and desc_map do not have the same keys!')
            self._desc = desc_map.copy()
        else:
            error_message = "desc_map is not a Mapping: {}".format(desc_map)
            raise TypeError(error_message)

        #Initialize the local dict, borrowing practices from MutableMapping update()
        if isinstance(init_dict, Mapping):
            for key in init_dict:
                self[key] = init_dict[key]
        elif hasattr(init_dict, "keys"):
            for key in init_dict.keys():
                self[key] = init_dict[key]
        else:
            for key, value in init_dict:
                self[key] = value

    def desc(self, key):
        """Get a string describing `key`."""
        if key not in self._fields:
            raise KeyError(key)
        return self._desc[key]

    def fields_str(self):
        """Get a string listing and describing all fields."""
        return self.__str__(verbose=False)

    #TODO: setdefault(), copy(), deepcopy()

    ## magic methods
    ## the key methods required by Mapping:
    # __getitem__ __iter__, __len__
    def __getitem__(self, key):
        if key in self._fields:
            #TODO: this will raise KeyError if somehow key not in _data, should
            #do a try except?
            return self._data[key]
        else:
            raise KeyError(
                  '`{}` is not a valid field in this DefinedDict'.format(key))

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    ## abstract MutableMapping methods and dict methods to consider
    #  __setitem__ __delitem__ __add__ __eq__ __ne__ keys() 
    #  __contains__ (esp if I ever need to deal with __missing__ protocols, see UserDict)
    def __setitem__(self, key, value):
        if key in self._fields:
            self._data[key] = value
        else:
            raise KeyError(
                  '"{}" is not a valid field in this DefinedDict'.format(key))

    def __delitem__(self, key):
        raise TypeError('DefinedDict fields (keys) are immutable, cannot be deleted')

    ## object magics
    # Potentially useful class dunders
    #__init,str,repr,getattr,setattr,delattr()__
    def __str__(self, verbose=True):
        field_str = '{} - {}'
        join_str = '\n'
        if verbose:
            #If verbose, include data and separate fields with ---
            field_str += '\n    {}'
            join_str += '---\n'
        ret_str = "DefinedDict class instance\n{}".format(
            join_str.join(
                (field_str.format(field, self._desc[field], self._data[field])
                for field in self._desc)))
        return ret_str

    #TODO: __repr__, which as much as possible should be valid Python code that
    #   could be used to recreate the instance.

