# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from brickv.ui_device_dialog import Ui_DeviceDialog
from PyQt4 import QtGui, QtCore

class LoggerDeviceDialog(QDialog,Ui_DeviceDialog):
    def __init__(self, parent, blueprint, add_data = True, ):
        QDialog.__init__(self, parent)
        
        self._add_data = add_data
        self._blueprint = blueprint
        self._logger_window = parent
        
        self.setupUi(self)
        self.signal_initialization()
        
        self._create_tree()
        
        
        print "LoggerDEviceDialog ADD-> " + str(self._add_data)
        
    def signal_initialization(self):
        self.btn_action_device.clicked.connect(self._btn_action_device_clicked)
    
    def _btn_action_device_clicked(self):
        pass
    
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
        print ("close")
        self._logger_window.destroy_device_dialog()
        #QDialog.destroy(self)
        #return QDialog.closeEvent(self, event)
