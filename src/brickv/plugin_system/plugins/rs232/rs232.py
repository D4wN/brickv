# -*- coding: utf-8 -*-
"""
RS232 Plugin
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

rs232.py: RS232 Plugin Implementation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt4.QtGui import QTextCursor
from PyQt4.QtCore import pyqtSignal

from brickv.plugin_system.plugin_base import PluginBase
from brickv.bindings.bricklet_rs232 import BrickletRS232
from brickv.plugin_system.plugins.rs232.ui_rs232 import Ui_RS232
from brickv.async_call import async_call

from brickv.plugin_system.plugins.rs232.qhexedit import QHexeditWidget

class RS232(PluginBase, Ui_RS232):
    qtcb_read = pyqtSignal(object, int)

    def __init__(self, *args):
        PluginBase.__init__(self, BrickletRS232, *args)

        self.setupUi(self)
        self.text.setReadOnly(True)

        self.rs232 = self.device

        self.qtcb_read.connect(self.cb_read)
        self.rs232.register_callback(self.rs232.CALLBACK_READ_CALLBACK,
                                     self.qtcb_read.emit)

        self.input_combobox.addItem("")
        self.input_combobox.lineEdit().setMaxLength(58)
        self.input_combobox.lineEdit().returnPressed.connect(self.input_changed)

        self.baudrate_combobox.currentIndexChanged.connect(self.configuration_changed)
        self.parity_combobox.currentIndexChanged.connect(self.configuration_changed)
        self.stopbits_spinbox.valueChanged.connect(self.configuration_changed)
        self.wordlength_spinbox.valueChanged.connect(self.configuration_changed)
        self.hardware_flowcontrol_combobox.currentIndexChanged.connect(self.configuration_changed)
        self.software_flowcontrol_combobox.currentIndexChanged.connect(self.configuration_changed)
        self.text_type_combobox.currentIndexChanged.connect(self.text_type_changed)

        self.hextext = QHexeditWidget(self.text.font())
        self.hextext.hide()
        self.layout().insertWidget(2, self.hextext)

        self.save_button.clicked.connect(self.save_clicked)

    def cb_read(self, message, length):
        s = ''.join(message[:length])
        self.hextext.appendData(s)

        # QTextEdit breaks lines at \r and \n
        s = s.replace('\n\r', '\n').replace('\r\n', '\n')

        ascii = ''
        for c in s:
            if (ord(c) < 32 or ord(c) > 126) and not (ord(c) in (10, 13)):
                ascii += '.'
            else:
                ascii += c

        self.text.moveCursor(QTextCursor.End)
        self.text.insertPlainText(ascii)
        self.text.moveCursor(QTextCursor.End)

    def input_changed(self):
        text = self.input_combobox.currentText().encode('utf-8') + '\n\r'
        c = ['\0']*60
        for i, t in enumerate(text):
            c[i] = t

        length = len(text)
        written = 0
        while length != 0:
            written = self.rs232.write(c, length)
            c = c[written:]
            c = c + ['\0']*written
            length = length - written

        self.input_combobox.setCurrentIndex(0)

    def get_configuration_async(self, conf):
        self.baudrate_combobox.setCurrentIndex(conf.baudrate)
        self.parity_combobox.setCurrentIndex(conf.parity)
        self.stopbits_spinbox.setValue(conf.stopbits)
        self.wordlength_spinbox.setValue(conf.wordlength)
        self.hardware_flowcontrol_combobox.setCurrentIndex(conf.hardware_flowcontrol)
        self.software_flowcontrol_combobox.setCurrentIndex(conf.software_flowcontrol)
        self.save_button.setEnabled(False)

    def text_type_changed(self):
        if self.text_type_combobox.currentIndex() == 0:
            self.hextext.hide()
            self.text.show()
        else:
            self.text.hide()
            self.hextext.show()

    def configuration_changed(self):
        self.save_button.setEnabled(True)

    def save_clicked(self):
        baudrate = self.baudrate_combobox.currentIndex()
        parity = self.parity_combobox.currentIndex()
        stopbits = self.stopbits_spinbox.value()
        wordlength = self.wordlength_spinbox.value()
        hardware_flowcontrol = self.hardware_flowcontrol_combobox.currentIndex()
        software_flowcontrol = self.software_flowcontrol_combobox.currentIndex()

        self.rs232.set_configuration(baudrate, parity, stopbits, wordlength, hardware_flowcontrol, software_flowcontrol)
        self.save_button.setEnabled(False)

    def start(self):
        async_call(self.rs232.get_configuration, None, self.get_configuration_async, self.increase_error_count)
        self.rs232.enable_read_callback()
#        self.cbe_read.set_period(100)

    def stop(self):
        pass
#        self.cbe_read.set_period(0)

    def destroy(self):
        pass

    def get_url_part(self):
        return 'rs232'

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletRS232.DEVICE_IDENTIFIER
