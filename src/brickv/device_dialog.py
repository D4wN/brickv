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

        self._add_data = None
        self._blueprint = None
        self._logger_window = parent

        # Code Inspect changes
        self._check_mode = ""

        self.setupUi(self)
        self.signal_initialization()

    # noinspection PyUnresolvedReferences
    def signal_initialization(self):
        """
            Init of all important Signals and connections.
        """
        self.tree_device_list.itemDoubleClicked.connect(self._tree_on_double_click)
        self.btn_action_device.clicked.connect(self._btn_action_device_clicked)
        self.checkbox_fast_mode.stateChanged.connect(self._checkbox_fast_mode_checked)

    def init_dialog(self, blueprint, add_data=True):
        """
            Set the current Dialog. Add or Remove are the two
            possible Dialog Types.
            Needs to be called before the .show() Function!
        """
        self._add_data = add_data
        self._blueprint = blueprint

        if self._add_data:
            self.btn_action_device.setText("Add")
            self._check_mode = "add"
        else:
            self.btn_action_device.setText("Remove")
            self._check_mode = "remove"

        self._create_tree()

    # noinspection PyCallByClass
    def _checkbox_fast_mode_checked(self):
        """
            Function to display the Fast Mode selection.
        """
        if self.checkbox_fast_mode.isChecked():
            QMessageBox.information(self, 'Fast Mode Enabled',
                                    'Fast Mode is now Enabled! You can now ' + self._check_mode +
                                    ' Devices with a DoubleClick.',
                                    QMessageBox.Ok)

    def _tree_on_double_click(self):  # , item, column
        """
            Enabling DoubleClick to add and remove devices from the list.
        """
        if not self.checkbox_fast_mode.isChecked():
            return

        self._btn_action_device_clicked()

    def _btn_action_device_clicked(self):
        """
            Add or remove the selected device from the list/DataLogger-Config.
        """
        focused_item = self.tree_device_list.currentItem()
        if focused_item is None:
            # noinspection PyCallByClass
            QMessageBox.information(self, 'No Device', 'No Device selected! Please select a Device first.',
                                    QMessageBox.Ok)
            return

        if self._add_data:
            # add device
            dev_name = focused_item.text(0)
            dev = GuiConfigHandler.get_device_blueprint(dev_name)

            if dev is None:
                return

            suggested_uid = "Enter UID"
            for device_info in infos.get_device_infos():
                if focused_item.text(0) in device_info.name:
                    suggested_uid = device_info.uid
                    break
            dev[Identifier.DEVICE_UID] = suggested_uid

            self._logger_window.add_item_to_tree(dev)

        else:
            # remove device
            dev = focused_item.text(0)
            dev_uid = focused_item.text(1)

            self.tree_device_list.takeTopLevelItem(self.tree_device_list.indexOfTopLevelItem(focused_item))
            self._logger_window.remove_item_from_tree(dev, dev_uid)

    def _create_tree(self):
        """
            Create the tree in the corresponding Dialog Mode(Add/Remove).
        """
        self.tree_device_list.clear()
        self.tree_device_list.setSortingEnabled(False)

        if not self._add_data:
            # add second column
            self.tree_device_list.setColumnHidden(1, False)
            self.tree_device_list.headerItem().setText(1, "UID")
            self.tree_device_list.header().setDefaultSectionSize(200)
        else:
            # hide header
            self.tree_device_list.setColumnHidden(1, True)

        tree_counter = 0
        for dev_item in self._blueprint:
            # new entry
            item_0 = QtGui.QTreeWidgetItem(self.tree_device_list)
            item_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

            if not self._add_data:
                for key in dev_item.keys():
                    self.tree_device_list.topLevelItem(tree_counter).setText(0, key)
                    self.tree_device_list.topLevelItem(tree_counter).setText(1, dev_item[key])
            else:
                self.tree_device_list.topLevelItem(tree_counter).setText(0, str(dev_item))

            tree_counter += 1

        self.tree_device_list.sortItems(0, QtCore.Qt.AscendingOrder)
        self.tree_device_list.setSortingEnabled(True)
