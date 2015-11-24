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

from brickv.plugin_system.plugins.red.program_utils import ChunkedDownloaderBase
from brickv.plugin_system.plugins.red.red_tab import REDTab
from brickv.plugin_system.plugins.red.ui_red_tab_vision import Ui_REDTabVision


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

        print "WORKING YEHA! " + str(self.session)

        self.btn_push.clicked.connect(self._start_download)

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