import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### Downscale Test ###################################################################################################
class Downscale(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "downscale"
        cls.module = Helper.start_module(cls.name)
        print "[" + cls.name + "] Starting Tests."
        Helper.show_running_modules(cls.name)

    @classmethod
    def tearDownClass(cls):
        Helper.kill_all_modules()
        Helper.show_running_modules(cls.name)
        print "[" + cls.name + "] Tests finished."

    # def setUp(self):
    #     print "su"
    #     self.name = "downscale"
    #     self.module = V.start_module(self.name)
    #     V.show_running_modules()
    #
    # def tearDown(self):
    #     print "td"
    #     V.kill_all_modules()

    ###### 1. Check if Module was successfully created (module.result==0) ###########################################
    def test_created(self):
        self.assertEqual(self.module.result, 0)

    ###### 2. Test Parameter Int ####################################################################################
    # def test_int_____(self):
    #     print "[" + str(self.name) + "] No Int Parameter to Test!"

    ### factor
    def test_factor_outOfBounds(self):
        default = 0
        min = 0
        max = 10
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "factor", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "factor", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_factor_normal(self):
        new_value = 5
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "factor", new_value),
                         TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "factor").value, new_value)

    ### period
    def test_period_outOfBounds(self):
        default = 1
        min = 0
        max = 500
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_period_normal(self):
        new_value = 400
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", new_value),
                         TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "period").value, new_value)

    ###### 3. Test Parameter String ################################################################################
    def test_string(self):
        # print "[" + str(self.name) + "] Starting String Parameter Tests."
        print "[" + str(self.name) + "] No String Parameter to Test!"
