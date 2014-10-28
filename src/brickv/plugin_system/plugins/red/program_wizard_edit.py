# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

program_wizard_edit.py: Edit Program Wizard

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

from PyQt4.QtCore import Qt, QVariant
from PyQt4.QtGui import QWizard
from brickv.plugin_system.plugins.red.program_wizard import ProgramWizard
from brickv.plugin_system.plugins.red.program_wizard_utils import *
from brickv.plugin_system.plugins.red.program_page_general import ProgramPageGeneral
from brickv.plugin_system.plugins.red.program_page_files import ProgramPageFiles
from brickv.plugin_system.plugins.red.program_page_java import ProgramPageJava
from brickv.plugin_system.plugins.red.program_page_python import ProgramPagePython
from brickv.plugin_system.plugins.red.program_page_ruby import ProgramPageRuby
from brickv.plugin_system.plugins.red.program_page_arguments import ProgramPageArguments
from brickv.plugin_system.plugins.red.program_page_stdio import ProgramPageStdio
from brickv.plugin_system.plugins.red.program_page_schedule import ProgramPageSchedule
from brickv.plugin_system.plugins.red.program_page_summary import ProgramPageSummary
from brickv.plugin_system.plugins.red.program_page_upload import ProgramPageUpload

class ProgramWizardEdit(ProgramWizard):
    def __init__(self, session, program, identifiers, script_manager, *args, **kwargs):
        ProgramWizard.__init__(self, session, identifiers, script_manager, *args, **kwargs)

        self.program = program

        self.setWindowTitle('Edit Program')

        self.setPage(Constants.PAGE_ARGUMENTS, ProgramPageArguments())

    # overrides QWizard.nextId
    def nextId(self):
        return -1

    # overrides ProgramWizard.get_field
    def get_field(self, name):
        if name == Constants.FIELD_NAME:
            return QVariant(unicode(self.program.custom_options.get(Constants.FIELD_NAME, '<unknown>')))
        elif name == Constants.FIELD_LANGUAGE:
            api_language = unicode(self.program.custom_options.get(Constants.FIELD_LANGUAGE, '<unknown>'))

            try:
                language_id = Constants.api_languages.keys()[Constants.api_languages.values().index(api_language)]
            except:
                language_id = LANGUAGE_INVALID

            return QVariant(language_id)
        else:
            return ProgramWizard.get_field(self, name)

    @property
    def available_files(self):
        return [] # FIXME

    @property
    def available_directories(self):
        return [] # FIXME