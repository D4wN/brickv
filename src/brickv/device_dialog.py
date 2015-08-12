# -*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog, QMessageBox
from brickv.ui_device_dialog import Ui_DeviceDialog
from PyQt4 import QtGui, QtCore
from brickv.data_logger.gui_config_handler import GuiConfigHandler
from PyQt4.QtCore import Qt
from brickv import infos

from brickv.data_logger.loggable_devices import Identifier


# noinspection PyTypeChecker
class LoggerDeviceDialog(QDialog, Ui_DeviceDialog):
    """
        Function and Event handling class for the Ui_DeviceDialog.
    """

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self._logger_window = parent
        self._no_connected_device_string = "No Connected Devices found"
        self._list_separator_string = "----------------------------------------" #TODO check if needed?

        self.setupUi(self)
        self.signal_initialization()

    # noinspection PyUnresolvedReferences
    def signal_initialization(self):
        """
            Init of all important Signals and connections.
        """
        self.btn_add_device.clicked.connect(self._btn_add_device_clicked)
        self.btn_add_all_devices.clicked.connect(self._btn_add_all_devices_clicked)
        self.btn_cancel.clicked.connect(self._btn_cancel_clicked)

    def init_dialog(self):
        """
           Builds the Tree.
        """
        connected_devices = infos.get_device_infos()
        if len(connected_devices) <= 0:
            self.btn_add_all_devices.setEnabled(False)
        else:
            self.btn_add_all_devices.setEnabled(True)

        self._create_tree()

    def _btn_cancel_clicked(self):
        self.close()

    def _btn_add_all_devices_clicked(self):
        print "Button add all clicked!"
        #TODO check if devices are allready in list
        #add all missing devices from list

    def _btn_add_device_clicked(self, uid=None):
        """
            Add or remove the selected device from the list/DataLogger-Config.
        """
        return

        focused_item = self.list_widget.currentItem()
        if focused_item is None:
            QMessageBox.information(self, 'No Device', 'No Device selected! Please select a Device first.',
                                    QMessageBox.Ok)
            return

        # add device
        dev_name = focused_item.text(0)
        dev = GuiConfigHandler.get_device_blueprint(dev_name)

        if dev is None:
            return

        #suggested_uid = "Enter UID"
        #for device_info in infos.get_device_infos():
        #    if focused_item.text(0) in device_info.name:
        #        suggested_uid = device_info.uid
        #        break

        if uid is not None:
            dev[Identifier.DEVICE_UID] = uid
        else:
            dev[Identifier.DEVICE_UID] = "Enter UID"

        self._logger_window.add_item_to_tree(dev)

    def _create_tree(self, connected_devices=0):
        """
            Create the tree in the corresponding Dialog Mode(Add/Remove).
        """
        list_blueprint = []

        # connected devices
        if connected_devices <= 0:
            connected_devices = infos.get_device_infos()

        if len(connected_devices) <= 0:
            list_blueprint.append(self._no_connected_device_string)
        else:
            for device_info in connected_devices:
                if device_info.name in Identifier.DEVICE_DEFINITIONS:
                    list_blueprint.append(device_info.name + " [" +device_info.uid+ "]")

        #self.combo_devices.insertSeparator(self.combo_devices.count() + 1)
        list_blueprint.append(self._list_separator_string)

        # list of all devices
        for device in Identifier.DEVICE_DEFINITIONS:
            list_blueprint.append(device)

        self.list_widget.clear()
        for dev in list_blueprint:
            self.list_widget.addItem(str(dev))
