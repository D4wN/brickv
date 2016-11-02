import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### XXXX Test ########################################################################################################
class TEST(unittest.TestCase):  # Change TEST to Name <-----------------------------------------------------------------

    @classmethod
    def setUpClass(cls):
        cls.name = "NAMEHERE"  # Insert Name <---------------------------------------------------------------------------
        cls.module = Helper.start_module(cls.name)
        print "[" + cls.name + "] Starting Tests."
        Helper.show_running_modules(cls.name)

    @classmethod
    def tearDownClass(cls):
        Helper.kill_all_modules()
        Helper.show_running_modules(cls.name)
        print "[" + cls.name + "] Tests finished."

    ###### 1. Check if Module was successfully created (module.result==0) ##############################################
    def test_created(self):
        self.assertEqual(self.module.result, 0)

    ###### 2. Test Parameter Int #######################################################################################
    # def test_int(self): # Use if no Int Parameters <------------------------------------------------------------------
    #     print "[" + str(self.name) + "] No Int Parameter to Test!"

    def test_XXX2_OutOfBounds(self):  # Change XXX2 to Parameter Name <-------------------------------------------------
        default = 0
        min = 0
        max = 10
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "XXX2", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "XXX2", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_XXX2_Normal(self):
        new_value = 5
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "XXX2", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "XXX2").value, new_value)

    ###### 3. Test Parameter String ####################################################################################
    # def test_string(self): # Use if no String Parameters <------------------------------------------------------------
    #     print "[" + str(self.name) + "] No String Parameter to Test!"

    def test_XXX_OutOfBounds(self):  # Change XXX to Parameter Name <---------------------------------------------------
        default = 0
        min = 0
        max = 10
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "XXX", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "XXX", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_XXX_Normal(self):
        new_value = 5
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "XXX", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_get(id, "XXX").value, new_value)
