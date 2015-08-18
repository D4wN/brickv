# -*- coding: utf-8 -*-

import codecs
import collections
import json
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt  # , SIGNAL
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


# noinspection PyProtectedMember,PyCallByClass
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

        # FIXME better way to find interval and uids in tree_widget?!
        self.__tree_interval_tooltip = "Interval in milliseconds"
        self.__tree_uid_tooltip = "UID must be at least 3 Character long"
        self.data_logger_thread = None
        self.tab_console_warning = False

        self.logger_device_dialog = None

        # Code Inspector
        self.host_infos = None
        self.last_host = None
        self.host_index_changing = None

        # if self._table_widget is not None:#FIXME rework this like the console_tab <-- what does that mean?!
        # self.jobs.append()

        self.setupUi(self)
        self.widget_initialization()

    def widget_initialization(self):
        """
            Sets default values for some widgets
        """
        # Login data
        self.host_info_initialization()
        # GUI LOG LEVEL
        self.combo_log_level_init(self.combo_console_level)
        self.combo_console_level.setCurrentIndex(1)  # INFO LEVEL
        # set loglevel
        self.combo_console_level_changed()

        # LOGLEVEL FROM CONFIG
        self.combo_log_level_init(self.combo_loglevel)
        self.combo_loglevel.setCurrentIndex(0)  # DEBUG LEVEL

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
        self.btn_set_eventfile.clicked.connect(self.btn_set_eventfile_clicked)
        self.btn_console_clear.clicked.connect(self.btn_console_clear_clicked)
        self.combo_console_level.currentIndexChanged.connect(self.combo_console_level_changed)
        self.btn_add_device.clicked.connect(self.btn_add_device_clicked)
        self.btn_remove_device.clicked.connect(self.btn_remove_device_clicked)
        self.btn_remove_all_devices.clicked.connect(self.btn_remove_all_devices_clicked)

        self.tab_widget.currentChanged.connect(self.tab_reset_warning)
        self.btn_clear_tabel.clicked.connect(self.btn_clear_table_clicked)

        self.connect(self._gui_logger, QtCore.SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE), self.txt_console_output)
        self.connect(self._gui_logger, QtCore.SIGNAL(GUILogger.SIGNAL_NEW_MESSAGE_TAB_HIGHLIGHT),
                     self.txt_console_highlight_tab)

        # login information
        self.combo_host.currentIndexChanged.connect(self._host_index_changed)
        self.spinbox_port.valueChanged.connect(self._port_changed)

        self.checkbox_xively.stateChanged.connect(self.cb_xively_changed)

        self.tree_devices.itemDoubleClicked.connect(self.tree_on_double_click)
        self.tree_devices.itemChanged.connect(self.tree_on_change)

    def combo_log_level_init(self, combo_widget):
        combo_widget.clear()
        od = collections.OrderedDict(sorted(GUILogger._convert_level.items()))
        for k in od.keys():
            combo_widget.addItem(od[k])

            # TODO dynamic way to set GUI LogLevel - not used at the moment!
            # set index
            # ll = GUILogger._convert_level[EventLogger.EVENT_LOG_LEVEL]
            # combo_widget_count = combo_widget.count()
            # for i in range(0, combo_widget_count):
            # if ll == combo_widget.itemText(i):
            # combo_widget.setCurrentIndex(i)
            # break

    def host_info_initialization(self):
        """
            initialize host by getting information out of brickv.config
        """
        self.host_infos = config.get_host_infos(config.HOST_INFO_COUNT)
        self.host_index_changing = True

        for host_info in self.host_infos:
            self.combo_host.addItem(host_info.host)

        self.last_host = None
        self.combo_host.setCurrentIndex(0)
        self.spinbox_port.setValue(self.host_infos[0].port)
        self.host_index_changing = False

    def btn_start_logging_clicked(self):
        """
            Start/Stop of the logging process
        """
        if (self.data_logger_thread is not None) and (not self.data_logger_thread.stopped):
            self.btn_start_logging.clicked.disconnect()

            self.data_logger_thread.stop()
            self._reset_stop()

        elif self.data_logger_thread is None:
            from data_logger import main

            arguments_map = {}
            arguments_map[main.GUI_CONFIG] = GuiConfigHandler.create_config_file(self)
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
            QMessageBox.warning(self, 'Error',
                                'Could not save the Config-File! Look at the Log-File for further information.',
                                QMessageBox.Ok)
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

        self.create_tree_items(config_blueprint)
        # general_section
        from brickv.data_logger.configuration_validator import ConfigurationReader

        self.update_setup_tab(config_json[ConfigurationReader.GENERAL_SECTION])

        # TODO add other information
        # xively

    def btn_set_logfile_clicked(self):
        """
            Opens a FileSelectionDialog and sets the selected path for the data output file.
        """
        fn = self.__choose_file_dialog('Choose Config Destination', "CSV-Files (*.csv);;Text-Files (*.txt)")

        if fn == "":
            # cancel
            self.line_path_to_file.setText("")
            EventLogger.debug("Cancelled select Config-File-Path.")
            return

        self.line_path_to_file.setText(fn)

    def btn_set_eventfile_clicked(self):
        """
            Opens a FileSelectionDialog and sets the selected path for the event output file.
        """
        fn = self.__choose_file_dialog('Choose Eventfile destination', "Log-Files (*.log)")

        if fn == "":
            # cancel
            EventLogger.debug("Cancelled select Eventfile-Path.")
            return

        self.line_path_to_eventfile.setText(fn)

    def __choose_file_dialog(self, msg, filter_string):
        return QtGui.QFileDialog.getSaveFileName(self, msg, os.getcwd(), filter_string)

    def btn_add_device_clicked(self):
        """
            Opens the DeviceDialog in Add-Mode.
        """
        if self.logger_device_dialog is None:
            self.logger_device_dialog = LoggerDeviceDialog(self)

        # blueprint = Identifier.DEVICE_DEFINITIONS
        self.logger_device_dialog.init_dialog(self)
        self.logger_device_dialog.show()

    def btn_remove_device_clicked(self):
        """
            Removes selected Device
        """
        selected_item = self.tree_devices.selectedItems()
        for index in range(0, len(selected_item)):
            try:
                if selected_item[index] is None:
                    continue

                device_name = selected_item[index].text(0)
                device_id = selected_item[index].text(1)

                if selected_item[index].text(0) not in Identifier.DEVICE_DEFINITIONS:
                    # have to find the parent
                    current_item = selected_item[0]

                    while True:
                        if current_item.parent() is None:
                            if current_item.text(0) not in Identifier.DEVICE_DEFINITIONS:
                                EventLogger.error("Cant remove device: " + selected_item[index].text(0))
                                device_name = ""
                                device_id = ""
                                break
                            else:
                                device_name = current_item.text(0)
                                device_id = current_item.text(1)
                                break
                        else:
                            current_item = current_item.parent()

                self.remove_item_from_tree(device_name, device_id)
            except Exception as e:
                if not str(e).startswith("wrapped C/C++ object"):
                    EventLogger.error("Cant remove device: " + str(e))  # was already removed


    def btn_remove_all_devices_clicked(self):
        self.tree_devices.clear()

    def btn_clear_table_clicked(self):
        """
            Clears the Data table.
        """
        self.table_widget.setRowCount(0)

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
        ll = self.combo_console_level.currentText()

        od = collections.OrderedDict(sorted(self._gui_logger._convert_level.items()))
        for k in od.keys():
            if ll == od[k]:
                self._gui_logger.level = k
                break

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
        """
            Persists host information changes like in brickv.mainwindow
            Changes port if the host was changed
        """
        if i < 0:
            return

        self.host_index_changing = True
        self.spinbox_port.setValue(self.host_infos[i].port)
        self.host_index_changing = False

    def _port_changed(self, value):
        """
            Persists host information changes like in brickv.mainwindow
        """
        if self.host_index_changing:
            return

        i = self.combo_host.currentIndex()
        if i < 0:
            return

        self.host_infos[i].port = self.spinbox_port.value()

    def cb_xively_changed(self):
        """
            Enables/Disables widgets for xively configuration
        """
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

            # logfile path
            self.line_path_to_eventfile.setText(general_section[ConfigurationReader.GENERAL_EVENTLOG_PATH])
            # loglevel
            ll = general_section[ConfigurationReader.GENERAL_EVENTLOG_LEVEL]
            od = collections.OrderedDict(sorted(GUILogger._convert_level.items()))

            counter = 0  # TODO better way to set the combo box index?
            for k in od.keys():
                if ll == k:
                    break
                counter += 1
            self.combo_loglevel.setCurrentIndex(counter)

            # log_to_console
            def __checkbox_bool_setter(bool_value):
                if bool_value:
                    return 2
                else:
                    return 0

            self.checkbox_to_file.setChecked(
                __checkbox_bool_setter(general_section[ConfigurationReader.GENERAL_EVENTLOG_TO_FILE]))
            # log_to_file
            self.checkbox_to_console.setCheckState(
                __checkbox_bool_setter(general_section[ConfigurationReader.GENERAL_EVENTLOG_TO_CONSOLE]))

        except Exception as e:
            EventLogger.critical("Could not read the General Section of the Config-File! -> " + str(e))
            return

    def create_tree_items(self, blueprint):
        """
            Create the device tree with the given blueprint.
            Shows all possible devices, if the view_all Flag is True.
        """
        self.tree_devices.clear()
        self.tree_devices.setSortingEnabled(False)

        try:
            for dev in blueprint:
                self.__add_item_to_tree(dev)
            EventLogger.debug("Device Tree created.")

        except Exception as e:
            EventLogger.warning("DeviceTree - Exception while creating the Tree: " + str(e))

        self.tree_devices.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_devices.setSortingEnabled(True)

    def add_item_to_tree(self, item_blueprint):
        self.tree_devices.setSortingEnabled(False)

        self.__add_item_to_tree(item_blueprint)

        self.tree_devices.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_devices.setSortingEnabled(True)

    def __add_item_to_tree(self, item_blueprint):
        """
        Private function with NO sort = false
        :param item_blueprint:
        :return:
        """
        # counts topLevelItems
        lv0_counter = self.tree_devices.topLevelItemCount()

        # counts values in devices
        value_counter = 0

        # lvl0: new entry(name|UID)
        item_0 = QtGui.QTreeWidgetItem(self.tree_devices)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        # set name|UID
        self.tree_devices.topLevelItem(lv0_counter).setText(0, str(item_blueprint[Identifier.DD_NAME]))
        self.tree_devices.topLevelItem(lv0_counter).setText(1, str(item_blueprint[Identifier.DD_UID]))
        self.tree_devices.topLevelItem(lv0_counter).setToolTip(1, self.__tree_uid_tooltip)

        for item_value in item_blueprint[Identifier.DD_VALUES]:
            # lvl1: new entry(value_name|interval)
            item_1 = QtGui.QTreeWidgetItem(item_0)
            item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            interval = item_blueprint[Identifier.DD_VALUES][item_value][Identifier.DD_VALUES_INTERVAL]
            self.tree_devices.topLevelItem(lv0_counter).child(value_counter).setText(0, str(item_value))
            self.tree_devices.topLevelItem(lv0_counter).child(value_counter).setText(1, str(interval))
            self.tree_devices.topLevelItem(lv0_counter).child(value_counter).setToolTip(1, self.__tree_interval_tooltip)

            # check sub_values
            sub_values = item_blueprint[Identifier.DD_VALUES][item_value][Identifier.DD_SUBVALUES]
            if sub_values is not None:
                # counts sub values in devices
                sub_value_counter = 0
                for item_sub_value in sub_values:
                    # lvl2: new entry (sub_value_name|True/False)
                    item_2 = QtGui.QTreeWidgetItem(item_1)
                    item_2.setFlags(
                        QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    lvl2_item = self.tree_devices.topLevelItem(lv0_counter).child(value_counter).child(
                        sub_value_counter)
                    item_sub_value_value = \
                        item_blueprint[Identifier.DD_VALUES][item_value][Identifier.DD_SUBVALUES][
                            item_sub_value]
                    lvl2_item.setText(0, str(item_sub_value))
                    if item_sub_value_value:
                        lvl2_item.setCheckState(1, QtCore.Qt.Checked)
                    else:
                        lvl2_item.setCheckState(1, QtCore.Qt.Unchecked)
                    lvl2_item.setText(1, "")

                    sub_value_counter += 1
            value_counter += 1

    def remove_item_from_tree(self, item_name, item_uid):
        """
            Removes an item from the device tree. The first match is removed!
        """
        # remove first found match!
        # removed_item = False
        t0_max = self.tree_devices.topLevelItemCount()

        for t0 in range(0, t0_max):

            dev_name = self.tree_devices.topLevelItem(t0).text(0)
            dev_uid = self.tree_devices.topLevelItem(t0).text(1)

            if dev_name == item_name and dev_uid == item_uid:
                # removed_item = True
                self.tree_devices.takeTopLevelItem(t0)
                break

                # can't use this approach because of multiple selection in tree_devices
                # if not removed_item:
                # QMessageBox.information(self, 'No Device found?', 'No Device was not found and could not be deleted!', QMessageBox.Ok)

    def tree_on_change(self, item, column):
        # check for wrong input number in interval or uid
        if column == 1:
            # check if tooltip is set
            tt = str(item.toolTip(1))
            if tt != "":
                # check if tooltip is interval
                if tt == self.__tree_interval_tooltip:
                    item.setText(1, str(Utilities.parse_to_int(item.text(1))))
                # check if tooltip is uid
                elif tt == self.__tree_uid_tooltip:
                    text = item.text(1)
                    if not Utilities.is_valid_string(text, 3):
                        text = Identifier.DD_UID_DEFAULT
                    item.setText(1, text)

    def tree_on_double_click(self, item, column):
        """
            Is called, when a cell in the tree was doubleclicked.
            Is used to allow the changing of the interval
            numbers and UID's but not empty cells.
        """
        edit_flag = (
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
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

            self.tab_set(self.tab_widget.indexOf(self.tab_console), QColor(255, 0, 0),
                         os.path.join(get_resources_path(), "dialog-warning.png"))

    def table_add_row(self, csv_data):
        """
            SIGNAL function:
            Adds new CSV Data into the Table.
        """
        # disable sort
        self.table_widget.setSortingEnabled(False)

        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, QtGui.QTableWidgetItem(str(csv_data.uid)))
        self.table_widget.setItem(row, 1, QtGui.QTableWidgetItem(str(csv_data.name)))
        self.table_widget.setItem(row, 2, QtGui.QTableWidgetItem(str(csv_data.var_name)))
        self.table_widget.setItem(row, 3, QtGui.QTableWidgetItem(str(csv_data.raw_data)))
        self.table_widget.setItem(row, 4, QtGui.QTableWidgetItem(str(csv_data.timestamp)))

        if self.checkbox_data_auto_scroll.isChecked():
            self.table_widget.scrollToBottom()

        # enable sort
        self.table_widget.setSortingEnabled(True)
