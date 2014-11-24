# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

program_info_python.py: Program Python Info Widget

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
from PyQt4.QtGui import QWidget
from brickv.plugin_system.plugins.red.program_info import ProgramInfo
from brickv.plugin_system.plugins.red.program_utils import Constants
from brickv.plugin_system.plugins.red.ui_program_info_python import Ui_ProgramInfoPython

class ProgramInfoPython(ProgramInfo, Ui_ProgramInfoPython):
    def __init__(self, context, *args, **kwargs):
        ProgramInfo.__init__(self, context, *args, **kwargs)

        self.setupUi(self)

        self.check_show_advanced_options.stateChanged.connect(self.update_ui_state)

    def update_ui_state(self):
        show_advanced_options = self.check_show_advanced_options.checkState() == Qt.Checked

        self.label_working_directory_title.setVisible(show_advanced_options)
        self.label_working_directory.setVisible(show_advanced_options)
        self.label_options_title.setVisible(show_advanced_options)
        self.label_options.setVisible(show_advanced_options)

        # version
        def cb_python_versions(versions):
            executable = unicode(self.program.executable)

            for version in versions:
                if version.executable == executable:
                    self.label_version.setText(version.version)
                    return

            self.label_version.setText('<unknown>')

        self.get_executable_versions('python', cb_python_versions)

        # start mode
        start_mode_api_name = self.program.cast_custom_option_value('python.start_mode', unicode, '<unknown>')
        start_mode          = Constants.get_python_start_mode(start_mode_api_name)

        self.label_start_mode.setText(Constants.python_start_mode_display_names[start_mode])

        start_mode_script_file = start_mode == Constants.PYTHON_START_MODE_SCRIPT_FILE
        start_mode_module_name = start_mode == Constants.PYTHON_START_MODE_MODULE_NAME
        start_mode_command     = start_mode == Constants.PYTHON_START_MODE_COMMAND

        self.label_script_file_title.setVisible(start_mode_script_file)
        self.label_script_file.setVisible(start_mode_script_file)
        self.label_module_name_title.setVisible(start_mode_module_name)
        self.label_module_name.setVisible(start_mode_module_name)
        self.label_command_title.setVisible(start_mode_command)
        self.label_command.setVisible(start_mode_command)

        # script file
        self.label_script_file.setText(self.program.cast_custom_option_value('python.script_file', unicode, '<unknown>'))

        # module name
        self.label_module_name.setText(self.program.cast_custom_option_value('python.module_name', unicode, '<unknown>'))

        # command
        self.label_command.setText(self.program.cast_custom_option_value('python.command', unicode, '<unknown>'))

        # working directory
        self.label_working_directory.setText(unicode(self.program.working_directory))

        # options
        self.label_options.setText('\n'.join(self.program.cast_custom_option_value_list('python.options', unicode, [])))
