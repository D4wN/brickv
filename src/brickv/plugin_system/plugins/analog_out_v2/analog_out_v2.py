# -*- coding: utf-8 -*-  
"""
Analog Out 2.0 Plugin
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

analog_out_v2.py: Analog Out 2.0 Plugin Implementation

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

from brickv.plugin_system.plugin_base import PluginBase
from brickv.bindings import ip_connection
from brickv.bindings.bricklet_analog_out_v2 import BrickletAnalogOutV2
from brickv.async_call import async_call

from PyQt4.QtGui import QVBoxLayout, QLabel, QHBoxLayout, QSpinBox, QComboBox

class AnalogOutV2(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickletAnalogOutV2, *args)
        
        self.ao = self.device
        
        self.voltage_label = QLabel('Output Voltage (mV): ')
        self.voltage_box = QSpinBox()
        self.voltage_box.setMinimum(0)

        # TODO: Get max output by reading input value
        self.voltage_box.setMaximum(16000)
        self.voltage_box.setSingleStep(1)
        self.mode_label = QLabel('Mode: ')
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Normal Mode")
        self.mode_combo.addItem("1k Ohm resistor to ground")
        self.mode_combo.addItem("100k Ohm resistor to ground")
        self.mode_combo.addItem("500k Ohm resistor to ground")
        
        # TODO: Add label for input voltage
        # TODO: Add CheckBox and SpinBox to force input voltage
        
        layout_h1 = QHBoxLayout()
        layout_h1.addStretch()
        layout_h1.addWidget(self.voltage_label)
        layout_h1.addWidget(self.voltage_box)
        layout_h1.addStretch()
        
        layout_h2 = QHBoxLayout()
        layout_h2.addStretch()
        layout_h2.addWidget(self.mode_label)
        layout_h2.addWidget(self.mode_combo)
        layout_h2.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h2)
        layout.addLayout(layout_h1)
        layout.addStretch()
        
        self.voltage_box.editingFinished.connect(self.voltage_finished)
        self.mode_combo.activated.connect(self.mode_changed)
        
    def start(self):
        async_call(self.ao.get_voltage, None, self.voltage_box.setValue, self.increase_error_count)
        async_call(self.ao.get_mode, None, self.mode_combo.setCurrentIndex, self.increase_error_count)
        
    def stop(self):
        pass

    def destroy(self):
        pass

    def get_url_part(self):
        return 'analog_out_v2'

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletAnalogOutV2.DEVICE_IDENTIFIER
    
    def voltage_finished(self):
        value = self.voltage_box.value()
        try:
            self.ao.set_voltage(value)
        except ip_connection.Error:
            return
        
        self.mode_combo.setCurrentIndex(0)
        
    def mode_changed(self, mode):
        try:
            self.ao.set_mode(mode)
        except ip_connection.Error:
            return
        
        self.voltage_box.setValue(0)
