# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2015-12-09.      #
#                                                           #
# Bindings Version 2.1.5                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

try:
    from collections import namedtuple
except ImportError:
    try:
        from tinkerforge.ip_connection import namedtuple
    except ValueError:
        from tinkerforge.ip_connection import namedtuple

try:
    from tinkerforge.ip_connection import Device, IPConnection, Error
except ValueError:
    from tinkerforge.ip_connection import Device, IPConnection, Error

CreateSession = namedtuple('CreateSession', ['error_code', 'session_id'])
AllocateString = namedtuple('AllocateString', ['error_code', 'string_id'])
GetStringLength = namedtuple('StringLength', ['error_code', 'length'])
GetStringChunk = namedtuple('StringChunk', ['error_code', 'buffer'])
AllocateList = namedtuple('AllocateList', ['error_code', 'list_id'])
GetListLength = namedtuple('ListLength', ['error_code', 'length'])
GetListItem = namedtuple('ListItem', ['error_code', 'item_object_id', 'type'])
OpenFile = namedtuple('OpenFile', ['error_code', 'file_id'])
CreatePipe = namedtuple('CreatePipe', ['error_code', 'file_id'])
GetFileInfo = namedtuple('FileInfo', ['error_code', 'type', 'name_string_id', 'flags', 'permissions', 'uid', 'gid', 'length', 'access_timestamp', 'modification_timestamp', 'status_change_timestamp'])
ReadFile = namedtuple('ReadFile', ['error_code', 'buffer', 'length_read'])
WriteFile = namedtuple('WriteFile', ['error_code', 'length_written'])
SetFilePosition = namedtuple('SetFilePosition', ['error_code', 'position'])
GetFilePosition = namedtuple('FilePosition', ['error_code', 'position'])
GetFileEvents = namedtuple('FileEvents', ['error_code', 'events'])
OpenDirectory = namedtuple('OpenDirectory', ['error_code', 'directory_id'])
GetDirectoryName = namedtuple('DirectoryName', ['error_code', 'name_string_id'])
GetNextDirectoryEntry = namedtuple('NextDirectoryEntry', ['error_code', 'name_string_id', 'type'])
GetProcesses = namedtuple('Processes', ['error_code', 'processes_list_id'])
SpawnProcess = namedtuple('SpawnProcess', ['error_code', 'process_id'])
GetProcessCommand = namedtuple('ProcessCommand', ['error_code', 'executable_string_id', 'arguments_list_id', 'environment_list_id', 'working_directory_string_id'])
GetProcessIdentity = namedtuple('ProcessIdentity', ['error_code', 'pid', 'uid', 'gid'])
GetProcessStdio = namedtuple('ProcessStdio', ['error_code', 'stdin_file_id', 'stdout_file_id', 'stderr_file_id'])
GetProcessState = namedtuple('ProcessState', ['error_code', 'state', 'timestamp', 'exit_code'])
GetPrograms = namedtuple('Programs', ['error_code', 'programs_list_id'])
DefineProgram = namedtuple('DefineProgram', ['error_code', 'program_id'])
GetProgramIdentifier = namedtuple('ProgramIdentifier', ['error_code', 'identifier_string_id'])
GetProgramRootDirectory = namedtuple('ProgramRootDirectory', ['error_code', 'root_directory_string_id'])
GetProgramCommand = namedtuple('ProgramCommand', ['error_code', 'executable_string_id', 'arguments_list_id', 'environment_list_id', 'working_directory_string_id'])
GetProgramStdioRedirection = namedtuple('ProgramStdioRedirection', ['error_code', 'stdin_redirection', 'stdin_file_name_string_id', 'stdout_redirection', 'stdout_file_name_string_id', 'stderr_redirection', 'stderr_file_name_string_id'])
GetProgramSchedule = namedtuple('ProgramSchedule', ['error_code', 'start_mode', 'continue_after_error', 'start_interval', 'start_fields_string_id'])
GetProgramSchedulerState = namedtuple('ProgramSchedulerState', ['error_code', 'state', 'timestamp', 'message_string_id'])
GetLastSpawnedProgramProcess = namedtuple('LastSpawnedProgramProcess', ['error_code', 'process_id', 'timestamp'])
GetCustomProgramOptionNames = namedtuple('CustomProgramOptionNames', ['error_code', 'names_list_id'])
GetCustomProgramOptionValue = namedtuple('CustomProgramOptionValue', ['error_code', 'value_string_id'])
VisionGetFramesize = namedtuple('VisionGetFramesize', ['result', 'width', 'height'])
VisionGetFrameperiod = namedtuple('VisionGetFrameperiod', ['result', 'milliseconds'])
VisionNumericalParameterGet = namedtuple('VisionNumericalParameterGet', ['result', 'value'])
VisionStringParameterGet = namedtuple('VisionStringParameterGet', ['result', 'value'])
VisionModuleStart = namedtuple('VisionModuleStart', ['result', 'id'])
VisionModuleGetName = namedtuple('VisionModuleGetName', ['result', 'name'])
VisionModuleGetID = namedtuple('VisionModuleGetID', ['result', 'id'])
VisionModuleIsActive = namedtuple('VisionModuleIsActive', ['result', 'active'])
VisionLibsCount = namedtuple('VisionLibsCount', ['result', 'count'])
VisionLibsLoadedCount = namedtuple('VisionLibsLoadedCount', ['result', 'count'])
VisionLibNamePath = namedtuple('VisionLibNamePath', ['result', 'name', 'path'])
VisionLibParametersCount = namedtuple('VisionLibParametersCount', ['result', 'count'])
VisionLibParameterDescribe = namedtuple('VisionLibParameterDescribe', ['result', 'name', 'type', 'min', 'max', 'default'])
VisionLibGetUserPrefix = namedtuple('VisionLibGetUserPrefix', ['result', 'path'])
VisionLibGetSystemLoadPath = namedtuple('VisionLibGetSystemLoadPath', ['result', 'path'])
VisionModuleResult = namedtuple('VisionModuleResult', ['result', 'x', 'y', 'width', 'height', 'string'])
VisionSceneStart = namedtuple('VisionSceneStart', ['result', 'scene_id'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickRED(Device):
    """
    Executes user programs and controls other Bricks/Bricklets standalone
    """

    DEVICE_IDENTIFIER = 17
    DEVICE_DISPLAY_NAME = 'RED Brick'

    CALLBACK_ASYNC_FILE_READ = 30
    CALLBACK_ASYNC_FILE_WRITE = 31
    CALLBACK_FILE_EVENTS_OCCURRED = 32
    CALLBACK_PROCESS_STATE_CHANGED = 45
    CALLBACK_PROGRAM_SCHEDULER_STATE_CHANGED = 65
    CALLBACK_PROGRAM_PROCESS_SPAWNED = 66
    CALLBACK_VISION_LIBRARIES = 104
    CALLBACK_VISION_MODULE = 105

    FUNCTION_CREATE_SESSION = 1
    FUNCTION_EXPIRE_SESSION = 2
    FUNCTION_EXPIRE_SESSION_UNCHECKED = 3
    FUNCTION_KEEP_SESSION_ALIVE = 4
    FUNCTION_RELEASE_OBJECT = 5
    FUNCTION_RELEASE_OBJECT_UNCHECKED = 6
    FUNCTION_ALLOCATE_STRING = 7
    FUNCTION_TRUNCATE_STRING = 8
    FUNCTION_GET_STRING_LENGTH = 9
    FUNCTION_SET_STRING_CHUNK = 10
    FUNCTION_GET_STRING_CHUNK = 11
    FUNCTION_ALLOCATE_LIST = 12
    FUNCTION_GET_LIST_LENGTH = 13
    FUNCTION_GET_LIST_ITEM = 14
    FUNCTION_APPEND_TO_LIST = 15
    FUNCTION_REMOVE_FROM_LIST = 16
    FUNCTION_OPEN_FILE = 17
    FUNCTION_CREATE_PIPE = 18
    FUNCTION_GET_FILE_INFO = 19
    FUNCTION_READ_FILE = 20
    FUNCTION_READ_FILE_ASYNC = 21
    FUNCTION_ABORT_ASYNC_FILE_READ = 22
    FUNCTION_WRITE_FILE = 23
    FUNCTION_WRITE_FILE_UNCHECKED = 24
    FUNCTION_WRITE_FILE_ASYNC = 25
    FUNCTION_SET_FILE_POSITION = 26
    FUNCTION_GET_FILE_POSITION = 27
    FUNCTION_SET_FILE_EVENTS = 28
    FUNCTION_GET_FILE_EVENTS = 29
    FUNCTION_OPEN_DIRECTORY = 33
    FUNCTION_GET_DIRECTORY_NAME = 34
    FUNCTION_GET_NEXT_DIRECTORY_ENTRY = 35
    FUNCTION_REWIND_DIRECTORY = 36
    FUNCTION_CREATE_DIRECTORY = 37
    FUNCTION_GET_PROCESSES = 38
    FUNCTION_SPAWN_PROCESS = 39
    FUNCTION_KILL_PROCESS = 40
    FUNCTION_GET_PROCESS_COMMAND = 41
    FUNCTION_GET_PROCESS_IDENTITY = 42
    FUNCTION_GET_PROCESS_STDIO = 43
    FUNCTION_GET_PROCESS_STATE = 44
    FUNCTION_GET_PROGRAMS = 46
    FUNCTION_DEFINE_PROGRAM = 47
    FUNCTION_PURGE_PROGRAM = 48
    FUNCTION_GET_PROGRAM_IDENTIFIER = 49
    FUNCTION_GET_PROGRAM_ROOT_DIRECTORY = 50
    FUNCTION_SET_PROGRAM_COMMAND = 51
    FUNCTION_GET_PROGRAM_COMMAND = 52
    FUNCTION_SET_PROGRAM_STDIO_REDIRECTION = 53
    FUNCTION_GET_PROGRAM_STDIO_REDIRECTION = 54
    FUNCTION_SET_PROGRAM_SCHEDULE = 55
    FUNCTION_GET_PROGRAM_SCHEDULE = 56
    FUNCTION_GET_PROGRAM_SCHEDULER_STATE = 57
    FUNCTION_CONTINUE_PROGRAM_SCHEDULE = 58
    FUNCTION_START_PROGRAM = 59
    FUNCTION_GET_LAST_SPAWNED_PROGRAM_PROCESS = 60
    FUNCTION_GET_CUSTOM_PROGRAM_OPTION_NAMES = 61
    FUNCTION_SET_CUSTOM_PROGRAM_OPTION_VALUE = 62
    FUNCTION_GET_CUSTOM_PROGRAM_OPTION_VALUE = 63
    FUNCTION_REMOVE_CUSTOM_PROGRAM_OPTION = 64
    FUNCTION_VISION_IS_VALID = 67
    FUNCTION_VISION_CAMERA_AVAILABLE = 68
    FUNCTION_VISION_CAMERA_ID_AVAILABLE = 69
    FUNCTION_VISION_CAMERA_ID_SELECT = 70
    FUNCTION_VISION_GET_FRAMESIZE = 71
    FUNCTION_VISION_SET_FRAMESIZE = 72
    FUNCTION_VISION_START_IDLE = 73
    FUNCTION_VISION_REQUEST_FRAMEPERIOD = 74
    FUNCTION_VISION_GET_FRAMEPERIOD = 75
    FUNCTION_VISION_STOP = 76
    FUNCTION_VISION_RESTART = 77
    FUNCTION_VISION_NUMERICAL_PARAMETER_SET = 78
    FUNCTION_VISION_NUMERICAL_PARAMETER_GET = 79
    FUNCTION_VISION_STRING_PARAMETER_SET = 80
    FUNCTION_VISION_STRING_PARAMETER_GET = 81
    FUNCTION_VISION_MODULE_START = 82
    FUNCTION_VISION_MODULE_STOP = 83
    FUNCTION_VISION_MODULE_RESTART = 84
    FUNCTION_VISION_MODULE_REMOVE = 85
    FUNCTION_VISION_MODULE_GET_NAME = 86
    FUNCTION_VISION_MODULE_GET_ID = 87
    FUNCTION_VISION_MODULE_IS_ACTIVE = 88
    FUNCTION_VISION_LIBS_COUNT = 89
    FUNCTION_VISION_LIBS_LOADED_COUNT = 90
    FUNCTION_VISION_LIB_NAME_PATH = 91
    FUNCTION_VISION_LIB_PARAMETERS_COUNT = 92
    FUNCTION_VISION_LIB_PARAMETER_DESCRIBE = 93
    FUNCTION_VISION_LIB_GET_USER_PREFIX = 94
    FUNCTION_VISION_LIB_SET_USER_PREFIX = 95
    FUNCTION_VISION_LIB_GET_SYSTEM_LOAD_PATH = 96
    FUNCTION_VISION_REMOVE_ALL_MODULES = 97
    FUNCTION_VISION_MODULE_RESULT = 98
    FUNCTION_VISION_SCENE_START = 99
    FUNCTION_VISION_SCENE_ADD = 100
    FUNCTION_VISION_SCENE_REMOVE = 101
    FUNCTION_VISION_GET_ERROR_DESCRIPTION = 102
    FUNCTION_VISION_GET_BUFFERED_RESULT = 103
    FUNCTION_GET_IDENTITY = 255

    ERROR_CODE_SUCCESS = 0
    ERROR_CODE_UNKNOWN_ERROR = 1
    ERROR_CODE_INVALID_OPERATION = 2
    ERROR_CODE_OPERATION_ABORTED = 3
    ERROR_CODE_INTERNAL_ERROR = 4
    ERROR_CODE_UNKNOWN_SESSION_ID = 5
    ERROR_CODE_NO_FREE_SESSION_ID = 6
    ERROR_CODE_UNKNOWN_OBJECT_ID = 7
    ERROR_CODE_NO_FREE_OBJECT_ID = 8
    ERROR_CODE_OBJECT_IS_LOCKED = 9
    ERROR_CODE_NO_MORE_DATA = 10
    ERROR_CODE_WRONG_LIST_ITEM_TYPE = 11
    ERROR_CODE_PROGRAM_IS_PURGED = 12
    ERROR_CODE_INVALID_PARAMETER = 128
    ERROR_CODE_NO_FREE_MEMORY = 129
    ERROR_CODE_NO_FREE_SPACE = 130
    ERROR_CODE_ACCESS_DENIED = 121
    ERROR_CODE_ALREADY_EXISTS = 132
    ERROR_CODE_DOES_NOT_EXIST = 133
    ERROR_CODE_INTERRUPTED = 134
    ERROR_CODE_IS_DIRECTORY = 135
    ERROR_CODE_NOT_A_DIRECTORY = 136
    ERROR_CODE_WOULD_BLOCK = 137
    ERROR_CODE_OVERFLOW = 138
    ERROR_CODE_BAD_FILE_DESCRIPTOR = 139
    ERROR_CODE_OUT_OF_RANGE = 140
    ERROR_CODE_NAME_TOO_LONG = 141
    ERROR_CODE_INVALID_SEEK = 142
    ERROR_CODE_NOT_SUPPORTED = 143
    ERROR_CODE_TOO_MANY_OPEN_FILES = 144
    OBJECT_TYPE_STRING = 0
    OBJECT_TYPE_LIST = 1
    OBJECT_TYPE_FILE = 2
    OBJECT_TYPE_DIRECTORY = 3
    OBJECT_TYPE_PROCESS = 4
    OBJECT_TYPE_PROGRAM = 5
    FILE_FLAG_READ_ONLY = 1
    FILE_FLAG_WRITE_ONLY = 2
    FILE_FLAG_READ_WRITE = 4
    FILE_FLAG_APPEND = 8
    FILE_FLAG_CREATE = 16
    FILE_FLAG_EXCLUSIVE = 32
    FILE_FLAG_NON_BLOCKING = 64
    FILE_FLAG_TRUNCATE = 128
    FILE_FLAG_TEMPORARY = 256
    FILE_FLAG_REPLACE = 512
    FILE_PERMISSION_USER_ALL = 448
    FILE_PERMISSION_USER_READ = 256
    FILE_PERMISSION_USER_WRITE = 128
    FILE_PERMISSION_USER_EXECUTE = 64
    FILE_PERMISSION_GROUP_ALL = 56
    FILE_PERMISSION_GROUP_READ = 32
    FILE_PERMISSION_GROUP_WRITE = 16
    FILE_PERMISSION_GROUP_EXECUTE = 8
    FILE_PERMISSION_OTHERS_ALL = 7
    FILE_PERMISSION_OTHERS_READ = 4
    FILE_PERMISSION_OTHERS_WRITE = 2
    FILE_PERMISSION_OTHERS_EXECUTE = 1
    PIPE_FLAG_NON_BLOCKING_READ = 1
    PIPE_FLAG_NON_BLOCKING_WRITE = 2
    FILE_TYPE_UNKNOWN = 0
    FILE_TYPE_REGULAR = 1
    FILE_TYPE_DIRECTORY = 2
    FILE_TYPE_CHARACTER = 3
    FILE_TYPE_BLOCK = 4
    FILE_TYPE_FIFO = 5
    FILE_TYPE_SYMLINK = 6
    FILE_TYPE_SOCKET = 7
    FILE_TYPE_PIPE = 8
    FILE_ORIGIN_BEGINNING = 0
    FILE_ORIGIN_CURRENT = 1
    FILE_ORIGIN_END = 2
    FILE_EVENT_READABLE = 1
    FILE_EVENT_WRITABLE = 2
    DIRECTORY_ENTRY_TYPE_UNKNOWN = 0
    DIRECTORY_ENTRY_TYPE_REGULAR = 1
    DIRECTORY_ENTRY_TYPE_DIRECTORY = 2
    DIRECTORY_ENTRY_TYPE_CHARACTER = 3
    DIRECTORY_ENTRY_TYPE_BLOCK = 4
    DIRECTORY_ENTRY_TYPE_FIFO = 5
    DIRECTORY_ENTRY_TYPE_SYMLINK = 6
    DIRECTORY_ENTRY_TYPE_SOCKET = 7
    DIRECTORY_FLAG_RECURSIVE = 1
    DIRECTORY_FLAG_EXCLUSIVE = 2
    PROCESS_SIGNAL_INTERRUPT = 2
    PROCESS_SIGNAL_QUIT = 3
    PROCESS_SIGNAL_ABORT = 6
    PROCESS_SIGNAL_KILL = 9
    PROCESS_SIGNAL_USER1 = 10
    PROCESS_SIGNAL_USER2 = 12
    PROCESS_SIGNAL_TERMINATE = 15
    PROCESS_SIGNAL_CONTINUE = 18
    PROCESS_SIGNAL_STOP = 19
    PROCESS_STATE_UNKNOWN = 0
    PROCESS_STATE_RUNNING = 1
    PROCESS_STATE_ERROR = 2
    PROCESS_STATE_EXITED = 3
    PROCESS_STATE_KILLED = 4
    PROCESS_STATE_STOPPED = 5
    PROGRAM_STDIO_REDIRECTION_DEV_NULL = 0
    PROGRAM_STDIO_REDIRECTION_PIPE = 1
    PROGRAM_STDIO_REDIRECTION_FILE = 2
    PROGRAM_STDIO_REDIRECTION_INDIVIDUAL_LOG = 3
    PROGRAM_STDIO_REDIRECTION_CONTINUOUS_LOG = 4
    PROGRAM_STDIO_REDIRECTION_STDOUT = 5
    PROGRAM_START_MODE_NEVER = 0
    PROGRAM_START_MODE_ALWAYS = 1
    PROGRAM_START_MODE_INTERVAL = 2
    PROGRAM_START_MODE_CRON = 3
    PROGRAM_SCHEDULER_STATE_STOPPED = 0
    PROGRAM_SCHEDULER_STATE_RUNNING = 1

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickRED.FUNCTION_CREATE_SESSION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_EXPIRE_SESSION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_EXPIRE_SESSION_UNCHECKED] = BrickRED.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickRED.FUNCTION_KEEP_SESSION_ALIVE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_RELEASE_OBJECT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_RELEASE_OBJECT_UNCHECKED] = BrickRED.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickRED.FUNCTION_ALLOCATE_STRING] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_TRUNCATE_STRING] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_STRING_LENGTH] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_STRING_CHUNK] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_STRING_CHUNK] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_ALLOCATE_LIST] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_LIST_LENGTH] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_LIST_ITEM] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_APPEND_TO_LIST] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_REMOVE_FROM_LIST] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_OPEN_FILE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_CREATE_PIPE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_FILE_INFO] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_READ_FILE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_READ_FILE_ASYNC] = BrickRED.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickRED.FUNCTION_ABORT_ASYNC_FILE_READ] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_WRITE_FILE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_WRITE_FILE_UNCHECKED] = BrickRED.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickRED.FUNCTION_WRITE_FILE_ASYNC] = BrickRED.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickRED.FUNCTION_SET_FILE_POSITION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_FILE_POSITION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_FILE_EVENTS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_FILE_EVENTS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.CALLBACK_ASYNC_FILE_READ] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.CALLBACK_ASYNC_FILE_WRITE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.CALLBACK_FILE_EVENTS_OCCURRED] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.FUNCTION_OPEN_DIRECTORY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_DIRECTORY_NAME] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_NEXT_DIRECTORY_ENTRY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_REWIND_DIRECTORY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_CREATE_DIRECTORY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROCESSES] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SPAWN_PROCESS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_KILL_PROCESS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROCESS_COMMAND] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROCESS_IDENTITY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROCESS_STDIO] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROCESS_STATE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.CALLBACK_PROCESS_STATE_CHANGED] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAMS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_DEFINE_PROGRAM] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_PURGE_PROGRAM] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_IDENTIFIER] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_ROOT_DIRECTORY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_PROGRAM_COMMAND] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_COMMAND] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_PROGRAM_STDIO_REDIRECTION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_STDIO_REDIRECTION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_PROGRAM_SCHEDULE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_SCHEDULE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_PROGRAM_SCHEDULER_STATE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_CONTINUE_PROGRAM_SCHEDULE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_START_PROGRAM] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_LAST_SPAWNED_PROGRAM_PROCESS] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_CUSTOM_PROGRAM_OPTION_NAMES] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_SET_CUSTOM_PROGRAM_OPTION_VALUE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_GET_CUSTOM_PROGRAM_OPTION_VALUE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_REMOVE_CUSTOM_PROGRAM_OPTION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.CALLBACK_PROGRAM_SCHEDULER_STATE_CHANGED] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.CALLBACK_PROGRAM_PROCESS_SPAWNED] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.FUNCTION_VISION_IS_VALID] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_CAMERA_AVAILABLE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_CAMERA_ID_AVAILABLE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_CAMERA_ID_SELECT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_GET_FRAMESIZE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_SET_FRAMESIZE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_START_IDLE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_REQUEST_FRAMEPERIOD] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_GET_FRAMEPERIOD] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_STOP] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_RESTART] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_NUMERICAL_PARAMETER_SET] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_NUMERICAL_PARAMETER_GET] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_STRING_PARAMETER_SET] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_STRING_PARAMETER_GET] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_START] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_STOP] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_RESTART] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_REMOVE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_GET_NAME] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_GET_ID] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_IS_ACTIVE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIBS_COUNT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIBS_LOADED_COUNT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_NAME_PATH] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_PARAMETERS_COUNT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_PARAMETER_DESCRIBE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_GET_USER_PREFIX] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_SET_USER_PREFIX] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_LIB_GET_SYSTEM_LOAD_PATH] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_REMOVE_ALL_MODULES] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_MODULE_RESULT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_SCENE_START] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_SCENE_ADD] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_SCENE_REMOVE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_GET_ERROR_DESCRIPTION] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.FUNCTION_VISION_GET_BUFFERED_RESULT] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickRED.CALLBACK_VISION_LIBRARIES] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.CALLBACK_VISION_MODULE] = BrickRED.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickRED.FUNCTION_GET_IDENTITY] = BrickRED.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickRED.CALLBACK_ASYNC_FILE_READ] = 'H B 60B B'
        self.callback_formats[BrickRED.CALLBACK_ASYNC_FILE_WRITE] = 'H B B'
        self.callback_formats[BrickRED.CALLBACK_FILE_EVENTS_OCCURRED] = 'H H'
        self.callback_formats[BrickRED.CALLBACK_PROCESS_STATE_CHANGED] = 'H B Q B'
        self.callback_formats[BrickRED.CALLBACK_PROGRAM_SCHEDULER_STATE_CHANGED] = 'H'
        self.callback_formats[BrickRED.CALLBACK_PROGRAM_PROCESS_SPAWNED] = 'H'
        self.callback_formats[BrickRED.CALLBACK_VISION_LIBRARIES] = '30s 30s b'
        self.callback_formats[BrickRED.CALLBACK_VISION_MODULE] = 'b i i i i 30s'

    def create_session(self, lifetime):
        """
        
        """
        return CreateSession(*self.ipcon.send_request(self, BrickRED.FUNCTION_CREATE_SESSION, (lifetime,), 'I', 'B H'))

    def expire_session(self, session_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_EXPIRE_SESSION, (session_id,), 'H', 'B')

    def expire_session_unchecked(self, session_id):
        """
        
        """
        self.ipcon.send_request(self, BrickRED.FUNCTION_EXPIRE_SESSION_UNCHECKED, (session_id,), 'H', '')

    def keep_session_alive(self, session_id, lifetime):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_KEEP_SESSION_ALIVE, (session_id, lifetime), 'H I', 'B')

    def release_object(self, object_id, session_id):
        """
        Decreases the reference count of an object by one and returns the resulting
        error code. If the reference count reaches zero the object gets destroyed.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_RELEASE_OBJECT, (object_id, session_id), 'H H', 'B')

    def release_object_unchecked(self, object_id, session_id):
        """
        
        """
        self.ipcon.send_request(self, BrickRED.FUNCTION_RELEASE_OBJECT_UNCHECKED, (object_id, session_id), 'H H', '')

    def allocate_string(self, length_to_reserve, buffer, session_id):
        """
        Allocates a new string object, reserves ``length_to_reserve`` bytes memory
        for it and sets up to the first 60 bytes. Set ``length_to_reserve`` to the
        length of the string that should be stored in the string object.
        
        Returns the object ID of the new string object and the resulting error code.
        """
        return AllocateString(*self.ipcon.send_request(self, BrickRED.FUNCTION_ALLOCATE_STRING, (length_to_reserve, buffer, session_id), 'I 58s H', 'B H'))

    def truncate_string(self, string_id, length):
        """
        Truncates a string object to ``length`` bytes and returns the resulting
        error code.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_TRUNCATE_STRING, (string_id, length), 'H I', 'B')

    def get_string_length(self, string_id):
        """
        Returns the length of a string object in bytes and the resulting error code.
        """
        return GetStringLength(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_STRING_LENGTH, (string_id,), 'H', 'B I'))

    def set_string_chunk(self, string_id, offset, buffer):
        """
        Sets a chunk of up to 58 bytes in a string object beginning at ``offset``.
        
        Returns the resulting error code.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_STRING_CHUNK, (string_id, offset, buffer), 'H I 58s', 'B')

    def get_string_chunk(self, string_id, offset):
        """
        Returns a chunk up to 63 bytes from a string object beginning at ``offset`` and
        returns the resulting error code.
        """
        return GetStringChunk(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_STRING_CHUNK, (string_id, offset), 'H I', 'B 63s'))

    def allocate_list(self, length_to_reserve, session_id):
        """
        Allocates a new list object and reserves memory for ``length_to_reserve``
        items. Set ``length_to_reserve`` to the number of items that should be stored
        in the list object.
        
        Returns the object ID of the new list object and the resulting error code.
        
        When a list object gets destroyed then the reference count of each object in
        the list object is decreased by one.
        """
        return AllocateList(*self.ipcon.send_request(self, BrickRED.FUNCTION_ALLOCATE_LIST, (length_to_reserve, session_id), 'H H', 'B H'))

    def get_list_length(self, list_id):
        """
        Returns the length of a list object in items and the resulting error code.
        """
        return GetListLength(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_LIST_LENGTH, (list_id,), 'H', 'B H'))

    def get_list_item(self, list_id, index, session_id):
        """
        Returns the object ID and type of the object stored at ``index`` in a list
        object and returns the resulting error code.
        
        Possible object types are:
        
        * String = 0
        * List = 1
        * File = 2
        * Directory = 3
        * Process = 4
        * Program = 5
        """
        return GetListItem(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_LIST_ITEM, (list_id, index, session_id), 'H H H', 'B H B'))

    def append_to_list(self, list_id, item_object_id):
        """
        Appends an object to a list object and increases the reference count of the
        appended object by one.
        
        Returns the resulting error code.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_APPEND_TO_LIST, (list_id, item_object_id), 'H H', 'B')

    def remove_from_list(self, list_id, index):
        """
        Removes the object stored at ``index`` from a list object and decreases the
        reference count of the removed object by one.
        
        Returns the resulting error code.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_REMOVE_FROM_LIST, (list_id, index), 'H H', 'B')

    def open_file(self, name_string_id, flags, permissions, uid, gid, session_id):
        """
        Opens an existing file or creates a new file and allocates a new file object
        for it.
        
        FIXME: name has to be absolute
        
        The reference count of the name string object is increased by one. When the
        file object gets destroyed then the reference count of the name string object is
        decreased by one. Also the name string object is locked and cannot be modified
        while the file object holds a reference to it.
        
        The ``flags`` parameter takes a ORed combination of the following possible file
        flags (in hexadecimal notation):
        
        * ReadOnly = 0x0001 (O_RDONLY)
        * WriteOnly = 0x0002 (O_WRONLY)
        * ReadWrite = 0x0004 (O_RDWR)
        * Append = 0x0008 (O_APPEND)
        * Create = 0x0010 (O_CREAT)
        * Exclusive = 0x0020 (O_EXCL)
        * NonBlocking = 0x0040 (O_NONBLOCK)
        * Truncate = 0x0080 (O_TRUNC)
        * Temporary = 0x0100
        * Replace = 0x0200
        
        FIXME: explain *Temporary* and *Replace* flag
        
        The ``permissions`` parameter takes a ORed combination of the following
        possible file permissions (in octal notation) that match the common UNIX
        permission bits:
        
        * UserRead = 00400
        * UserWrite = 00200
        * UserExecute = 00100
        * GroupRead = 00040
        * GroupWrite = 00020
        * GroupExecute = 00010
        * OthersRead = 00004
        * OthersWrite = 00002
        * OthersExecute = 00001
        
        Returns the object ID of the new file object and the resulting error code.
        """
        return OpenFile(*self.ipcon.send_request(self, BrickRED.FUNCTION_OPEN_FILE, (name_string_id, flags, permissions, uid, gid, session_id), 'H I H I I H', 'B H'))

    def create_pipe(self, flags, length, session_id):
        """
        Creates a new pipe and allocates a new file object for it.
        
        The ``flags`` parameter takes a ORed combination of the following possible
        pipe flags (in hexadecimal notation):
        
        * NonBlockingRead = 0x0001
        * NonBlockingWrite = 0x0002
        
        The length of the pipe buffer can be specified with the ``length`` parameter
        in bytes. If length is set to zero, then the default pipe buffer length is used.
        
        Returns the object ID of the new file object and the resulting error code.
        """
        return CreatePipe(*self.ipcon.send_request(self, BrickRED.FUNCTION_CREATE_PIPE, (flags, length, session_id), 'I Q H', 'B H'))

    def get_file_info(self, file_id, session_id):
        """
        Returns various information about a file and the resulting error code.
        
        Possible file types are:
        
        * Unknown = 0
        * Regular = 1
        * Directory = 2
        * Character = 3
        * Block = 4
        * FIFO = 5
        * Symlink = 6
        * Socket = 7
        * Pipe = 8
        
        If the file type is *Pipe* then the returned name string object is invalid,
        because a pipe has no name. Otherwise the returned name string object was used
        to open or create the file object, as passed to :func:`OpenFile`.
        
        The returned flags were used to open or create the file object, as passed to
        :func:`OpenFile` or :func:`CreatePipe`. See the respective function for a list
        of possible file and pipe flags.
        
        FIXME: everything except flags and length is invalid if file type is *Pipe*
        """
        return GetFileInfo(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_FILE_INFO, (file_id, session_id), 'H H', 'B B H I H I I Q Q Q Q'))

    def read_file(self, file_id, length_to_read):
        """
        Reads up to 62 bytes from a file object.
        
        Returns the bytes read, the actual number of bytes read and the resulting
        error code.
        
        If there is not data to be read, either because the file position reached
        end-of-file or because there is not data in the pipe, then zero bytes are
        returned.
        
        If the file object was created by :func:`OpenFile` without the *NonBlocking*
        flag or by :func:`CreatePipe` without the *NonBlockingRead* flag then the
        error code *NotSupported* is returned.
        """
        return ReadFile(*self.ipcon.send_request(self, BrickRED.FUNCTION_READ_FILE, (file_id, length_to_read), 'H B', 'B 62B B'))

    def read_file_async(self, file_id, length_to_read):
        """
        Reads up to 2\ :sup:`63`\  - 1 bytes from a file object asynchronously.
        
        Reports the bytes read (in 60 byte chunks), the actual number of bytes read and
        the resulting error code via the :func:`AsyncFileRead` callback.
        
        If there is not data to be read, either because the file position reached
        end-of-file or because there is not data in the pipe, then zero bytes are
        reported.
        
        If the file object was created by :func:`OpenFile` without the *NonBlocking*
        flag or by :func:`CreatePipe` without the *NonBlockingRead* flag then the error
        code *NotSupported* is reported via the :func:`AsyncFileRead` callback.
        """
        self.ipcon.send_request(self, BrickRED.FUNCTION_READ_FILE_ASYNC, (file_id, length_to_read), 'H Q', '')

    def abort_async_file_read(self, file_id):
        """
        Aborts a :func:`ReadFileAsync` operation in progress.
        
        Returns the resulting error code.
        
        On success the :func:`AsyncFileRead` callback will report *OperationAborted*.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_ABORT_ASYNC_FILE_READ, (file_id,), 'H', 'B')

    def write_file(self, file_id, buffer, length_to_write):
        """
        Writes up to 61 bytes to a file object.
        
        Returns the actual number of bytes written and the resulting error code.
        
        If the file object was created by :func:`OpenFile` without the *NonBlocking*
        flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
        error code *NotSupported* is returned.
        """
        return WriteFile(*self.ipcon.send_request(self, BrickRED.FUNCTION_WRITE_FILE, (file_id, buffer, length_to_write), 'H 61B B', 'B B'))

    def write_file_unchecked(self, file_id, buffer, length_to_write):
        """
        Writes up to 61 bytes to a file object.
        
        Does neither report the actual number of bytes written nor the resulting error
        code.
        
        If the file object was created by :func:`OpenFile` without the *NonBlocking*
        flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
        write operation will fail silently.
        """
        self.ipcon.send_request(self, BrickRED.FUNCTION_WRITE_FILE_UNCHECKED, (file_id, buffer, length_to_write), 'H 61B B', '')

    def write_file_async(self, file_id, buffer, length_to_write):
        """
        Writes up to 61 bytes to a file object.
        
        Reports the actual number of bytes written and the resulting error code via the
        :func:`AsyncFileWrite` callback.
        
        If the file object was created by :func:`OpenFile` without the *NonBlocking*
        flag or by :func:`CreatePipe` without the *NonBlockingWrite* flag then the
        error code *NotSupported* is reported via the :func:`AsyncFileWrite` callback.
        """
        self.ipcon.send_request(self, BrickRED.FUNCTION_WRITE_FILE_ASYNC, (file_id, buffer, length_to_write), 'H 61B B', '')

    def set_file_position(self, file_id, offset, origin):
        """
        Set the current seek position of a file object in bytes relative to ``origin``.
        
        Possible file origins are:
        
        * Beginning = 0
        * Current = 1
        * End = 2
        
        Returns the resulting absolute seek position and error code.
        
        If the file object was created by :func:`CreatePipe` then it has no seek
        position and the error code *InvalidSeek* is returned.
        """
        return SetFilePosition(*self.ipcon.send_request(self, BrickRED.FUNCTION_SET_FILE_POSITION, (file_id, offset, origin), 'H q B', 'B Q'))

    def get_file_position(self, file_id):
        """
        Returns the current seek position of a file object in bytes and returns the
        resulting error code.
        
        If the file object was created by :func:`CreatePipe` then it has no seek
        position and the error code *InvalidSeek* is returned.
        """
        return GetFilePosition(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_FILE_POSITION, (file_id,), 'H', 'B Q'))

    def set_file_events(self, file_id, events):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_FILE_EVENTS, (file_id, events), 'H H', 'B')

    def get_file_events(self, file_id):
        """
        
        """
        return GetFileEvents(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_FILE_EVENTS, (file_id,), 'H', 'B H'))

    def open_directory(self, name_string_id, session_id):
        """
        Opens an existing directory and allocates a new directory object for it.
        
        FIXME: name has to be absolute
        
        The reference count of the name string object is increased by one. When the
        directory object is destroyed then the reference count of the name string
        object is decreased by one. Also the name string object is locked and cannot be
        modified while the directory object holds a reference to it.
        
        Returns the object ID of the new directory object and the resulting error code.
        """
        return OpenDirectory(*self.ipcon.send_request(self, BrickRED.FUNCTION_OPEN_DIRECTORY, (name_string_id, session_id), 'H H', 'B H'))

    def get_directory_name(self, directory_id, session_id):
        """
        Returns the name of a directory object, as passed to :func:`OpenDirectory`, and
        the resulting error code.
        """
        return GetDirectoryName(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_DIRECTORY_NAME, (directory_id, session_id), 'H H', 'B H'))

    def get_next_directory_entry(self, directory_id, session_id):
        """
        Returns the next entry in a directory object and the resulting error code.
        
        If there is not next entry then error code *NoMoreData* is returned. To rewind
        a directory object call :func:`RewindDirectory`.
        
        Possible directory entry types are:
        
        * Unknown = 0
        * Regular = 1
        * Directory = 2
        * Character = 3
        * Block = 4
        * FIFO = 5
        * Symlink = 6
        * Socket = 7
        """
        return GetNextDirectoryEntry(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_NEXT_DIRECTORY_ENTRY, (directory_id, session_id), 'H H', 'B H B'))

    def rewind_directory(self, directory_id):
        """
        Rewinds a directory object and returns the resulting error code.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_REWIND_DIRECTORY, (directory_id,), 'H', 'B')

    def create_directory(self, name_string_id, flags, permissions, uid, gid):
        """
        FIXME: name has to be absolute
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_CREATE_DIRECTORY, (name_string_id, flags, permissions, uid, gid), 'H I H I I', 'B')

    def get_processes(self, session_id):
        """
        
        """
        return GetProcesses(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROCESSES, (session_id,), 'H', 'B H'))

    def spawn_process(self, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id, uid, gid, stdin_file_id, stdout_file_id, stderr_file_id, session_id):
        """
        
        """
        return SpawnProcess(*self.ipcon.send_request(self, BrickRED.FUNCTION_SPAWN_PROCESS, (executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id, uid, gid, stdin_file_id, stdout_file_id, stderr_file_id, session_id), 'H H H H I I H H H H', 'B H'))

    def kill_process(self, process_id, signal):
        """
        Sends a UNIX signal to a process object and returns the resulting error code.
        
        Possible UNIX signals are:
        
        * Interrupt = 2
        * Quit = 3
        * Abort = 6
        * Kill = 9
        * User1 = 10
        * User2 = 12
        * Terminate = 15
        * Continue =  18
        * Stop = 19
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_KILL_PROCESS, (process_id, signal), 'H B', 'B')

    def get_process_command(self, process_id, session_id):
        """
        Returns the executable, arguments, environment and working directory used to
        spawn a process object, as passed to :func:`SpawnProcess`, and the resulting
        error code.
        """
        return GetProcessCommand(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROCESS_COMMAND, (process_id, session_id), 'H H', 'B H H H H'))

    def get_process_identity(self, process_id):
        """
        Returns the process ID and the user and group ID used to spawn a process object,
        as passed to :func:`SpawnProcess`, and the resulting error code.
        
        The process ID is only valid if the state is *Running* or *Stopped*, see
        :func:`GetProcessState`.
        """
        return GetProcessIdentity(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROCESS_IDENTITY, (process_id,), 'H', 'B I I I'))

    def get_process_stdio(self, process_id, session_id):
        """
        Returns the stdin, stdout and stderr files used to spawn a process object, as
        passed to :func:`SpawnProcess`, and the resulting error code.
        """
        return GetProcessStdio(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROCESS_STDIO, (process_id, session_id), 'H H', 'B H H H'))

    def get_process_state(self, process_id):
        """
        Returns the current state, timestamp and exit code of a process object, and
        the resulting error code.
        
        Possible process states are:
        
        * Unknown = 0
        * Running = 1
        * Error = 2
        * Exited = 3
        * Killed = 4
        * Stopped = 5
        
        The timestamp represents the UNIX time since when the process is in its current
        state.
        
        The exit code is only valid if the state is *Error*, *Exited*, *Killed* or
        *Stopped* and has different meanings depending on the state:
        
        * Error: error code for error occurred while spawning the process (see below)
        * Exited: exit status of the process
        * Killed: UNIX signal number used to kill the process
        * Stopped: UNIX signal number used to stop the process
        
        Possible exit/error codes in *Error* state are:
        
        * InternalError = 125
        * CannotExecute = 126
        * DoesNotExist = 127
        
        The *CannotExecute* error can be caused by the executable being opened for
        writing.
        """
        return GetProcessState(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROCESS_STATE, (process_id,), 'H', 'B B Q B'))

    def get_programs(self, session_id):
        """
        
        """
        return GetPrograms(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAMS, (session_id,), 'H', 'B H'))

    def define_program(self, identifier_string_id, session_id):
        """
        
        """
        return DefineProgram(*self.ipcon.send_request(self, BrickRED.FUNCTION_DEFINE_PROGRAM, (identifier_string_id, session_id), 'H H', 'B H'))

    def purge_program(self, program_id, cookie):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_PURGE_PROGRAM, (program_id, cookie), 'H I', 'B')

    def get_program_identifier(self, program_id, session_id):
        """
        
        """
        return GetProgramIdentifier(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_IDENTIFIER, (program_id, session_id), 'H H', 'B H'))

    def get_program_root_directory(self, program_id, session_id):
        """
        FIXME: root directory is absolute: <home>/programs/<identifier>
        """
        return GetProgramRootDirectory(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_ROOT_DIRECTORY, (program_id, session_id), 'H H', 'B H'))

    def set_program_command(self, program_id, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id):
        """
        FIXME: working directory is relative to <home>/programs/<identifier>/bin
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_PROGRAM_COMMAND, (program_id, executable_string_id, arguments_list_id, environment_list_id, working_directory_string_id), 'H H H H H', 'B')

    def get_program_command(self, program_id, session_id):
        """
        FIXME: working directory is relative to <home>/programs/<identifier>/bin
        """
        return GetProgramCommand(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_COMMAND, (program_id, session_id), 'H H', 'B H H H H'))

    def set_program_stdio_redirection(self, program_id, stdin_redirection, stdin_file_name_string_id, stdout_redirection, stdout_file_name_string_id, stderr_redirection, stderr_file_name_string_id):
        """
        FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_PROGRAM_STDIO_REDIRECTION, (program_id, stdin_redirection, stdin_file_name_string_id, stdout_redirection, stdout_file_name_string_id, stderr_redirection, stderr_file_name_string_id), 'H B H B H B H', 'B')

    def get_program_stdio_redirection(self, program_id, session_id):
        """
        FIXME: stdio file names are relative to <home>/programs/<identifier>/bin
        """
        return GetProgramStdioRedirection(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_STDIO_REDIRECTION, (program_id, session_id), 'H H', 'B B H B H B H'))

    def set_program_schedule(self, program_id, start_mode, continue_after_error, start_interval, start_fields_string_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_PROGRAM_SCHEDULE, (program_id, start_mode, continue_after_error, start_interval, start_fields_string_id), 'H B ? I H', 'B')

    def get_program_schedule(self, program_id, session_id):
        """
        
        """
        return GetProgramSchedule(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_SCHEDULE, (program_id, session_id), 'H H', 'B B ? I H'))

    def get_program_scheduler_state(self, program_id, session_id):
        """
        FIXME: message is currently valid in error-occurred state only
        """
        return GetProgramSchedulerState(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_PROGRAM_SCHEDULER_STATE, (program_id, session_id), 'H H', 'B B Q H'))

    def continue_program_schedule(self, program_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_CONTINUE_PROGRAM_SCHEDULE, (program_id,), 'H', 'B')

    def start_program(self, program_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_START_PROGRAM, (program_id,), 'H', 'B')

    def get_last_spawned_program_process(self, program_id, session_id):
        """
        
        """
        return GetLastSpawnedProgramProcess(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_LAST_SPAWNED_PROGRAM_PROCESS, (program_id, session_id), 'H H', 'B H Q'))

    def get_custom_program_option_names(self, program_id, session_id):
        """
        
        """
        return GetCustomProgramOptionNames(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_CUSTOM_PROGRAM_OPTION_NAMES, (program_id, session_id), 'H H', 'B H'))

    def set_custom_program_option_value(self, program_id, name_string_id, value_string_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_SET_CUSTOM_PROGRAM_OPTION_VALUE, (program_id, name_string_id, value_string_id), 'H H H', 'B')

    def get_custom_program_option_value(self, program_id, name_string_id, session_id):
        """
        
        """
        return GetCustomProgramOptionValue(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_CUSTOM_PROGRAM_OPTION_VALUE, (program_id, name_string_id, session_id), 'H H H', 'B H'))

    def remove_custom_program_option(self, program_id, name_string_id):
        """
        
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_REMOVE_CUSTOM_PROGRAM_OPTION, (program_id, name_string_id), 'H H', 'B')

    def vision_is_valid(self):
        """
        Check if the library is valid. Should be called once before usage.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_IS_VALID, (), '', 'h')

    def vision_camera_available(self):
        """
        Check if any camera device is available.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_CAMERA_AVAILABLE, (), '', 'h')

    def vision_camera_id_available(self, device):
        """
        Check if a specific camera device is available.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_CAMERA_ID_AVAILABLE, (device,), 'b', 'h')

    def vision_camera_id_select(self, device):
        """
        If several cameras are available, select the preferred one.  If that device
        is not available, another one may still be used.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_CAMERA_ID_SELECT, (device,), 'b', 'h')

    def vision_get_framesize(self):
        """
        Request the resolution of the camera frames.  This can only be called once
        the camera is active, so in particular, if the resolution needs to be known
        before a module can be started, vision_start_idle() must be called.
        """
        return VisionGetFramesize(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_GET_FRAMESIZE, (), '', 'h H H'))

    def vision_set_framesize(self, width, height):
        """
        Selects a framesize WxH.
        This will temporarily stop and restart all active modules.
        If the requested framesize is not available, the settings will be restored
        to the last valid settings, if any.  If no module is running, the camera
        will just be tested.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_SET_FRAMESIZE, (width, height), 'H H', 'h')

    def vision_start_idle(self):
        """
        Starts a dummy module keeping the Api up and running even if no 'real' module
        is active.  This can be used to block the camera or if the resolution has to
        be known before any module is running.  Subsequent calls will not start
        another dummy.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_START_IDLE, (), '', 'h')

    def vision_request_frameperiod(self, milliseconds):
        """
        Set the minimum inverse frame frequency. Vision modules registered
        and started in the api will be executed sequentially during one
        execution loop. The execution latency set here is the minimum
        delay between two loops, i.e. the minimum inverse framerate
        (frames are grabbed once at the beginning of each loop).
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_REQUEST_FRAMEPERIOD, (milliseconds,), 'I', 'h')

    def vision_get_frameperiod(self):
        """
        Get the effective frameperiod, which can be larger than the frameperiod
        requested.
        """
        return VisionGetFrameperiod(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_GET_FRAMEPERIOD, (), '', 'h I'))

    def vision_stop(self):
        """
        Pause Tinkervision, deactivating (but not disabling) every module.  The camera will
        be released and no further callbacks will be executed, but on vision_restart(), the Api
        will be found in the exact same state as left (assuming that the camera can
        be acquired again).
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_STOP, (), '', 'h')

    def vision_restart(self):
        """
        Restart Tinkervision from paused state, initiated through call to vision_stop().
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_RESTART, (), '', 'h')

    def vision_numerical_parameter_set(self, id, parameter, value):
        """
        Set the value of a numerical parameter of a specific module.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_NUMERICAL_PARAMETER_SET, (id, parameter, value), 'b 30s i', 'h')

    def vision_numerical_parameter_get(self, id, parameter):
        """
        Get the value of a numerical parameter of a specific module.
        """
        return VisionNumericalParameterGet(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_NUMERICAL_PARAMETER_GET, (id, parameter), 'b 30s', 'h i'))

    def vision_string_parameter_set(self, id, parameter, value):
        """
        Set the value of a string parameter of a specific module.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_STRING_PARAMETER_SET, (id, parameter, value), 'b 30s 30s', 'h')

    def vision_string_parameter_get(self, id, parameter):
        """
        Get the value of a string parameter of a specific module.
        """
        return VisionStringParameterGet(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_STRING_PARAMETER_GET, (id, parameter), 'b 30s', 'h 30s'))

    def vision_module_start(self, name):
        """
        Start a vision module identified by its library name.
        The requested module will be loaded and started if it is found in one of the
        available library search paths (system/user).
        On success, it will be assigned a unique id.
        """
        return VisionModuleStart(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_START, (name,), '30s', 'h b'))

    def vision_module_stop(self, id):
        """
        Disable a module without removing it.
        A disabled module won't be executed, but it is still available for
        configuration or reactivation. The associated camera will be released if it
        is not used by other modules.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_STOP, (id,), 'b', 'h')

    def vision_module_restart(self, id):
        """
        Restart a module that has been stopped with module_stop().
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_RESTART, (id,), 'b', 'h')

    def vision_module_remove(self, id):
        """
        Deactivate and remove a module.
        The id of a removed module is invalid afterwards.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_REMOVE, (id,), 'b', 'h')

    def vision_module_get_name(self, id):
        """
        Get the name of a loaded module.
        """
        return VisionModuleGetName(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_GET_NAME, (id,), 'b', 'h 30s'))

    def vision_module_get_id(self, library):
        """
        Retrieve the id of a loaded library.
        """
        return VisionModuleGetID(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_GET_ID, (library,), 'h', 'h b'))

    def vision_module_is_active(self, id):
        """
        Check if a loaded module is active, i.e. actually running.
        """
        return VisionModuleIsActive(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_IS_ACTIVE, (id,), 'b', 'h B'))

    def vision_libs_count(self):
        """
        Get the number of currently available libraries.
        This can be used to iterate through all libraries using
        vision_lib_name_path().
        """
        return VisionLibsCount(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIBS_COUNT, (), '', 'h H'))

    def vision_libs_loaded_count(self):
        """
        Retrieve the number of loaded libraries.
        The result can be used with vision_module_get_id().
        """
        return VisionLibsLoadedCount(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIBS_LOADED_COUNT, (), '', 'h H'))

    def vision_lib_name_path(self, number):
        """
        Get the name and load path of an available library.
        Pass a number smaller then vision_libs_count.
        """
        return VisionLibNamePath(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_NAME_PATH, (number,), 'H', 'h 30s 30s'))

    def vision_lib_parameters_count(self, lib):
        """
        Get the number of parameters a library supports.
        """
        return VisionLibParametersCount(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_PARAMETERS_COUNT, (lib,), '30s', 'h H'))

    def vision_lib_parameter_describe(self, libname, parameter):
        """
        Get the properties of a parameter from a library. type is 0 for numeric parameters,
        1 for string parameters. min, max, default are only valid in the first case.
        """
        return VisionLibParameterDescribe(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_PARAMETER_DESCRIBE, (libname, parameter), '30s H', 'h 30s B i i i'))

    def vision_lib_get_user_prefix(self):
        """
        Access the currently set user paths prefix.
        """
        return VisionLibGetUserPrefix(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_GET_USER_PREFIX, (), '', 'h 30s'))

    def vision_lib_set_user_prefix(self, path):
        """
        Set the user paths prefix from an existing path. The directory has to
        provide the subdirectories lib (path searched for user modules), data
        (default path to store or load data or frames from) and scripts (path used to load
        python scripts from).
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_SET_USER_PREFIX, (path,), '30s', 'h')

    def vision_lib_get_system_load_path(self):
        """
        Access the fixed system module load path.
        """
        return VisionLibGetSystemLoadPath(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_LIB_GET_SYSTEM_LOAD_PATH, (), '', 'h 30s'))

    def vision_remove_all_modules(self):
        """
        Disable, remove and destroy all modules.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_REMOVE_ALL_MODULES, (), '', 'h')

    def vision_module_result(self, module_id):
        """
        Get the result of the latest execution of a given module.
        """
        return VisionModuleResult(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_MODULE_RESULT, (module_id,), 'b', 'h i i i i 30s'))

    def vision_scene_start(self, module_id):
        """
        Start a new scene given a loaded module.
        """
        return VisionSceneStart(*self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_SCENE_START, (module_id,), 'b', 'h h'))

    def vision_scene_add(self, scene_id, module_id):
        """
        Add a module to an existing scene.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_SCENE_ADD, (scene_id, module_id), 'h b', 'h')

    def vision_scene_remove(self, scene_id):
        """
        Remove a scene without affecting the associated modules.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_SCENE_REMOVE, (scene_id,), 'h', 'h')

    def vision_get_error_description(self, code):
        """
        Get a string representation of a result code. All api functions return 0 on success,
        and a negative value on error.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_GET_ERROR_DESCRIPTION, (code,), 'h', '30s')

    def vision_get_buffered_result(self):
        """
        If any vision method returned 1, the requested operation took too long and is running
        in the background.  This method can then be called until a different result is
        returned.
        """
        return self.ipcon.send_request(self, BrickRED.FUNCTION_VISION_GET_BUFFERED_RESULT, (), '', 'h')

    def get_identity(self):
        """
        Returns the UID, the UID where the Brick is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be '0'-'8' (stack position).
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickRED.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

RED = BrickRED # for backward compatibility
