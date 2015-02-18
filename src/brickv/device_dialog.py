# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog, QMessageBox
from brickv.ui_device_dialog import Ui_DeviceDialog
from PyQt4 import QtGui, QtCore
from brickv.data_logger.gui_config_handler import GuiConfigHandler

class LoggerDeviceDialog(QDialog,Ui_DeviceDialog):
    def __init__(self, parent, blueprint, add_data = True, ):
        QDialog.__init__(self, parent)
        
        self._add_data = add_data
        self._blueprint = blueprint
        self._logger_window = parent
        
        self.setupUi(self)
        self.signal_initialization()
        
        self._create_tree()
        
    def signal_initialization(self):
        self.tree_device_list.itemDoubleClicked.connect(self._tree_on_double_click)
        self.btn_action_device.clicked.connect(self._btn_action_device_clicked)
        self.checkbox_fast_mode.stateChanged.connect(self._checkbox_fast_mode_checked)
        
        if self._add_data:
            self.btn_action_device.setText("Add")
            self._check_mode = "add"
        else:
            self.btn_action_device.setText("Remove")
            self._check_mode = "remove"
    
    def _checkbox_fast_mode_checked(self):
        if self.checkbox_fast_mode.isChecked():
            QMessageBox.information(self, 'Fast Mode Enabled', 'Fast Mode is now Enabled! You can now '+self._check_mode+' Devices with a DoubleClick.', QMessageBox.Ok)
    
    def _tree_on_double_click(self): #, item, column
        if not self.checkbox_fast_mode.isChecked():
            return
        
        self._btn_action_device_clicked()
    
    def _btn_action_device_clicked(self):
        focused_item = self.tree_device_list.currentItem()
        if focused_item is None:
            QMessageBox.information(self, 'No Device', 'No Device selected! Please select a Device first.', QMessageBox.Ok)          
            return
        
        if self._add_data:
            #add device
            dev = GuiConfigHandler.get_single_device_bluprint(focused_item.text(0))
            
            if dev is None:
                return
            
            self._logger_window.add_item_to_tree(dev)
            
        else:
            #remove device
            dev = focused_item.text(0)
            dev_uid = focused_item.text(1)
            
            self.tree_device_list.takeTopLevelItem(self.tree_device_list.indexOfTopLevelItem(focused_item))
            self._logger_window.remove_item_from_tree(dev, dev_uid)
    
    def _create_tree(self):
        self.tree_device_list.clear()
        self.tree_device_list.setSortingEnabled(False)
        
        if not self._add_data:
            #add second collumn
            self.tree_device_list.headerItem().setText(1, "UID")
        
        tree_counter = 0;
        for dev_item in self._blueprint:
            for i in dev_item:
                                
                #new entry in tree 
                item_0 = QtGui.QTreeWidgetItem(self.tree_device_list) 
                item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                self.tree_device_list.topLevelItem(tree_counter).setText(0, str(i))
                if not self._add_data:
                    self.tree_device_list.topLevelItem(tree_counter).setText(1, str(dev_item[i]))
                
                tree_counter+=1
        
        self.tree_device_list.sortItems ( 0, QtCore.Qt.AscendingOrder)
        self.tree_device_list.setSortingEnabled(True)
    
    def closeEvent(self, event):
        self._logger_window.destroy_device_dialog()
        #QDialog.destroy(self)
        #return QDialog.closeEvent(self, event)
