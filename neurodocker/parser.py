"""Class to parse specifications for Dockerfile."""
# Author: Jakub Kaczmarzyk <jakubk@mit.edu>
from __future__ import absolute_import, division, print_function

from neurodocker import SUPPORTED_SOFTWARE
from neurodocker.utils import load_json


class SpecsParser(object):
    """Class to parse specifications for Dockerfile.

    Parameters
    ----------
    filepath : str
        Path to JSON file containing environment specifications.
    specs : dict
        Dictionary of environment specifications.
    """
    VALID_TOP_LEVEL_KEYS = ['base', 'pkg_manager']
    VALID_TOP_LEVEL_KEYS.extend(SUPPORTED_SOFTWARE.keys())

    def __init__(self, filepath=None, specs=None):
        if filepath is not None and specs is not None:
            raise ValueError("Specify either `filepath` or `specs`, not both.")
        elif filepath is not None:
            self.specs = load_json(filepath)
        elif specs is not None:
            self.specs = specs

        self.parse()

    def __str__(self):
        return str(self.specs)

    def parse(self):
        self._validate_keys()
        try:
            self._parse_conda_pip()
        except KeyError:
            pass

    def _validate_keys(self):
        """Raise KeyError if invalid top-level key(s)."""
        if 'base' not in self.specs.keys():
            raise KeyError("A base image must be specified in the key 'base'.")
        if 'pkg_manager' not in self.specs.keys():
            raise KeyError("The Linux package manager must be specified in the "
                           "key 'pkg_manager'.")
        invalid = set(self.specs) - set(self.VALID_TOP_LEVEL_KEYS)
        if invalid:
            invalid = ", ".join(invalid)
            valid = ", ".join(self.VALID_TOP_LEVEL_KEYS)
            raise KeyError("Unexpected top-level key(s) in input: {0}. Valid "
                           "keys are {1}."
                           "".format(invalid, valid))

    def _parse_conda_pip(self):
        """Parse packages to install with `conda` and/or `pip`."""
        for key, val in self.specs['miniconda'].items():
            if key == "python_version":
                continue
            if isinstance(val, (list, tuple)):
                self.specs['miniconda'][key] = ' '.join(val)
            if isinstance(val, str):
                self.specs['miniconda'][key] = val
