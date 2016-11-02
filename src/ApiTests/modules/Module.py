import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

##### Module Test ######################################################################################################
class Module(unittest.TestCase):  # Change TEST to Name <---------------------------------------------------------------

    @classmethod
    def setUpClass(cls):
        cls.name = "Module"
        cls.mod_name = "grayfilter"
        cls.module = Helper.start_module(cls.mod_name)
        print "[" + cls.name + "] Starting Tests."
        Helper.show_running_modules(cls.name)

    @classmethod
    def tearDownClass(cls):
        Helper.kill_all_modules()
        Helper.show_running_modules(cls.name)
        print "[" + cls.name + "] Tests finished."

    ###### 1. Check if Module was successfully created (module.result==0) ##############################################
    def test_created(self):
        # def vision_module_start(self, name):
        self.assertEqual(self.module.result, 0)

    ###### Next Test ###################################################################################################
    def test_module_Stop_Restart(self):
        # def vision_module_stop(self, id):
        self.assertEqual(Helper.red.vision_module_stop(self.module.id), TVE.TV_OK)
        # def vision_module_restart(self, id):
        self.assertEqual(Helper.red.vision_module_restart(self.module.id), TVE.TV_OK)

    def test_module_Getter(self):
        pass
        # def vision_module_get_name(self, id):
        tmp = Helper.red.vision_module_get_name(self.module.id)
        self.assertEqual(tmp.result, TVE.TV_OK)
        self.assertEqual(tmp.name, self.mod_name)
        # def vision_module_get_id(self, library):
        tmp = Helper.red.vision_module_get_id(0)
        self.assertEqual(tmp.result, TVE.TV_OK)
        self.assertEqual(tmp.id, self.module.id)
        # def vision_module_is_active(self, id):
        tmp = Helper.red.vision_module_is_active(self.module.id)
        self.assertEqual(tmp.result, TVE.TV_OK)
        self.assertEqual(tmp.active, 1)  # 1 = True

        # def vision_module_result(self, module_id):
        # there should be no result avaialbe; -61 as error code
        self.assertEqual(Helper.red.vision_module_result(self.module.id).result, TVE.TV_RESULT_NOT_AVAILABLE)

    def test_module_Remove(self):
        tmp_module = Helper.red.vision_module_start(self.mod_name)
        self.assertEqual(tmp_module.result, TVE.TV_OK)
        # def vision_libs_loaded_count(self): # shows module loaded count! should be 2 here
        tmp = Helper.red.vision_libs_loaded_count()
        self.assertEqual(tmp.result, TVE.TV_OK)
        self.assertEqual(tmp.count, 2)
        # def vision_module_remove(self, id): # remove the new module
        Helper.show_running_modules(self.name)
        self.assertEqual(Helper.red.vision_module_remove(tmp_module.id), TVE.TV_OK)
        # import time
        # time.sleep(5)
        self.assertEqual(tmp.count, 1)
        Helper.show_running_modules(self.name)
