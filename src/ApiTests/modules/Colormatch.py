import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### Colormatch Test ##################################################################################################
class Colormatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "colormatch"
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
    # def test_int(self):
    #     print "[" + str(self.name) + "] No Int Parameter to Test!"

    # min-hue
    def test_min_hue_OutOfBounds(self):
        default = 0
        min = 0
        max = 180
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-hue", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-hue", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_min_hue_Normal(self):
        new_value = 90
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-hue", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "min-hue").value, new_value)

    # max-hue
    def test_max_hue_OutOfBounds(self):
        default = 0
        min = 0
        max = 180
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-hue", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-hue", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_max_hue_Normal(self):
        new_value = 95
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-hue", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "max-hue").value, new_value)

    # min-value
    def test_min_value_OutOfBounds(self):
        default = 0
        min = 0
        max = 255
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-value", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-value", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_min_value_Normal(self):
        new_value = 200
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-value", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "min-value").value, new_value)

    # max-value
    def test_max_value_OutOfBounds(self):
        default = 0
        min = 0
        max = 255
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-value", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-value", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_max_value_Normal(self):
        new_value = 150
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-value", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "max-value").value, new_value)

    # min-saturation
    def test_min_saturation_OutOfBounds(self):
        default = 0
        min = 0
        max = 255
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-saturation", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-saturation", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_min_saturation_Normal(self):
        new_value = 125
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "min-saturation", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "min-saturation").value, new_value)

    # max-saturation
    def test_max_saturation_OutOfBounds(self):
        default = 0
        min = 0
        max = 255
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-saturation", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-saturation", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_max_saturation_Normal(self):
        new_value = 55
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "max-saturation", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "max-saturation").value, new_value)

    # result_timeout
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
        new_value = 10
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "result_timeout", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "result_timeout").value, new_value)

    # callbacks_enabled
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

    # period
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
        print "[" + str(self.name) + "] No String Parameter to Test!"
