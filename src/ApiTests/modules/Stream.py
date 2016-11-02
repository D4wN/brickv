import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

#### Stream Test #######################################################################################################
class Stream(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "stream"

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

    def test_period_OutOfBounds(self):
        default = 0
        min = 0
        max = 500
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (min - 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", (max + 1)),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_period_Normal(self):
        new_value = 333
        id = self.module.id
        self.assertEqual(Helper.red.vision_numerical_parameter_set(id, "period", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_numerical_parameter_get(id, "period").value, new_value)

    ###### 3. Test Parameter String ################################################################################
    # def test_string(self):
    #     print "[" + str(self.name) + "] No String Parameter to Test!"

    def test_url_Different(self):
        id = self.module.id
        long = "thisIsAVeryLongPrefixForAPictureIGuessItCouldBeToLongMaybeMaybeNotWeWillSee"
        empty = ""
        illegal = "/Hello!!$%&/()=?"
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "url", long),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "url", empty),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "url", illegal),
                         TVE.TV_MODULE_ERROR_SETTING_PARAMETER)

    def test_url_Normal(self):
        new_value = "stream"
        # new_value = "/stream"
        # new_value = "/stream/"
        # new_value = "loclahost:4444/stream"
        id = self.module.id
        self.assertEqual(Helper.red.vision_string_parameter_set(id, "url", new_value), TVE.TV_OK)
        self.assertEqual(Helper.red.vision_string_parameter_get(id, "url").value, new_value)
