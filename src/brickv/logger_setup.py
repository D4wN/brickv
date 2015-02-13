# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logger.ui'
#
# Created: Tue Feb 10 14:45:20 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from brickv.ui_logger_setup import Ui_Logger
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from brickv.data_logger.utils import Utilities
from brickv.data_logger.loggable_devices import Identifier
from brickv.data_logger.event_logger import EventLogger
import codecs
import json
import collections
from brickv.data_logger.gui_config_handler import GuiConfigHandler
import os

class LoggerWindow(QDialog,Ui_Logger):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
                
        self.interval_string = "_interval"
        self.interval_show = "interval"
        self.exceptional_interval_string = "special_values"        
        
        self.setupUi(self)
        self.signal_initialization()
        
    def signal_initialization(self):
        # Buttons 
        self.btn_start_logging.clicked.connect(self.btn_start_logging_clicked)
        self.btn_save_config.clicked.connect(self.btn_save_config_clicked)
        self.btn_set_logfile.clicked.connect(self.btn_set_logfile_clicked)
        
        self.checkbox_xively.stateChanged.connect(self.cb_xively_changed)
        
        self.tree_devices.itemDoubleClicked.connect(self.tree_on_double_click)
        self.tree_devices.itemChanged.connect(self.tree_on_change)
        
        #FIXME - find better init position
        self.createTreeItems(None, True)

    def btn_start_logging_clicked(self):
        # TODO: Start data logger here
        from data_logger import main
        
        arguments_map = {}
        arguments_map[main.CONSOLE_CONFIG_FILE] = self.path_to_config
        arguments_map[main.CONSOLE_VALIDATE_ONLY] = False
        main.main(arguments_map)
        
    def btn_save_config_clicked(self):
        # TODO: Call Marvs save_config function
        QMessageBox.information(self, 'Info', 'btn_save_config_clicked was clicked - name dialog?', QMessageBox.Ok)
        
        conf = GuiConfigHandler.create_config_file(self.tree_devices)    
        try: 
            with open(os.getcwd()+"\\src\\brickv\\data_logger\\created_config.json", "w") as outfile:
                json.dump(conf, outfile, sort_keys=True, indent=2)
        except Exception as e:    
            print("Save config to File: " + str(e) )    

    def btn_set_logfile_clicked(self):
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
    
    def createTreeItems(self, device_items, view_all=True):
        self.tree_devices.clear()
        self.tree_devices.setSortingEnabled(False)
        
        try:
            if view_all:
                try:
                    with codecs.open(os.getcwd()+"\\src\\brickv\\data_logger\\gui_config.json", 'r', 'UTF-8') as content_file:
                        try:       
                            device_items = json.load(content_file, object_pairs_hook=collections.OrderedDict)
                            
                        except ValueError as e:    
                            print("DeviceTree - Cant parse the configuration file: " + str(e) )
                except Exception as e1:
                    print("DeviceTree - Exception: " + str(e1) )
            
            if device_items == None:
                print("DeviceTree - No Devices found? Check your "+os.getcwd()+"\\src\\brickv\\data_logger\\gui_config.json File. ")
                return
               
            #counts topLevelItems
            tree_counter = 0;
            
            for dev_item in device_items:
                #print str(dev_item) + "@" + str(tree_counter)
                #counts variables
                variable_counter = 0
                
                #new entry in tree 
                item_0 = QtGui.QTreeWidgetItem(self.tree_devices) 
                item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
                self.tree_devices.topLevelItem(tree_counter).setText(0, str(dev_item))
                #show uid, when view_all=False
                #else show nothing
                if view_all:
                    self.tree_devices.topLevelItem(tree_counter).setText(1,"Enter UID")
                
                for variable in device_items[dev_item]:
                    #print "  "+str(variable) + "@" + str(variable_counter)
                    #counts each variable
                    var_n_counter = 0
                    
                    #check if var = uid
                    if variable == Identifier.DEVICE_UID:
                        self.tree_devices.topLevelItem(tree_counter).setText(1,str(device_items[dev_item][variable]))
                        continue
                    
                    #new child for the previeous item
                    item_1 = QtGui.QTreeWidgetItem(item_0)
                    self.tree_devices.topLevelItem(tree_counter).child(variable_counter).setText(0, str(variable))
                    
                    
                    for var_n in device_items[dev_item][variable]:
                        #print "  "+str(var_n) + "@" + str(var_n_counter)
                        #new child of child
                        item_2 = QtGui.QTreeWidgetItem(item_1)                    
                        tmp_item = self.tree_devices.topLevelItem(tree_counter).child(variable_counter).child(var_n_counter);
                        
                        if str(var_n) == self.interval_string or str(self.tree_devices.topLevelItem(tree_counter).child(variable_counter).text(0)) == self.exceptional_interval_string:
                            item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled)
                            if str(var_n) == self.interval_string:
                                tmp_item.setText(0, self.interval_show)
                            else:
                                tmp_item.setText(0, str(var_n))
                            tmp_item.setText(1, str(device_items[dev_item][variable][var_n])) 
                        else:
                            item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                            tmp_item.setText(0, str(var_n)) 
                            tmp_item.setCheckState (1, QtCore.Qt.Checked)
                            tmp_item.setText(1, "") 
                       
                        
                        var_n_counter+=1
                    variable_counter+=1   
                
                if str(self.tree_devices.topLevelItem(tree_counter).text(1)) == "":
                    self.tree_devices.topLevelItem(tree_counter).setText(1,"Enter UID")
                             
                tree_counter+=1
            EventLogger.debug("Divece Tree created.")
            
        except Exception as e:
            print "DeviceTree - Exception while creating the Tree: " +str(e)
        
        self.tree_devices.sortItems ( 0, QtCore.Qt.AscendingOrder)
        self.tree_devices.setSortingEnabled(True)
        
    
    def tree_on_change(self, item, column): 
        #check for wrong input number in interval
        if column == 1:
            if str(item.text(0)).lower() == self.interval_show:
                #check for string and value lower 0
                #Utilities.parse_to_int(string) FIXME
                item.setText(1,str(Utilities.parse_to_int(str(item.text(1)))))
                
        #checkState 0 = False; 1 = PartialSelected; 2 = True
  
    def tree_on_double_click(self, item, column):
        edit_flag = (QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        non_edit_flag = (QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        
        if column == 0:            
            item.setFlags(non_edit_flag)
            
        elif item.text(column) != "" or item.text(column) == None:
            item.setFlags(edit_flag)
