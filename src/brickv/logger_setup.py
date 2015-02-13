# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logger.ui'
#
# Created: Tue Feb 10 14:45:20 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from brickv.ui_logger_setup import Ui_Logger
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox

class LoggerWindow(QDialog,Ui_Logger):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.signal_initialization()
        
    def signal_initialization(self):
        # Buttons 
        self.btn_start_logging.clicked.connect(self.btn_start_logging_clicked)
        self.btn_save_config.clicked.connect(self.btn_save_config_clicked)
        self.btn_set_logfile.clicked.connect(self.btn_set_logfile_clicked)
        
        self.checkbox_xively.stateChanged.connect(self.cb_xively_changed)

    def btn_start_logging_clicked(self):
        # TODO: Start data logger here
        from data_logger import main
        
        arguments_map = {}
        arguments_map[main.CONSOLE_CONFIG_FILE] = self.path_to_config
        arguments_map[main.CONSOLE_VALIDATE_ONLY] = False
        main.main(arguments_map)
        
    def btn_save_config_clicked(self):
        # TODO: Call Marvs save_config function
        QMessageBox.information(self, 'Info', 'btn_save_config_clicked was clicked', QMessageBox.Ok)

    def btn_set_logfile_clicked(self):
        import os
        fn = QtGui.QFileDialog.getOpenFileName(self, "Open File...", os.getcwd(),
                "CSV-Files (*.csv);;Text-Files (*.txt);;JSON-Files (*.json)")
        if fn:
            self.lineEdit.setText(fn)
            self.path_to_config = fn
    
    def cb_xively_changed(self):
        if self.checkbox_xively.isChecked():
            self.groupBox_xively.setEnabled(True)
        else:
            self.groupBox_xively.setEnabled(False)
