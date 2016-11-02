import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### Snapshot Test ###################################################################################################
class Snapshot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "snapshot"
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
    # def test_string(self):
    #     print "[" + str(self.name) + "] No String Parameter to Test!"

    # prefix
    def test_prefix_Different(self):
        long = "thisIsAVeryLongPrefixForAPictureIGuessItCouldBeToLongMaybeMaybeNotWeWillSee"
        empty = ""
        illegal = "/Hello!!$%&/()=?"
        wrong_type = None
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "prefix", long),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "prefix", empty),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "prefix", illegal),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        # TODO: Check for wrong type
        # self.assertEqual(V.red.vision_string_parameter_set(id, "prefix", wrong_type), TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_prefix_Normal(self):
        new_value = "newPrefix"
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "prefix", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_get(id, "prefix").value, new_value)

    # format   {"yv12", "pgm", "bmp", "png", "jpg", "jpeg", "tiff",  "tif"}};
    def test_format_AllAvailable(self):
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "yv12"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "pgm"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "bmp"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "png"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "jpg"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "jpeg"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "tiff"), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", "tif"), TVE.TV_OK)

    def test_format_Normal(self):
        new_value = "jpg"
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "format", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_get(id, "format").value, new_value)

    # path
    def test_path_OutOfBounds(self):
        long = "/thisIsAVeryLongPthForAPictureIGuessItCouldBeToLongMaybeMaybeNotWeWillSee/"
        empty = ""
        illegal = "/Hello!!$%&/()=?"
        wrong_type = None
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "path", long),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "path", empty),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "path", illegal),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        # TODO: Check for wrong type
        # self.assertEqual(V.red.vision_string_parameter_set(id, "path", wrong_type), TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_path_Normal(self):
        new_value = "/home/tf"
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "path", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_get(id, "path").value, new_value)
