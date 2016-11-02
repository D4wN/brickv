import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### Motiondetect Test ################################################################################################
class Motiondetect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "motiondetect"
        cls.module = Helper.start_module(cls.name)
        print "[" + cls.name + "] Starting Tests."
        Helper.show_running_modules(cls.name)

    @classmethod
    def tearDownClass(cls):
        Helper.kill_all_modules()
        Helper.show_running_modules(cls.name)
        print "[" + cls.name + "] Tests finished."

    ###### 1. Check if Module was successfully created (module.result==0) ###########################################
    def test_created(self):
        self.assertEqual(self.module.result, 0)

    ###### 2. Test Parameter Int ####################################################################################
    #  def test_int(self):
    #     print "[" + str(self.name) + "] No Int Parameter to Test!"

    #   result_timeout  min=0   max=40  default=20
    def test_result_timeout_OutOfBounds(self):
        default = 20
        min = 0
        max = 40
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "result_timeout", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "result_timeout", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_result_timeout_Normal(self):
        new_value = 5
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "result_timeout", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "result_timeout").value, new_value)

    #   callbacks_enabled   min=0   max=1   default=1
    def test_callbacks_enabled_OutOfBounds(self):
        default = 1
        min = 0
        max = 1
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "callbacks_enabled", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "callbacks_enabled", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_callbacks_enabled_Normal(self):
        new_value = 0
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "callbacks_enabled", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "callbacks_enabled").value, new_value)

    #   period    min=0   max=500 default=1
    def test_period_OutOfBounds(self):
        default = 1
        min = 0
        max = 500
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_period_Normal(self):
        new_value = 300
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "period").value, new_value)

    ###### 3. Test Parameter String ################################################################################
    def test_string(self):
        print "[" + str(self.name) + "] No String Parameter to Test!"
