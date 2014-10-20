# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

new_program_stdio.py: New Program Wizard Stdio Page

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

from PyQt4.QtGui import QWizardPage
from brickv.plugin_system.plugins.red.new_program_constants import Constants
from brickv.plugin_system.plugins.red.ui_new_program_stdio import Ui_NewProgramStdio
import os

class NewProgramStdio(QWizardPage, Ui_NewProgramStdio):
    def __init__(self, *args, **kwargs):
        QWizardPage.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.setTitle('Stdio Redirection')

    # overrides QWizardPage.initializePage
    def initializePage(self):
        self.setSubTitle('Specify how the standard input and output of the new {0} program [{1}] should be redirected.'
                         .format(Constants.language_names[self.field('language').toInt()[0]],
                                 str(self.field('name').toString())))
        self.update_ui_state()

    # overrides QWizardPage.nextId
    def nextId(self):
        return Constants.PAGE_SCHEDULE

    def update_ui_state(self):
        pass
