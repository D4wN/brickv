# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

red_tab_settings_services.py: RED settings services tab implementation FIXME

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
import os
from PyQt4.QtCore import pyqtSignal
from brickv.bindings.brick_red import BrickRED, RED
from brickv.bindings.ip_connection import IPConnection
from brickv.config import HostInfo
from brickv.plugin_system.plugins.red.api import REDBrick

from brickv.plugin_system.plugins.red.program_utils import ChunkedDownloaderBase
from brickv.plugin_system.plugins.red.red_tab import REDTab
from brickv.plugin_system.plugins.red.ui_red_tab_vision import Ui_REDTabVision

class TEMP_MAINWINDOW():  # FIXME how do i get the ipcon in one of the tabs? (vision)
    TEMP_IPCON = None

class MyDownloader(ChunkedDownloaderBase):
    def __init__(self, widget):
        ChunkedDownloaderBase.__init__(self, widget.session)

        self._widget = widget
        self.session = widget.session

    def report_error(self, message, *args):
        print "MyDownloader::ERROR = " + str(message)

    def set_progress_maximum(self, maximum):
        print "MyDownloader::set_progress_maximum = " +str(maximum)

    def set_progress_value(self, value, message):
        print "MyDownloader::set_progress_value = " +str(value) + ", " +str(message)

    def done(self):
        print "MyDownloader::done = DONE!"
        self._widget.downloader = None


class REDTabVision(REDTab, Ui_REDTabVision):

    qtcb_enumerate = pyqtSignal(str, str, 'char', type((0,)), type((0,)), int, int)

    def __init__(self):
        REDTab.__init__(self)

        self.setupUi(self)

        self.downloader = None
        self.red = None

        print str(self.session)


        self.__init_connections()
        self.__init_uid()

    def __init_connections(self):
        self.qtcb_enumerate.connect(self.cb_enumerate)

        self.button_debug_start_motion.clicked.connect(self._button_debug_start_motion_clicked)
        self.button_debug_stop_all.clicked.connect(self._button_debug_stop_all_clicked)

        # self.btn_push.clicked.connect(self._start_download)

    def __init_uid(self):
        #print str(HostInfo.host) + ":" + str(HostInfo.port)
        # self.ipcon = IPConnection()  # TODO old_ipcon
        self.ipcon = TEMP_MAINWINDOW.TEMP_IPCON
        self.uid = None
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, self.qtcb_enumerate.emit)
        #self.ipcon.connect(HostInfo.host, HostInfo.port) # TODO old_ipcon

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type):
        if self.uid is not None:
            return

        # if enumeration_type in [IPConnection.ENUMERATION_TYPE_AVAILABLE, IPConnection.ENUMERATION_TYPE_CONNECTED]:
        #    evice_info = infos.get_info(uid)

            # device_info == None:
        print "br:"+str(BrickRED.DEVICE_IDENTIFIER)
        if device_identifier == BrickRED.DEVICE_IDENTIFIER:
            print "RedBrick: " + str(uid)
            self.uid = uid
            if self.red is None:
                pass
                self.red = RED(self.uid, self.ipcon)
                print "RED Test: API" + str(self.red.api_version)
            # self.ipcon.disconnect()  # TODO old_ipcon
        else:
            print "Other: " + str(uid)

    def _button_debug_start_motion_clicked(self):
        pass

    def _button_debug_stop_all_clicked(self):
        pass

    def _start_download(self):
        if self.downloader is not None:
            return

        print "Start Download..."
        print str(self.session)

        red_path = u'/home/tf/programs/Dummy/bin/main_stop.py'
        my_path = "C:\\Programmierung\\Repos\\Python\\TinkervisionBrickv\\main_stop.py"

        self.downloader = MyDownloader(self)
        print "Prepared = " + str(self.downloader.prepare(red_path))

        my_path_exists = os.path.exists(my_path)
        print "Path exists = " + str(my_path_exists)
        if my_path_exists:
            print "Deleting(DEBUG): " + str(my_path)
            os.remove(my_path)

        self.downloader.start(my_path)
        print "Remaining: " + str(self.downloader.remaining_source_size)

        count = 0
        while count != 20:
            count += 1
            print "Progress = " + str(self.downloader.current_progress)
            #sleep(1)

    def tab_on_focus(self):
        print "tab_on_focus"

    def tab_off_focus(self):
        print "tab_off_focus"

    def tab_destroy(self):
        print "tab_destroy"