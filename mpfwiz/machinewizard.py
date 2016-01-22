"""Contains the MachineWizard base class"""
# machinewizard.py
# Mission Pinball Framework Wizard
# Written by Brian Madden, Gabe Knuth & John Marsh
# Released under the MIT License. (See license info at the end of this file.)

import pickle
import logging
import os
import time
import sys
import queue

import errno

from mpf.system import *
from mpf.system.config import Config, CaseInsensitiveDict
from mpf.system.data_manager import DataManager
from mpf.system.assets import AssetManager
from mpf.system.utility_functions import Util
from mpf.system.file_manager import FileManager
import version
from mpfwiz.config_storage import MPFConfigFile


class MachineWizard(object):
    """Base class for the Machine Wizard object.

    The machine wizard is the main entity used by the mpf wizard. It's the
    layer between the Wizard UI and the configuration files.

    Args:
        options: Dictionary of options the machine wizard uses to configure
            itself.

    Attributes:
        options: A dictionary of options built from the command line options
            used to launch mpf.py.
        config: A dictionary of machine's configuration settings, merged from
            various sources.
        machine_path: The root path of this machine_files folder
    """
    def __init__(self, options):
        self.options = options
        self.log = logging.getLogger('machinewizard')
        self.log.info("MPF Wizard v%s", version.__version__)
        self.log.debug("Init Options: {}".format(self.options))
        self.verify_system_info()

        self.done = False
        self.machine_path = None  # Path to this machine's folder root

        FileManager.init()

        self.mpfconfig = dict()
        self.mpfconfig = Config.load_config_file(self.options['mpfconfigfile'])

        self.config_files = dict()
        #self.config = Config.load_config_file(self.options['mpfconfigfile'])
        self._set_machine_path()
        self._load_config_from_files()
        
        self.log.info('machine config loaded')

    def _set_machine_path(self):
        # If the machine folder value passed starts with a forward or
        # backward slash, then we assume it's from the mpf root. Otherwise we
        # assume it's in the mpf/machine_files folder
        if (self.options['machine_path'].startswith('/') or
                self.options['machine_path'].startswith('\\')):
            machine_path = self.options['machine_path']
        else:
            machine_path = os.path.join(self.mpfconfig['mpf']['paths']
                                        ['machine_files'],
                                        self.options['machine_path'])

        self.machine_path = os.path.abspath(machine_path)
        self.log.debug("Machine path: {}".format(self.machine_path))

        # Add the machine folder to sys.path so we can import modules from it
        sys.path.append(self.machine_path)

    def _load_config_from_files(self):
        self.log.info("Loading config from original files")
        for num, config_file in enumerate(self.options['configfile']):

            if not (config_file.startswith('/') or
                    config_file.startswith('\\')):

                config_file = os.path.join(self.machine_path,
                    self.mpfconfig['mpf']['paths']['config'], config_file)

            self.log.info("Machine config file #%s: %s", num+1, config_file)

            new_config = self._load_config_file(config_file)
            #new_config = MPFConfigFile(config_file, self._load_config_file(config_file))
            self.config_files[config_file] = new_config

    def _load_config_file(self, filename, verify_version=True, halt_on_error=True):
        config_file = MPFConfigFile(filename, FileManager.load(filename, verify_version, halt_on_error, True))

        try:
            if 'config' in config_file.config:
                path = os.path.split(filename)[0]

                for file in Util.string_to_list(config_file.config['config']):
                    full_file = os.path.join(path, file)
                    new_config = self._load_config_file(full_file)
                    config_file.add_child_file(new_config)
            return config_file
        except TypeError:
            return dict()

    def verify_system_info(self):
        """Dumps information about the Python installation to the log.

        Information includes Python version, Python executable, platform, and
        system architecture.

        """
        python_version = sys.version_info

        if python_version[0] != 3:  # pragma: no cover
            self.log.error("Incorrect Python version. MPF requires Python 3."
                           "x. You have Python %s.%s.%s.", python_version[0],
                           python_version[1], python_version[2])
            sys.exit()

        self.log.debug("Python version: %s.%s.%s", python_version[0],
                      python_version[1], python_version[2])
        self.log.debug("Platform: %s", sys.platform)
        self.log.debug("Python executable location: %s", sys.executable)
        self.log.debug("32-bit Python? %s", sys.maxsize < 2**32)


# The MIT License (MIT)

# Copyright (c) 2013-2016 Brian Madden, Gabe Knuth and the AUTHORS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
