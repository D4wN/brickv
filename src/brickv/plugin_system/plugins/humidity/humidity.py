# -*- coding: utf-8 -*-  
"""
Humidity Plugin
Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

humidity.py: Humidity Plugin Implementation

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
from brickv.plot_widget import PlotWidget
from brickv.bindings.bricklet_humidity import BrickletHumidity
from brickv.async_call import async_call
from brickv.utils import CallbackEmulator

from PyQt4.QtGui import QVBoxLayout, QLabel, QHBoxLayout
from PyQt4.QtCore import Qt

class HumidityLabel(QLabel):
    def setText(self, text):
        text = "Humidity: " + text + " %RH (Relative Humidity)"
        super(HumidityLabel, self).setText(text)
    
class Humidity(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickletHumidity, *args)

        self.hum = self.device

        self.cbe_humidity = CallbackEmulator(self.hum.get_humidity,
                                             self.cb_humidity,
                                             self.increase_error_count)

        self.humidity_label = HumidityLabel('Humidity: ')

        self.current_value = None

        plot_list = [['', Qt.red, self.get_current_value]]
        self.plot_widget = PlotWidget('Relative Humidity [%RH]', plot_list)

        layout_h = QHBoxLayout()
        layout_h.addStretch()
        layout_h.addWidget(self.humidity_label)
        layout_h.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h)
        layout.addWidget(self.plot_widget)

    def start(self):
        async_call(self.hum.get_humidity, None, self.cb_humidity, self.increase_error_count)
        self.cbe_humidity.set_period(100)
        
        self.plot_widget.stop = False
        
    def stop(self):
        self.cbe_humidity.set_period(0)
        
        self.plot_widget.stop = True

    def destroy(self):
        pass

    def get_url_part(self):
        return 'humidity'

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletHumidity.DEVICE_IDENTIFIER
    
    def get_current_value(self):
        return self.current_value

    def cb_humidity(self, humidity):
        self.current_value = humidity/10.0
        self.humidity_label.setText(str(humidity/10.0))
