from tests.MpfWizardTestCase import MpfWizardTestCase
from mpfwiz.machinewizard import MachineWizard

class TestMachineWizard(MpfWizardTestCase):
    def test_MachineWizard_gameload(self):
        machine = MachineWizard(self.testargs)

        self.assertEqual(machine.mpfconfig['hardware']['platform'], 'smart_virtual')