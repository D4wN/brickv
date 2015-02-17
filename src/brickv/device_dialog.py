# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from brickv.ui_device_dialog import Ui_DeviceDialog

class LoggerDeviceDialogw(QDialog,Ui_DeviceDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.signal_initialization()
        
    def signal_initialization(self):
        # TODO: All singnal inits goes here
        pass