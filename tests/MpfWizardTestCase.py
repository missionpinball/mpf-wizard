import unittest

from mpfwiz.machinewizard import MachineWizard
from mpf.system.utility_functions import Util
import logging
import time
import sys
from mock import *
from datetime import datetime, timedelta
import inspect


class TestMachineWizard(MachineWizard):
    def __init__(self, options):
        self.options = options
        #super().__init__(options)

    def someRandomFunction(self):
        return 'fyc'

class MpfWizardTestCase(unittest.TestCase):
    def loadTestArgs(self):
        self.testargs = dict()
        self.testargs['mpfconfigile'] = 'E:\\mpf-dev\\mpf\\mpf\\mpfconfig.yaml'
        self.testargs['machine_path'] = 'E:\\spaceballs\\spaceballs'
        self.testargs['loglevel'] = 10
        self.testargs['bcp'] = True
        self.testargs['consoleloglevel'] = 20
        self.testargs['logfile'] = 'logs\\2016-01-22-09-42-26-mpf-OmegaStation.log'
        self.testargs['create'] = False
        self.testargs['rebuild_cache'] = False
        self.testargs['force_platform'] = None
        self.testargs['configfile'] = ['config']

    def someRandomFunction(self):
        return 'fyc'
