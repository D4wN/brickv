import unittest

from ApiTests.TvErrorCodes import TVE
from ApiTests.Util import Helper

#### Functions Test #######################################################################################################
class Functions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.name = "TvFunctions"
        # cls.module = Helper.start_module(cls.mod_name)
        print "[" + cls.name + "] Starting Tests."
        # Helper.show_running_modules(cls.name)

    @classmethod
    def tearDownClass(cls):
        # Helper.kill_all_modules()
        Helper.show_running_modules(cls.name)
        print "[" + cls.name + "] Tests finished."

    ##############################################################################################
    def test_basic_Functions(self):
        # def vision_is_valid(self):
        self.assertEqual(Helper.red.vision_is_valid(), TVE.TV_OK)
        # def vision_camera_available(self):
        self.assertEqual(Helper.red.vision_camera_available(), TVE.TV_OK)

    def test_framesize_Functions(self):
        # def vision_get_framesize(self):
        self.assertEqual(Helper.red.vision_get_framesize().result, TVE.TV_OK)  # TODO bug reported???
        # # def vision_set_framesize(self, width, height):
        self.assertEqual(Helper.red.vision_set_framesize(160, 90).result, TVE.TV_OK)

    def test_frameperiod_Functions(self):
        # def vision_get_frameperiod(self):
        self.assertEqual(Helper.red.vision_get_frameperiod().result, TVE.TV_OK)
        # def vision_request_frameperiod(self, milliseconds):
        self.assertEqual(Helper.red.vision_request_frameperiod(1000), TVE.TV_OK)

    def test_vision_Functions(self):
        # def vision_start_idle(self):
        self.assertEqual(Helper.red.vision_start_idle(), TVE.TV_OK)
        # def vision_stop(self):
        self.assertEqual(Helper.red.vision_stop(), TVE.TV_OK)
        # def vision_restart(self):
        self.assertEqual(Helper.red.vision_restart(), TVE.TV_OK)
        # Test purpose!
        self.assertEqual(Helper.red.vision_stop(), TVE.TV_OK)

    def test_lib_DynamicFunctions(self):
        # Creates dynamic test for all found modules.

        # def vision_libs_count(self):
        result = Helper.red.vision_libs_count()
        self.assertEqual(result.result, TVE.TV_OK)  # Test if libs are there
        lib_count = result.count
        for lib_number in range(0, lib_count):
            # def vision_lib_name_path(self, number):
            result = Helper.red.vision_lib_name_path(lib_number)
            self.assertEqual(result.result, TVE.TV_OK)  # Test if lib could be read
            lib_name = result.name

            # def vision_lib_parameters_count(self, lib):
            result = Helper.red.vision_lib_parameters_count(lib_name)
            self.assertEqual(result.result, TVE.TV_OK)  # Test if lib parameter could be read
            para_count = result.count
            for para_number in range(0, para_count):
                # def vision_lib_parameter_describe(self, libname, parameter):
                result = Helper.red.vision_lib_parameter_describe(lib_name, para_number)
                self.assertEqual(result.result, TVE.TV_OK)  # Test if lib parameter discription is working

    def test_lib_Functions(self):
        # def vision_lib_get_system_load_path(self):
        self.assertEqual(Helper.red.vision_lib_get_system_load_path().result, TVE.TV_OK)

        # def vision_lib_get_user_prefix(self):
        result = Helper.red.vision_lib_get_user_prefix()
        self.assertEqual(result.result, TVE.TV_OK)

        # def vision_lib_set_user_prefix(self, path):
        new_path = "/home/tf/"
        self.assertEqual(Helper.red.vision_lib_set_user_prefix(new_path),
                         TVE.TV_OK)

    def test_error_Discriptions(self):
        # look at TvErrorCodes.py
        # def vision_get_error_description(self, code):
        # TV_OK = 0
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_OK), "Ok")
        # TV_RESULT_BUFFERED = 1
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_RESULT_BUFFERED), "Result buffered")
        #
        # # /* General errors: */
        # TV_NOT_IMPLEMENTED = -1
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_NOT_IMPLEMENTED), "Not implemented")
        # TV_INTERNAL_ERROR = -2
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_INTERNAL_ERROR), "Unknown internal error")
        # TV_INVALID_ARGUMENT = -3
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_INVALID_ARGUMENT), "Invalid argument passed")
        # TV_BUSY = -4
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_BUSY), "Tinkervision busy; try again")
        #
        # # ///< Could not allocate a node in a SceneTree
        # TV_NODE_ALLOCATION_FAILED = -11
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_NODE_ALLOCATION_FAILED),
                         "Allocating scene node failed")
        # TV_NO_ACTIVE_MODULES = -12
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_NO_ACTIVE_MODULES), "No active modules")
        #
        # # /* Camera errors: */
        # TV_CAMERA_NOT_AVAILABLE = -21
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_CAMERA_NOT_AVAILABLE), "Camera not available")
        # TV_CAMERA_SETTINGS_FAILED = -22
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_CAMERA_SETTINGS_FAILED),
                         "Camera settings failed")
        #
        # # ///< An id passed to Api is not registered as Module
        # TV_INVALID_ID = -31
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_INVALID_ID), "ID is invalid")
        # TV_MODULE_INITIALIZATION_FAILED = -32
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_INITIALIZATION_FAILED),
                         "Module Initialization failed")
        # TV_MODULE_NO_SUCH_PARAMETER = -33
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_NO_SUCH_PARAMETER), "No such parameter")
        # TV_MODULE_ERROR_SETTING_PARAMETER = -34
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_ERROR_SETTING_PARAMETER),
                         "Module settings failed")
        #
        # # /* System thread errors: */
        # TV_EXEC_THREAD_FAILURE = -41
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_EXEC_THREAD_FAILURE),
                         "Main thread did not react")
        # TV_THREAD_RUNNING = -42
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_THREAD_RUNNING), "Main thread already running")
        #
        # # /* External library errors: */
        # TV_MODULE_DLOPEN_FAILED = -51
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_DLOPEN_FAILED), "Module dlopen failed")
        # TV_MODULE_DLSYM_FAILED = -52
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_DLSYM_FAILED), "Module dlsym failed")
        # TV_MODULE_DLCLOSE_FAILED = -53
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_DLCLOSE_FAILED), "Module dlclose failed")
        # TV_MODULE_CONSTRUCTION_FAILED = -54
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_CONSTRUCTION_FAILED),
                         "Module construction failed")
        # TV_MODULE_NOT_AVAILABLE = -55
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_MODULE_NOT_AVAILABLE), "Module not available")
        #
        # # /* Callback/Result request errors: */
        # TV_RESULT_NOT_AVAILABLE = -61
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_RESULT_NOT_AVAILABLE),
                         "No result provided by module")
        # TV_GLOBAL_CALLBACK_ACTIVE = -62
        self.assertEqual(Helper.red.vision_get_error_description(TVE.TV_GLOBAL_CALLBACK_ACTIVE),
                         "Global callback is active")

# Static Stuff

# #Scene Stuff
# def vision_scene_start(self, module_id):
# def vision_scene_add(self, scene_id, module_id):
# def vision_scene_remove(self, scene_id):
