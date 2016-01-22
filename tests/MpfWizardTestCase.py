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

    def someRandomFunction(self):
        return 'fyc'
