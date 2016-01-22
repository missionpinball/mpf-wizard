from tests.MpfWizardTestCase import MpfWizardTestCase
from mpfwiz.config_storage import MPFConfigFile

class TestConfigStorage(MpfWizardTestCase):

    def test_MPFConfigFile_mergedconfig(self):
        
        test_dict = dict()
        test_dict['hardware'] = dict()
        test_dict['hardware']['platform'] = 'smart_virtual'
        test_dict['hardware']['driverboards'] = 'virtual'
        test_dict['hardware']['dmd'] = 'smartmatrix'
        test_dict['coils'] = dict()
        test_dict['coils']['c_flipper_left_main'] = dict()
        test_dict['coils']['c_flipper_left_main']['number'] = 0
        test_dict['coils']['c_flipper_left_hold'] = dict()
        test_dict['coils']['c_flipper_left_hold']['number'] = 1
        
        root_config = dict()
        root_config['hardware'] = dict()
        root_config['hardware']['platform'] = 'smart_virtual'
        root_config['hardware']['driverboards'] = 'virtual'
        root_config['hardware']['dmd'] = 'smartmatrix'
        root_config_file = MPFConfigFile('rootfile.yaml', root_config)

        child_config = dict()
        child_config['coils'] = dict()
        child_config['coils']['c_flipper_left_main'] = dict()
        child_config['coils']['c_flipper_left_main']['number'] = 0
        child_config['coils']['c_flipper_left_hold'] = dict()
        child_config['coils']['c_flipper_left_hold']['number'] = 1
        child_config_file = MPFConfigFile('childfile.yaml', child_config)
        
        root_config_file.add_child_file(child_config_file)
        
        merged_dict = root_config_file.get_merged_config()
        
        self.assertDictEqual(merged_dict, test_dict)
        