from tests.MpfWizardTestCase import MpfWizardTestCase
from tests.MpfWizardTestCase import TestMachineWizard

class TestConfigLoad(MpfWizardTestCase):

    def test_singe_file_load(self):
        machine = TestMachineWizard(None)
        
        self.assertEqual(machine.someRandomFunction(), 'fyc')

    def test_some_other_thing(self):
        machine = TestMachineWizard(None)
        
        self.assertEqual(machine.someRandomFunction(), 'fyc')
        