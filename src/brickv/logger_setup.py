# -*- coding: utf-8 -*-

import codecs
import collections
import json
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox

from brickv import config
from brickv.data_logger.event_logger import EventLogger, GUILogger
from brickv.data_logger.gui_config_handler import GuiConfigHandler
from brickv.data_logger.job import GuiDataJob
from brickv.data_logger.loggable_devices import Identifier
from brickv.data_logger.utils import Utilities
from brickv.device_dialog import LoggerDeviceDialog
from brickv.ui_logger_setup import Ui_Logger


class LoggerWindow(QDialog, Ui_Logger):
    """
        Function and Event handling class for the Ui_Logger.
    """
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self._gui_logger = GUILogger("GUILogger", EventLogger.EVENT_LOG_LEVEL)
        self._gui_job = None
        EventLogger.add_logger(self._gui_logger)
        
        self.interval_string = "_interval"
        self.interval_show = "interval"
        self.exceptional_interval_string = "special_values"
        self.data_logger_thread = None
        self.tab_console_warning = False
        
        self.logger_device_dialog = None

        #if self._table_widget is not None:#FIXME rework this like the console_tab
        #    self.jobs.append()

        self.setupUi(self)
        self.widget_initialization()
        
    def widget_initialization(self):
        '''
            Sets default values for some widgets
        '''
        # Login data
        self.host_info_initialization()
        self.combo_log_level_init(self.combo_console_level)
        self.combo_console_level.setCurrentIndex(1) #INFO LEVEL
        
        self.signal_initialization()
           
    def signal_initialization(self):
        """
            Init of all important Signals and connections.
        """
        # Buttons
        self.btn_start_logging.clicked.connect(self.btn_start_logging_clicked)
        self.btn_save_config.clicked.connect(self.btn_save_config_clicked)
        self.btn_load_config.clicked.connect(self.btn_load_config_clicked)
        self.btn_set_logfile.clicked.connect(self.btn_set_logfile_clicked)
        self.btn_console_clear.clicked.connect(self.btn_console_clear_clicked)
        self.combo_console_level.currentIndexChanged.connect(self.combo_console_level_changed)
        self.btn_add_device.clicked.connect(self.btn_add_device_clicked)
        self.btn_remove_device.clicked.connect(self.btn_remove_device_clicked)
        
        self.tab_widget.currentChanged.connect(self.tab_reset_warning)
        self.btn_clear_tabel.clicked.connect(self.btn_clear_table_clicked)


        self.connect(self._gui_logger, QtCore.SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE), self.txt_console_output)
        self.connect(self._gui_logger, QtCore.SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE_TAB_HIGHLIGHT), self.txt_console_highlight_tab)
        
        # login information
        self.combo_host.currentIndexChanged.connect(self._host_index_changed)
        self.spinbox_port.valueChanged.connect(self._port_changed)
        
        self.checkbox_xively.stateChanged.connect(self.cb_xively_changed)
        
        self.tree_devices.itemDoubleClicked.connect(self.tree_on_double_click)
        self.tree_devices.itemChanged.connect(self.tree_on_change)

    def combo_log_level_init(self, combo_widget):
        combo_widget.clear()
        od = collections.OrderedDict(sorted(self._gui_logger._convert_level.items()))
        for k in od.keys():
            combo_widget.addItem(od[k])

    def host_info_initialization(self):
        '''
            initialize host by getting information out of brickv.config
        '''
        self.host_infos = config.get_host_infos(config.HOST_INFO_COUNT)
        self.host_index_changing = True

        for host_info in self.host_infos:
            self.combo_host.addItem(host_info.host)

        self.last_host = None
        self.combo_host.setCurrentIndex(0)
        self.spinbox_port.setValue(self.host_infos[0].port)
        self.host_index_changing = False
        
    def btn_start_logging_clicked(self):
        '''
            Start/Stop of the logging process
        '''
        if (self.data_logger_thread is not None) and (not self.data_logger_thread.stopped):
            self.btn_start_logging.clicked.disconnect()
            
            self.data_logger_thread.stop()
            self._reset_stop()

        elif self.data_logger_thread is None:
            from data_logger import main
            arguments_map = {}
            arguments_map[main.GUI_CONFIG] = GuiConfigHandler.create_config_file(self)
            from brickv.data_logger.job import GuiDataJob
            self._gui_job = GuiDataJob(name="GuiData-Writer")
            self.connect(self._gui_job, QtCore.SIGNAL(GuiDataJob.SIGNAL_NEW_DATA), self.table_add_row)
            arguments_map[main.GUI_ELEMENT] = self._gui_job

            self.data_logger_thread = main.main(arguments_map)


            if self.data_logger_thread is not None:
                self.btn_start_logging.setText("Stop Logging")
                self.tab_devices.setEnabled(False)
                self.tab_setup.setEnabled(False)
                # self.tab_xively.setEnabled(False)#nyi
                self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.tab_console))
                self.tab_reset_warning()
            
    def _reset_stop(self):
        self.tab_devices.setEnabled(True)
        self.tab_setup.setEnabled(True)
        # self.tab_xively.setEnabled(True)#nyi
        self.btn_start_logging.setText("Start Logging")

        self.disconnect(self._gui_job, QtCore.SIGNAL(GuiDataJob.SIGNAL_NEW_DATA), self.table_add_row)
        self.data_logger_thread = None
        self._gui_job = None
        
        self.btn_start_logging.clicked.connect(self.btn_start_logging_clicked)

    def btn_save_config_clicked(self):
        """
            Opens a FileSelectionDialog and saves the current config.
        """
        conf = GuiConfigHandler.create_config_file(self)
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Save  Config-File', os.getcwd(), filter='*.json')
        
        if fn == "":
            # cancel
            EventLogger.debug("Cancelled load Config.")
            return
        
        try:
            with open(fn, 'w') as outfile:
                json.dump(conf, outfile, sort_keys=True, indent=2)
        except Exception as e1:
            EventLogger.warning("Load Config - Exception: " + str(e1))
            QMessageBox.warning(self, 'Error', 'Could not save the Config-File! Look at the Log-File for further information.', QMessageBox.Ok)
            return
        
        QMessageBox.information(self, 'Success', 'Config-File saved!', QMessageBox.Ok)
        EventLogger.info("Config-File saved to: " + str(fn))

    def btn_load_config_clicked(self):
        """
            Opens a FileSelectionDialog and loads the selected config.
        """
        fn = QtGui.QFileDialog.getOpenFileName(self, "Open Config-File...", os.getcwd(), "JSON-Files (*.json)")
        
        if fn == "":
            # cancel
            EventLogger.debug("Cancelled save Config.")
            return
        
        config_json = None
        try:
            with codecs.open(fn, 'r', 'UTF-8') as content_file:
                try:
                    config_json = json.load(content_file)
                    
                except ValueError as e:
                    EventLogger.warning("Load Config - Cant parse the configuration file: " + str(e))
        except Exception as e1:
            EventLogger.warning("Load Config - Exception: " + str(e1))
            return
         
        EventLogger.info("Loaded Config-File from: " + str(fn))
         
        # devices
        config_blueprint = GuiConfigHandler.load_devices(config_json)
        if config_blueprint is None:
            return
        
        self.create_tree_items(config_blueprint, False)
        # general_section
        from brickv.data_logger.configuration_validator import ConfigurationReader
        self.update_setup_tab(config_json[ConfigurationReader.GENERAL_SECTION])
        
        # TODO add other informations
        # xively

    def btn_set_logfile_clicked(self):
        """
            Opens a FileSelectionDialog and sets the selected path for the data output file.
        """
        fn = QtGui.QFileDialog.getSaveFileName(self, 'Choose Config Destination', os.getcwd(), "CSV-Files (*.csv);;Text-Files (*.txt)")
        
        if fn == "":
            # cancel
            EventLogger.debug("Cancelled select Config-File-Path.")
            return
        
        self.line_path_to_file.setText(fn)
    
    def btn_add_device_clicked(self):
        """
            Opens the DeviceDialog in Add-Mode.
        """
        if self.logger_device_dialog is None:
            self.logger_device_dialog = LoggerDeviceDialog(self)
            
        blueprint = json.loads(GuiConfigHandler.all_devices_blueprint)
        self.logger_device_dialog.init_dialog(blueprint, True)
        self.logger_device_dialog.show()
    
    def btn_remove_device_clicked(self):
        """
            Opens the DeviceDialog in Remove-Mode.
        """
        if self.logger_device_dialog is None:
            self.logger_device_dialog = LoggerDeviceDialog(self)
        
        self.logger_device_dialog.init_dialog(GuiConfigHandler.get_simple_blueprint(self), False)
        self.logger_device_dialog.show()

    def btn_clear_table_clicked(self):
        """
            Clears the Data table.
        """
        self.table_widget.setRow(0)

    def tab_reset_warning(self):
        """
            Resets the Warning @ the console tab.
        """
        if not self.tab_console_warning or self.tab_widget.currentWidget().objectName() != self.tab_console.objectName():
            return

        self.tab_console_warning = False
        from PyQt4.QtGui import QColor
        self.tab_set(self.tab_widget.indexOf(self.tab_console), QColor(0, 0, 0), None)

    def combo_console_level_changed(self):
        """
            Changes the log level dynamically.
        """
        import logging
        ll = self.combo_console_level.currentText()

        od = collections.OrderedDict(sorted(self._gui_logger._convert_level.items()))
        for k in od.keys():
            if ll == od[k]:
                self._gui_logger.level = k
                break;

    def tab_set(self, tab_index, color, icon=None):
        """
            Sets the font Color and an icon, if given, at a specific tab.
        """
        from PyQt4.QtGui import QIcon
        
        self.tab_widget.tabBar().setTabTextColor(tab_index, color)
        if icon is not None:
            self.tab_widget.setTabIcon(tab_index, QIcon(icon))
        else:
            self.tab_widget.setTabIcon(tab_index, QIcon())
    
    def btn_console_clear_clicked(self):
        """
            Clears the gui console tab.
        """
        self.txt_console.clear()
    
    def _host_index_changed(self, i):
        '''
            Persists host information changes like in brickv.mainwindow
            Changes port if the host was changed
        '''
        if i < 0:
            return

        self.host_index_changing = True
        self.spinbox_port.setValue(self.host_infos[i].port)
        self.host_index_changing = False

    def _port_changed(self, value):
        '''
            Persists host information changes like in brickv.mainwindow
        '''
        if self.host_index_changing:
            return

        i = self.combo_host.currentIndex()
        if i < 0:
            return

        self.host_infos[i].port = self.spinbox_port.value()
            
    def cb_xively_changed(self):
        '''
            Enables/Disables widgets for xively configuration
        '''
        if self.checkbox_xively.isChecked():
            self.groupBox_xively.setEnabled(True)
        else:
            self.groupBox_xively.setEnabled(False)
    
    def update_setup_tab(self, general_section):
        """
            Update the information of the setup tab with the given general_section.
        """
        from brickv.data_logger.configuration_validator import ConfigurationReader
        
        try:
            # host            combo_host              setEditText(String)
            self.combo_host.setEditText(general_section[ConfigurationReader.GENERAL_HOST])
            # port            spinbox_port            setValue(int)
            self.spinbox_port.setValue(general_section[ConfigurationReader.GENERAL_PORT])
            # file_count      spin_file_count         setValue(int)
            self.spin_file_count.setValue(general_section[ConfigurationReader.GENERAL_LOG_COUNT])
            # file_size       spin_file_size          setValue(int/1024/1024)  (Byte -> MB)
            self.spin_file_size.setValue((general_section[ConfigurationReader.GENERAL_LOG_FILE_SIZE] / 1024.0 / 1024.0))
            # path_to_file    line_path_to_file       setText(string)
            self.line_path_to_file.setText(general_section[ConfigurationReader.GENERAL_PATH_TO_FILE])
            
        except Exception as e:
            EventLogger.critical("Could not read the General Section of the Config-File! -> " + str(e))
            return
        
    def create_tree_items(self, blueprint, view_all=False):
        """
            Create the device tree with the given blueprint.
            Shows all possible devices, if the view_all Flag is True.
        """
        self.tree_devices.clear()
        self.tree_devices.setSortingEnabled(False)
        
        try:
            if view_all:
                try:
                    try:
                        blueprint = json.loads(GuiConfigHandler.all_devices_blueprint)
                             
                    except ValueError as e:
                        EventLogger.warning("DeviceTree - Cant parse the Blueprint: " + str(e))
                except Exception as e1:
                    EventLogger.warning("DeviceTree - Exception: " + str(e1))
           
            # counts topLevelItems
            tree_counter = 0
            
            for i in range(0, len(blueprint)):
                device_items = blueprint[i]
            
                for dev_item in device_items:
                    # counts variables
                    variable_counter = 0
                    
                    # new entry in tree
                    item_0 = QtGui.QTreeWidgetItem(self.tree_devices)
                    item_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tree_devices.topLevelItem(tree_counter).setText(0, str(dev_item))
                    # show uid, when view_all=False
                    # else show nothing
                    if view_all:
                        self.tree_devices.topLevelItem(tree_counter).setText(1, "Enter UID")
                    
                    for variable in device_items[dev_item]:
                        # counts each variable
                        var_n_counter = 0
                        
                        # check if var = uid
                        if variable == Identifier.DEVICE_UID:
                            self.tree_devices.topLevelItem(tree_counter).setText(1, str(device_items[dev_item][variable]))
                            continue
                        
                        # new child for the previeous item
                        item_1 = QtGui.QTreeWidgetItem(item_0)
                        self.tree_devices.topLevelItem(tree_counter).child(variable_counter).setText(0, str(variable))
                        
                        
                        for var_n in device_items[dev_item][variable]:
                            # new child of child
                            item_2 = QtGui.QTreeWidgetItem(item_1)
                            tmp_item = self.tree_devices.topLevelItem(tree_counter).child(variable_counter).child(var_n_counter)
                            
                            if str(var_n) == self.interval_string or str(self.tree_devices.topLevelItem(tree_counter).child(variable_counter).text(0)) == self.exceptional_interval_string:
                                item_2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                                if str(var_n) == self.interval_string:
                                    tmp_item.setText(0, self.interval_show)
                                else:
                                    tmp_item.setText(0, str(var_n))
                                tmp_item.setText(1, str(device_items[dev_item][variable][var_n]))
                                tmp_item.setToolTip(1,"Interval in milliseconds")
                            else:
                                item_2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                                tmp_item.setText(0, str(var_n))
                                if device_items[dev_item][variable][var_n]:
                                    tmp_item.setCheckState(1, QtCore.Qt.Checked)
                                else:
                                    tmp_item.setCheckState(1, QtCore.Qt.Unchecked)
                                tmp_item.setText(1, "")
                           
                            
                            var_n_counter += 1
                        variable_counter += 1
                    
                    if str(self.tree_devices.topLevelItem(tree_counter).text(1)) == "":
                        self.tree_devices.topLevelItem(tree_counter).setText(1, "Enter UID")
                                 
                    tree_counter += 1
            
            EventLogger.debug("Device Tree created.")
            
        except Exception as e:
            EventLogger.warning("DeviceTree - Exception while creating the Tree: " + str(e))
        
        self.tree_devices.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_devices.setSortingEnabled(True)
       
    def add_item_to_tree(self, item_blueprint,uid=""):
        """
            Adds an item to the device tree. Needs the correct blueprint.
        """
        self.tree_devices.setSortingEnabled(False)
        # add device into tree
        
        tree_counter = self.tree_devices.topLevelItemCount()
        
        for dev_item in item_blueprint:
            # counts variables
            variable_counter = 0
            
            # new entry in tree
            item_0 = QtGui.QTreeWidgetItem(self.tree_devices)
            item_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tree_devices.topLevelItem(tree_counter).setText(0, str(dev_item))

            self.tree_devices.topLevelItem(tree_counter).setText(1, uid)
            
        
            for variable in item_blueprint[dev_item]:
                # counts each variable
                var_n_counter = 0
                
                # check if var = uid
                if variable == Identifier.DEVICE_UID:
                    self.tree_devices.topLevelItem(tree_counter).setText(1, str(item_blueprint[dev_item][variable]))
                    continue
                
                # new child for the previeous item
                item_1 = QtGui.QTreeWidgetItem(item_0)
                self.tree_devices.topLevelItem(tree_counter).child(variable_counter).setText(0, str(variable))
                
                
                for var_n in item_blueprint[dev_item][variable]:
                    # new child of child
                    item_2 = QtGui.QTreeWidgetItem(item_1)
                    tmp_item = self.tree_devices.topLevelItem(tree_counter).child(variable_counter).child(var_n_counter)
                    
                    if str(var_n) == self.interval_string or str(self.tree_devices.topLevelItem(tree_counter).child(variable_counter).text(0)) == self.exceptional_interval_string:
                        item_2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                        if str(var_n) == self.interval_string:
                            tmp_item.setText(0, self.interval_show)
                            tmp_item.setToolTip(1,"Interval in milliseconds")
                        else:
                            tmp_item.setText(0, str(var_n))
                        tmp_item.setText(1, str(item_blueprint[dev_item][variable][var_n]))
                    else:
                        item_2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                        tmp_item.setText(0, str(var_n))
                        if item_blueprint[dev_item][variable][var_n]:
                            tmp_item.setCheckState(1, QtCore.Qt.Checked)
                        else:
                            tmp_item.setCheckState(1, QtCore.Qt.Unchecked)
                        tmp_item.setText(1, "")
                    
                    var_n_counter += 1
                variable_counter += 1
        
        self.tree_devices.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_devices.setSortingEnabled(True)
    
    def remove_item_from_tree(self, item_name, item_uid):
        """
            Removes an item from the device tree. The first match is removed!
        """
        # remove first found match!
        removed_item = False
        t0_max = self.tree_devices.topLevelItemCount()
        
        for t0 in range(0, t0_max):
            
            dev_name = self.tree_devices.topLevelItem(t0).text(0)
            dev_uid = self.tree_devices.topLevelItem(t0).text(1)
            
            if dev_name == item_name and dev_uid == item_uid:
                removed_item = True
                self.tree_devices.takeTopLevelItem(t0)
                break
          
        if not removed_item:
            QMessageBox.information(self, 'No Device found?', 'No Device was not found and could not be deleted!', QMessageBox.Ok)
        
    def tree_on_change(self, item, column):
        """
            Tries to parse the input of a tree cell into an
            integer. if its not possible, or below a certain
            treshhold, it will be set to 0. Only checks cells
            where the first collumn is interval!
        """
        # check for wrong input number in interval
        if column == 1:
            if str(item.text(0)).lower() == self.interval_show:
                # check for string and value lower 0
                item.setText(1, str(Utilities.parse_to_int(str(item.text(1)))))
  
    def tree_on_double_click(self, item, column):
        """
            Is called, when a cell in the tree was doubleclicked.
            Is used to allow the changeing of the interval
            numbers and UID's but not empty cells.
        """
        edit_flag = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        non_edit_flag = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        
        if column == 0:
            item.setFlags(non_edit_flag)
            
        elif item.text(column) != "" or item.text(column) is None:
            item.setFlags(edit_flag)

    def txt_console_output(self, msg):
        """
            SIGNAL function:
            Function to write text on the gui console tab.
        """
        self.txt_console.append(str(msg))
        if self.checkbox_console_auto_scroll.isChecked():
            self.txt_console.moveCursor(QtGui.QTextCursor.End)


    def txt_console_highlight_tab(self):
        """
            SIGNAL function:
            Highlight the console/message tab when an error occurs.
        """
        if not self.tab_console_warning and self.tab_widget.currentWidget().objectName() != self.tab_console.objectName():
            self.tab_console_warning = True
            from brickv.utils import get_resources_path
            from PyQt4.QtGui import QColor
            self.tab_set(self.tab_widget.indexOf(self.tab_console), QColor(255, 0, 0), os.path.join(get_resources_path(), "dialog-warning.png"))

    def table_add_row(self, csv_data):
        """
            SIGNAL function:
            Adds new CSV Data into the Table.
        """
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, QtGui.QTableWidgetItem(str(csv_data.uid)))
        self.table_widget.setItem(row, 1, QtGui.QTableWidgetItem(str(csv_data.name)))
        self.table_widget.setItem(row, 2, QtGui.QTableWidgetItem(str(csv_data.var_name)))
        self.table_widget.setItem(row, 3, QtGui.QTableWidgetItem(str(csv_data.raw_data)))
        self.table_widget.setItem(row, 4, QtGui.QTableWidgetItem(str(csv_data.timestamp)))

        if self.checkbox_data_auto_scroll.isChecked():
            self.table_widget.scrollToBottom()
