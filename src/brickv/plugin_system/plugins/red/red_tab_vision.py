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
from collections import OrderedDict
import os
from time import sleep
from PyQt4.QtCore import QTimer

from brickv.plugin_system.plugins.red.program_utils import ChunkedDownloaderBase
from brickv.plugin_system.plugins.red.red_tab import REDTab
from brickv.plugin_system.plugins.red.ui_red_tab_vision import Ui_REDTabVision
from brickv.async_call import async_call
from brickv.plugin_system.plugins.red.vision_wizard import VisionWizardContext
from brickv.plugin_system.plugins.red.vision_wizard_new import VisionWizardNew

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
        self.vision_module_list = OrderedDict()

        self.first_tab_on_focus  = True
        self.tab_is_alive        = True
        self.refresh_in_progress = False
        self.new_vision_wizard  = None

        self.__init_connections()
        self.update_ui_state()

    def __clear_up(self):
        self.downloader = None
        self.red = None

        if self.new_vision_wizard != None:
            self.new_vision_wizard.close()

    def __init_connections(self):
        self.button_debug_start_motion.clicked.connect(self._button_debug_start_motion_clicked)
        self.button_debug_test_all.clicked.connect(self._button_debug_test_all_clicked)
        self.button_debug_stop_all.clicked.connect(self._button_debug_stop_all_clicked)
        self.button_new.clicked.connect(self.show_new_vision_wizard)

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
            #sleep(5)
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

    def __check_result(self, result):
        if result.result != 0:
            # FIXME error handling
            return False
        return True

    def get_vision_modules(self):
        if self.red is None:
            return  # FIXME Error Message

        result = self.red.vision_libs_count()
        if not self.__check_result(result):
            print "get_vision_modules::vision_libs_count"
            return
        lib_count = result.count
        print "lib_count = " + str(lib_count)

        # get module names
        for i in range(0, lib_count):
            result = self.red.vision_lib_name_path(i)
            if not self.__check_result(result):
                print "get_vision_modules::vision_lib_name_path"
                return
            self.vision_module_list[result.name] = OrderedDict()

            # get parameter and descriptions
            para_result = self.red.vision_lib_parameters_count(result.name)
            if not self.__check_result(para_result):
                print "get_vision_modules::vision_lib_parameters_count"
                return
            for j in range(0, para_result.count):
                para_desc = self.red.vision_lib_parameter_describe(result.name, j)
                if not self.__check_result(para_desc):
                    continue
                self.vision_module_list[result.name][para_desc.name] = para_desc
                #print "para_desc = " + str(para_desc)
        print "module_list = \n" + str(self.vision_module_list)

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
        self.get_vision_modules()

    def _button_debug_test_all_clicked(self):
        print "Test all clicked"

        print "vision_is_valid                  = " + str(self.red.vision_is_valid())
        print "vision_camera_available          = " + str(self.red.vision_camera_available())
        print "def vision_get_framesize         = " + str(self.red.vision_get_framesize())
        print "vision_get_frameperiod           = " + str(self.red.vision_get_frameperiod())
        print "vision_libs_count                = " + str(self.red.vision_libs_count())
        print "vision_lib_get_user_prefix       = " + str(self.red.vision_lib_get_user_prefix())
        print "vision_lib_get_system_load_path  = " + str(self.red.vision_lib_get_system_load_path())
        print "vision_libs_loaded_count         = " + str(self.red.vision_libs_loaded_count())
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)
        # print "" + str(self.red)

    def _button_debug_stop_all_clicked(self):
        print "Stop all clicked = " + str(self.red.vision_stop())

    def show_new_vision_wizard(self):
        print "show_new_vision_wizard"
        self.button_new.setEnabled(False)

        # if self.stacked_container.count() > 1:
        #     current_widget = self.stacked_container.currentWidget()
        # else:
        #     current_widget = None
        #
        # if current_widget != None:
        #     current_widget.set_program_callbacks_enabled(False)
        #
        identifiers = []
        #
        # for i in range(self.tree_programs.topLevelItemCount()):
        #     identifiers.append(self.tree_programs.topLevelItem(i).data(0, Qt.UserRole).program.identifier)

        context = VisionWizardContext(self.session, identifiers, self.script_manager, self.image_version)

        self.new_vision_wizard = VisionWizardNew(self, context)

        self.new_vision_wizard.exec_()
        self.button_new.setEnabled(True) # FIXME temp only

        # if self.new_vision_wizard.upload_successful:
        #     self.add_program_to_tree(self.new_vision_wizard.program)
        #     self.tree_programs.topLevelItem(self.tree_programs.topLevelItemCount() - 1).setSelected(True)
        #
        #     for i in reversed(range(self.tree_programs.topLevelItemCount() - 1)):
        #         self.tree_programs.topLevelItem(i).setSelected(False)