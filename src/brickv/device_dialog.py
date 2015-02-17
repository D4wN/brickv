# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from brickv.ui_device_dialog import Ui_DeviceDialog

class LoggerDeviceDialog(QDialog,Ui_DeviceDialog):
    def __init__(self, parent, blueprint, add_data = True, ):
        QDialog.__init__(self, parent)
        
        self._add_data = add_data
        self._blueprint = blueprint
        self._logger_window = parent
        
        self.setupUi(self)
        self.signal_initialization()
        
        print "LoggerDEviceDialog ADD-> " + str(self._add_data)
        
    def signal_initialization(self):
        # TODO: All singnal inits goes here
        pass