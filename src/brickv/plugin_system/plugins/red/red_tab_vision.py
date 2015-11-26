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
from time import sleep
from PyQt4.QtCore import QTimer

from brickv.plugin_system.plugins.red.program_utils import ChunkedDownloaderBase
from brickv.plugin_system.plugins.red.red_tab import REDTab
from brickv.plugin_system.plugins.red.ui_red_tab_vision import Ui_REDTabVision
from brickv.async_call import async_call

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

    def __init__(self):
        REDTab.__init__(self)
        self.setupUi(self)

        self.downloader = None
        self.red = None

        self.first_tab_on_focus  = True
        self.tab_is_alive        = True
        self.refresh_in_progress = False

        self.__init_connections()
        self.update_ui_state()

    def __clear_up(self):
        self.downloader = None
        self.red = None

    def __init_connections(self):
        self.button_debug_start_motion.clicked.connect(self._button_debug_start_motion_clicked)
        self.button_debug_test_all.clicked.connect(self._button_debug_test_all_clicked)
        self.button_debug_stop_all.clicked.connect(self._button_debug_stop_all_clicked)

    def __init_red(self):
        # use the session object to get a BrickRED Object
        if self.red is not None and self.session is not None:
            return

        self.red = self.session._brick

        print "SESSION _brick : " + str(self.session._brick)
        print "REDBrick       : " + str(self.red)
        print "RED Vison      : " + str(self.red.vision_camera_available())

    def tab_on_focus(self):
        print "tab_on_focus"
        if self.first_tab_on_focus:
            self.first_tab_on_focus = False

            QTimer.singleShot(1, self.__init_red)
            QTimer.singleShot(1, self.refresh_vision_programs)

    def tab_off_focus(self):
        print "tab_off_focus"

    def tab_destroy(self):
        self.__clear_up()
        print "tab_destroy"

    def update_ui_state(self):
        if self.refresh_in_progress:
            self.progress_refresh.setVisible(True)
            self.button_refresh.setText('Refreshing...')
            self.button_refresh.setEnabled(False)
            self.button_new.setEnabled(False)
            self.button_delete.setEnabled(False)
        else:
            self.progress_refresh.setVisible(False)
            self.button_refresh.setText('Refresh')
            self.button_refresh.setEnabled(True)
            self.button_new.setEnabled(True)

    def refresh_vision_programs(self):
        def refresh_async():
            print "Refreshed!"
            sleep(5)
            return

        def cb_success():
            self.refresh_in_progress = False
            self.update_ui_state()

        def cb_error():
            print "CB_ERROR"
            pass # FIXME: report error


        self.refresh_in_progress = True
        self.update_ui_state()

        async_call(refresh_async, None, cb_success, cb_error)

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

    def _button_debug_start_motion_clicked(self):
        print "Start Motion clicked"
        def cb_vision(a, b, c, d):
            print "CB: " + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d)

        self.red.register_callback(self.red.CALLBACK_VISION_MODULE, cb_vision)

        self.tmp_id = self.red.vision_module_start("motion") # brickv.bindings.ip_connection.Error: Got invalid parameter for function 77 (-9)

    def _button_debug_test_all_clicked(self):
        print "Test all clicked"

        # print "IDs: " + str(self.tmp_id)

        # print "vision_camera_available     = " + str(self.red.vision_camera_available())
        # print "vision_get_inv_framerate    = " + str(self.red.vision_get_inv_framerate())
        # w, h = self.red.vision_get_resolution()
        # print "vision_get_resolution       = " + str(w) + " x " + str(h) # struct.error: unpack requires a string argument of length 2
        # print "vision_libs_count           = " + str(self.red.vision_libs_count()) # brickv.bindings.ip_connection.Error: Got invalid parameter for function 82 (-9)
        print "vision_lib_user_load_path   = " + str(self.red.vision_lib_user_load_path()) # brickv.bindings.ip_connection.Error: Function 90 is not supported (-10)
        # print "vision_lib_system_load_path = " + str(self.red.vision_lib_system_load_path()) # brickv.bindings.ip_connection.Error: Function 87 is not supported (-10)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)

    def _button_debug_stop_all_clicked(self):
        print "Stop all clicked = " + str(self.red.vision_stop())