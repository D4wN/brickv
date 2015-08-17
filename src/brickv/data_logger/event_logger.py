"""
/*---------------------------------------------------------------------------
                                Event Logger
 ---------------------------------------------------------------------------*/
"""
from PyQt4 import QtCore
import logging
import datetime
from PyQt4.QtCore import SIGNAL


class EventLogger():
    """
        Basic EventLogger class.
    """

    EVENT_CONSOLE_LOGGING = True  # for logging to the console
    EVENT_FILE_LOGGING = True  # for event logging in to a file
    EVENT_FILE_LOGGING_PATH = "data_logger.log"  # default file path for logging events
    EVENT_LOG_LEVEL = logging.DEBUG

    format = "%(asctime)s - %(levelname)8s - %(message)s"
    __loggers = {}

    def __init__(self):
        pass

    def add_logger(logger):
        if logger.name is None or logger.name == "":
            raise Exception("Logger has no Attribute called 'name'!")

        EventLogger.__loggers[logger.name] = logger

    def remove_logger(logger_name):
        if logger_name in EventLogger.__loggers:
            EventLogger.__loggers.pop(logger_name)
            return True

        return False

    # Does not really work as expected >_>
    # def get_logger(logger_name):
    #     if logger_name in EventLogger.__loggers:
    #         return EventLogger.__loggers.get(logger_name)
    #     return None

    def debug(msg, logger_name=None):
        level = logging.DEBUG
        EventLogger._send_message(level, msg, logger_name)

    def info(msg, logger_name=None):
        level = logging.INFO
        EventLogger._send_message(level, msg, logger_name)

    def warn(msg, logger_name=None):
        level = logging.WARN
        EventLogger._send_message(level, msg, logger_name)

    def warning(msg, logger_name=None):
        level = logging.WARNING
        EventLogger._send_message(level, msg, logger_name)

    def error(msg, logger_name=None):
        level = logging.ERROR
        EventLogger._send_message(level, msg, logger_name)

    def critical(msg, logger_name=None):
        level = logging.CRITICAL
        EventLogger._send_message(level, msg, logger_name)

    def log(level, msg, logger_name=None):
        EventLogger._send_message(level, msg, logger_name)

    def _send_message(level, msg, logger_name):
        if logger_name is not None:
            if logger_name in EventLogger.__loggers:
                EventLogger.__loggers[logger_name].log(level, msg)
        else:
            for logger in EventLogger.__loggers.values():
                logger.log(level, msg)


    # static methods
    add_logger = staticmethod(add_logger)
    remove_logger = staticmethod(remove_logger)
    # get_logger = staticmethod(get_logger)
    debug = staticmethod(debug)
    info = staticmethod(info)
    warn = staticmethod(warn)
    warning = staticmethod(warning)
    error = staticmethod(error)
    critical = staticmethod(critical)
    log = staticmethod(log)
    _send_message = staticmethod(_send_message)


class ConsoleLogger(logging.Logger):
    """
    This class outputs the logged events to the console
    """

    def __init__(self, name, log_level):
        logging.Logger.__init__(self, name, log_level)

        # create console handler and set level
        ch = logging.StreamHandler()

        ch.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter(EventLogger.format)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.addHandler(ch)


class FileLogger(logging.Logger):
    """
    This class writes the logged events to an LOG file (EventLogger.EVENT_FILE_LOGGING_PATH)
    """

    def __init__(self, name, log_level, filename):
        logging.Logger.__init__(self, name, log_level)

        ch = logging.FileHandler(filename, mode="a")

        ch.setLevel(log_level)

        # create formatter
        formatter = logging.Formatter(EventLogger.format)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.addHandler(ch)

        self.info("###### NEW LOGGING SESSION STARTED ######")


class GUILogger(logging.Logger, QtCore.QObject):
    """
    This class outputs the logged data to the brickv gui
    """

    # for level as string
    _convert_level = {}
    _convert_level[logging.DEBUG] = logging._levelNames.get(logging.DEBUG)  # "DEBUG"
    _convert_level[logging.INFO] = logging._levelNames.get(logging.INFO)  # "INFO"
    _convert_level[logging.WARN] = logging._levelNames.get(logging.WARN)  # "WARNING"
    _convert_level[logging.WARNING] = logging._levelNames.get(logging.WARNING)  # "WARNING"
    _convert_level[logging.CRITICAL] = logging._levelNames.get(logging.CRITICAL)  # "CRITICAL"
    _convert_level[logging.ERROR] = logging._levelNames.get(logging.ERROR)  # "ERROR"

    _output_format = "{asctime} - <b>{levelname:8}</b> - {message}"
    _output_format_warning = "<font color=\"orange\">{asctime} - <b>{levelname:8}</b> - {message}</font>"
    _output_format_critical = "<font color=\"red\">{asctime} - <b>{levelname:8}</b> - {message}</font>"

    SIGNAL_NEW_MESSAGE = "newEventMessage"
    SIGNAL_NEW_MESSAGE_TAB_HIGHLIGHT = "newEventTabHighlight"

    def __init__(self, name, log_level):
        logging.Logger.__init__(self, name, log_level)
        QtCore.QObject.__init__(self)

    def debug(self, msg):
        self.log(logging.DEBUG, msg)

    def info(self, msg):
        self.log(logging.INFO, msg)

    def warn(self, msg):
        self.log(logging.WARN, msg)

    def warning(self, msg):
        self.log(logging.WARNING, msg)

    def critical(self, msg):
        self.log(logging.CRITICAL, msg)

    def error(self, msg):
        self.log(logging.ERROR, msg)

    def log(self, level, msg):

        if level >= self.level:
            asctime = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            levelname = GUILogger._convert_level[level]

            if level == logging.WARN or level == logging.WARNING:
                self.emit(SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE),
                          GUILogger._output_format_warning.format(asctime=asctime, levelname=levelname, message=msg))
                self.emit(SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE_TAB_HIGHLIGHT))
            elif level == logging.CRITICAL or level == logging.ERROR:
                self.emit(SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE),
                          GUILogger._output_format_critical.format(asctime=asctime, levelname=levelname, message=msg))
                self.emit(SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE_TAB_HIGHLIGHT))
            else:
                self.emit(SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE),
                          GUILogger._output_format.format(asctime=asctime, levelname=levelname, message=msg))
