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
from mpf.system.tasks import Task, DelayManager, DelayManagerRegistry
from mpf.system.data_manager import DataManager
from mpf.system.timing import Timing
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
        done: Boolean. Set to True and MPF exits.
        machine_path: The root path of this machine_files folder
        display:
        plugins:
        scriptlets:
        platform:
        events:
    """
    def __init__(self, options):
        self.options = options
        self.log = logging.getLogger('machinewizard')
        self.log.info("MPF Wizard v%s", version.__version__)
        self.log.debug("Init Options: {}".format(self.options))
        self.verify_system_info()

        self.done = False
        self.machine_path = None  # Path to this machine's folder root
        self.game = None
        self.machine_vars = CaseInsensitiveDict()
        self.machine_var_monitor = False
        self.machine_var_data_manager = None

        FileManager.init()

        self.mpfconfig = dict()
        self.mpfconfig = Config.load_config_file(self.options['mpfconfigfile'])

        self.config_files = dict()
        #self.config = Config.load_config_file(self.options['mpfconfigfile'])
        self._set_machine_path()
        self._load_config_from_files()
        
        self.hardware_platforms = dict()
        self.default_platform = None        

        # Do this here so there's a credit_string var even if they're not using
        # the credits mode
        #try:
            #credit_string = self.config['credits']['free_play_string']
        #except KeyError:
            #credit_string = 'FREE PLAY'

        #self.create_machine_var('credits_string', credit_string, silent=True)

        self.log.info('machine config loaded')

    def validate_machine_config_section(self, section):
        if section not in self.config['config_validator']:
            return

        if section not in self.config:
            self.config[section] = dict()

        self.config[section] = self.config_processor.process_config2(
            section, self.config[section], section)

    def _load_machine_vars(self):
        self.machine_var_data_manager = DataManager(self, 'machine_vars')

        current_time = time.time()

        for name, settings in (
                iter(self.machine_var_data_manager.get_data().items())):

            if ('expire' in settings and settings['expire'] and
                    settings['expire'] < current_time):

                settings['value'] = 0

            self.create_machine_var(name=name, value=settings['value'])

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

        if python_version[0] != 3:
            self.log.error("Incorrect Python version. MPF requires Python 3."
                           "x. You have Python %s.%s.%s.", python_version[0],
                           python_version[1], python_version[2])
            sys.exit()

        self.log.debug("Python version: %s.%s.%s", python_version[0],
                      python_version[1], python_version[2])
        self.log.debug("Platform: %s", sys.platform)
        self.log.debug("Python executable location: %s", sys.executable)
        self.log.debug("32-bit Python? %s", sys.maxsize < 2**32)


    def configure_debugger(self):
        pass

    def set_machine_var(self, name, value, force_events=False):
        """Sets the value of a machine variable.

        Args:
            name: String name of the variable you're setting the value for.
            value: The value you're setting. This can be any Type.
            force_events: Boolean which will force the event posting, the
                machine monitor callback, and writing the variable to disk (if
                it's set to persist). By default these things only happen if
                the new value is different from the old value.

        """
        if name not in self.machine_vars:
            self.log.warning("Received request to set machine_var '%s', but "
                             "that is not a valid machine_var.", name)
            return

        prev_value = self.machine_vars[name]['value']
        self.machine_vars[name]['value'] = value

        try:
            change = value-prev_value
        except TypeError:
            if prev_value != value:
                change = True
            else:
                change = False

        if change or force_events:

            if self.machine_vars[name]['persist'] and self.config['mpf']['save_machine_vars_to_disk']:
                disk_var = CaseInsensitiveDict()
                disk_var['value'] = value

                if self.machine_vars[name]['expire_secs']:
                    disk_var['expire'] = (time.time() +
                        self.machine_vars[name]['expire_secs'])

                self.machine_var_data_manager.save_key(name, disk_var)

            self.log.debug("Setting machine_var '%s' to: %s, (prior: %s, "
                           "change: %s)", name, value, prev_value,
                           change)
            self.events.post('machine_var_' + name,
                                     value=value,
                                     prev_value=prev_value,
                                     change=change)

            if self.machine_var_monitor:
                for callback in self.monitors['machine_vars']:
                    callback(name=name, value=value,
                             prev_value=prev_value, change=change)

    def get_machine_var(self, name):
        """Returns the value of a machine variable.

        Args:
            name: String name of the variable you want to get that value for.

        Returns:
            The value of the variable if it exists, or None if the variable
            does not exist.

        """
        try:
            return self.machine_vars[name]['value']
        except KeyError:
            return None

    def is_machine_var(self, name):
        if name in self.machine_vars:
            return True
        else:
            return False

    def create_machine_var(self, name, value=0, persist=False,
                           expire_secs=None, silent=False):
        """Creates a new machine variable:

        Args:
            name: String name of the variable.
            value: The value of the variable. This can be any Type.
            persist: Boolean as to whether this variable should be saved to
                disk so it's available the next time MPF boots.
            expire_secs: Optional number of seconds you'd like this variable
                to persist on disk for. When MPF boots, if the expiration time
                of the variable is in the past, it will be loaded with a value
                of 0. For example, this lets you write the number of credits on
                the machine to disk to persist even during power off, but you
                could set it so that those only stay persisted for an hour.

        """
        var = CaseInsensitiveDict()

        var['value'] = value
        var['persist'] = persist
        var['expire_secs'] = expire_secs

        self.machine_vars[name] = var

        if not silent:
            self.set_machine_var(name, value, force_events=True)

    def remove_machine_var(self, name):
        """Removes a machine variable by name. If this variable persists to
        disk, it will remove it from there too.

        Args:
            name: String name of the variable you want to remove.

        """
        try:
            del self.machine_vars[name]
            self.machine_var_data_manager.remove_key(name)
        except KeyError:
            pass

    def remove_machine_var_search(self, startswith='', endswith=''):
        """Removes a machine variable by matching parts of its name.

        Args:
            startswith: Optional start of the variable name to match.
            endswith: Optional end of the variable name to match.

        For example, if you pass startswit='player' and endswith='score', this
        method will match and remove player1_score, player2_score, etc.

        """
        for var in list(self.machine_vars.keys()):
            if var.startswith(startswith) and var.endswith(endswith):
                del self.machine_vars[var]
                self.machine_var_data_manager.remove_key(var)



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
