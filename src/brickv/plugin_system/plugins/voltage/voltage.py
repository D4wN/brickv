# -*- coding: utf-8 -*-  
"""
Voltage Plugin
Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

voltage.py: Voltage Plugin Implementation

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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QVBoxLayout, QLabel, QHBoxLayout

from brickv.plugin_system.plugin_base import PluginBase
from brickv.bindings.bricklet_voltage import BrickletVoltage
from brickv.plot_widget import PlotWidget
from brickv.async_call import async_call
from brickv.callback_emulator import CallbackEmulator

class CurrentLabel(QLabel):
    def setText(self, text):
        text = "Voltage: " + text + " V"
        super(CurrentLabel, self).setText(text)
    
class Voltage(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickletVoltage, *args)
        
        self.vol = self.device

        self.cbe_voltage = CallbackEmulator(self.vol.get_voltage,
                                            self.cb_voltage,
                                            self.increase_error_count)

        self.voltage_label = CurrentLabel('Voltage: ')
        
        self.current_value = None
        
        plot_list = [['', Qt.red, self.get_current_value]]
        self.plot_widget = PlotWidget('Voltage [mV]', plot_list)
        
        layout_h = QHBoxLayout()
        layout_h.addStretch()
        layout_h.addWidget(self.voltage_label)
        layout_h.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h)
        layout.addWidget(self.plot_widget)
        
    def start(self):
        async_call(self.vol.get_voltage, None, self.cb_voltage, self.increase_error_count)
        self.cbe_voltage.set_period(100)
        
        self.plot_widget.stop = False
        
    def stop(self):
        self.cbe_voltage.set_period(0)
        
        self.plot_widget.stop = True

    def destroy(self):
        pass

    def get_url_part(self):
        return 'voltage'

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletVoltage.DEVICE_IDENTIFIER

    def get_current_value(self):
        return self.current_value

    def cb_voltage(self, voltage):
        self.current_value = voltage
        self.voltage_label.setText(str(voltage/1000.0))
