import unittest
import sys
import logging
import inspect

from datetime import datetime, timedelta

from mock import *

from mpfwiz.machinewizard import MachineWizard
from mpf.system.utility_functions import Util

from time import time, sleep

class TestMachineWizard(MachineWizard):
    def __init__(self, options):
        self.options = options
        #super().__init__(options)

class MpfWizardTestCase(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.testargs = dict()
        self.testargs['mpfconfigfile'] = 'tests/machine_files/mpfconfig.yaml'
        self.testargs['machine_path'] = '../tests/machine_files/basic_loading'
        self.testargs['loglevel'] = 10
        self.testargs['bcp'] = True
        self.testargs['consoleloglevel'] = 20
        self.testargs['logfile'] = 'logs\\2016-01-22-09-42-26-mpf-OmegaStation.log'
        self.testargs['create'] = False
        self.testargs['rebuild_cache'] = False
        self.testargs['force_platform'] = None
        self.testargs['configfile'] = ['config']
