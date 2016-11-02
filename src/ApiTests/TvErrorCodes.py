class TVE:
    TV_OK = 0
    TV_RESULT_BUFFERED = 1

    # /* General errors: */
    TV_NOT_IMPLEMENTED = -1
    TV_INTERNAL_ERROR = -2
    TV_INVALID_ARGUMENT = -3
    TV_BUSY = -4

    # ///< Could not allocate a node in a SceneTree
    TV_NODE_ALLOCATION_FAILED = -11
    TV_NO_ACTIVE_MODULES = -12

    # /* Camera errors: */
    TV_CAMERA_NOT_AVAILABLE = -21
    TV_CAMERA_SETTINGS_FAILED = -22

    # ///< An id passed to Api is not registered as Module
    TV_INVALID_ID = -31
    TV_MODULE_INITIALIZATION_FAILED = -32
    TV_MODULE_NO_SUCH_PARAMETER = -33
    TV_MODULE_ERROR_SETTING_PARAMETER = -34

    # /* System thread errors: */
    TV_EXEC_THREAD_FAILURE = -41
    TV_THREAD_RUNNING = -42

    # /* External library errors: */
    TV_MODULE_DLOPEN_FAILED = -51
    TV_MODULE_DLSYM_FAILED = -52
    TV_MODULE_DLCLOSE_FAILED = -53
    TV_MODULE_CONSTRUCTION_FAILED = -54
    TV_MODULE_NOT_AVAILABLE = -55

    # /* Callback/Result request errors: */
    TV_RESULT_NOT_AVAILABLE = -61
    TV_GLOBAL_CALLBACK_ACTIVE = -62