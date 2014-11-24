# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

program_info_files.py: Program Files Info Widget

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

from PyQt4.QtCore import Qt, QDateTime, QVariant
from PyQt4.QtGui import QIcon, QWidget, QStandardItemModel, QStandardItem, QAbstractItemView, QLineEdit,\
                        QSortFilterProxyModel, QFileDialog, QProgressDialog, QMessageBox, QInputDialog
from brickv.plugin_system.plugins.red.api import *
from brickv.plugin_system.plugins.red.ui_program_info_files import Ui_ProgramInfoFiles
from brickv.async_call import async_call
from brickv.program_path import get_program_path
import os
import json

def expand_directory_walk_to_lists(directory_walk):
    files = {}
    directories = set()

    def expand(root, dw):
        if 'c' in dw:
            if len(root) > 0:
                directories.add(root)

            for child_name, child_dw in dw['c'].iteritems():
                expand(os.path.join(root, child_name), child_dw)
        else:
            files[root] = dw

    expand('', directory_walk)

    return files, sorted(list(directories))


def get_file_display_size(size):
    if size < 1024:
        return str(size) + ' Bytes'
    else:
        return str(size / 1024) + ' kiB'


def merge_path(item, path):
    parent = item.parent()
    if parent:
        return merge_path(parent, os.path.join(unicode(parent.text()), path))
    else:
        return path


def expand_directory_walk_to_model(directory_walk, model, folder_icon, file_icon):
    def create_last_modified_item(last_modified):
        item = QStandardItem(QDateTime.fromTime_t(last_modified).toString('yyyy-MM-dd HH:mm:ss'))
        item.setData(QVariant(last_modified))

        return item

    def expand(parent_item, name, dw):
        if 'c' in dw:
            if name == None:
                name_item = parent_item
                size_item = None
            else:
                name_item = QStandardItem(name)
                name_item.setData(QVariant(folder_icon), Qt.DecorationRole)

                size_item          = QStandardItem('')
                last_modified_item = create_last_modified_item(int(dw['l']))

                parent_item.appendRow([name_item, size_item, last_modified_item])

            size = 0

            for child_name, child_dw in dw['c'].iteritems():
                size += expand(name_item, child_name, child_dw)

            if size_item != None:
                size_item.setText(get_file_display_size(size))
                size_item.setData(QVariant(size))

            return size
        else:
            name_item = QStandardItem(name)
            name_item.setData(QVariant(file_icon), Qt.DecorationRole)

            size      = int(dw['s'])
            size_item = QStandardItem(get_file_display_size(size))
            size_item.setData(QVariant(size))

            last_modified_item = create_last_modified_item(int(dw['l']))

            parent_item.appendRow([name_item, size_item, last_modified_item])

            return size

    expand(model.invisibleRootItem(), None, directory_walk)

    return model


class FilesProxyModel(QSortFilterProxyModel):
    # overrides QSortFilterProxyModel.lessThan
    def lessThan(self, left, right):
        # size and last modified
        if left.column() in [1, 2]:
            return left.data(Qt.UserRole + 1).toInt()[0] < right.data(Qt.UserRole + 1).toInt()[0]

        return QSortFilterProxyModel.lessThan(self, left, right)


class ProgramInfoFiles(QWidget, Ui_ProgramInfoFiles):
    def __init__(self, context, update_main_ui_state, set_widget_enabled, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.session                 = context.session
        self.script_manager          = context.script_manager
        self.program                 = context.program
        self.update_main_ui_state    = update_main_ui_state
        self.set_widget_enabled      = set_widget_enabled
        self.bin_directory           = os.path.join(unicode(self.program.root_directory), 'bin')
        self.refresh_in_progress     = False
        self.available_files         = {}
        self.available_directories   = []
        self.folder_icon             = QIcon(os.path.join(get_program_path(), "folder-icon.png"))
        self.file_icon               = QIcon(os.path.join(get_program_path(), "file-icon.png"))
        self.tree_files_model        = QStandardItemModel(self)
        self.tree_files_model_header = ['Name', 'Size', 'Last Modified']
        self.tree_files_proxy_model  = FilesProxyModel(self)
        self.rename_from             = ""

        self.tree_files_model.setHorizontalHeaderLabels(self.tree_files_model_header)
        self.tree_files_proxy_model.setSourceModel(self.tree_files_model)
        self.tree_files.setModel(self.tree_files_model)
        self.tree_files.setModel(self.tree_files_proxy_model)
        self.tree_files.setColumnWidth(0, 210)
        self.tree_files.setColumnWidth(1, 85)

        self.tree_files.selectionModel().selectionChanged.connect(self.update_ui_state)
        self.tree_files_model.itemChanged.connect(self.tree_file_item_changed)
        self.button_upload_files.clicked.connect(self.upload_files)
        self.button_download_files.clicked.connect(self.download_selected_files)
        self.button_rename_file.clicked.connect(self.rename_selected_file)
        self.button_delete_files.clicked.connect(self.delete_selected_files)

    def update_ui_state(self):
        selection_count = len(self.tree_files.selectionModel().selectedRows())

        self.set_widget_enabled(self.button_download_files, selection_count > 0)
        self.set_widget_enabled(self.button_rename_file, selection_count == 1)
        self.set_widget_enabled(self.button_delete_files, selection_count > 0)

    def tree_file_item_changed(self, item):
        _from = self.rename_from
        _to = self.rename_from.replace(os.path.split(self.rename_from)[1], unicode(item.text()))
        print unicode(_from)
        print unicode(_to)
        self.rename_from = ""

    def refresh_files(self):
        def cb_directory_walk(result):
            if result == None or len(result.stderr) > 0:
                self.refresh_in_progress = False
                self.update_main_ui_state()
                return # FIXME: report error

            def expand_async(data):
                directory_walk        = json.loads(data)
                available_files       = {}
                available_directories = []

                if directory_walk != None:
                    available_files, available_directories = expand_directory_walk_to_lists(directory_walk)

                return directory_walk, available_files, available_directories

            def cb_expand_success(args):
                directory_walk, available_files, available_directories = args

                self.available_files       = available_files
                self.available_directories = available_directories
                self.refresh_in_progress   = False
                self.update_main_ui_state()

                self.tree_files_model.itemChanged.disconnect(self.tree_file_item_changed)
                expand_directory_walk_to_model(directory_walk, self.tree_files_model, self.folder_icon, self.file_icon)
                self.tree_files_model.itemChanged.connect(self.tree_file_item_changed)

                self.tree_files.header().setSortIndicator(0, Qt.AscendingOrder)

            def cb_expand_error():
                pass # FIXME: report error

            async_call(expand_async, result.stdout, cb_expand_success, cb_expand_error)

        self.refresh_in_progress = True
        self.update_main_ui_state()

        width1 = self.tree_files.columnWidth(0)
        width2 = self.tree_files.columnWidth(1)

        self.tree_files_model.clear()
        self.tree_files_model.setHorizontalHeaderLabels(self.tree_files_model_header)
        self.tree_files.setColumnWidth(0, width1)
        self.tree_files.setColumnWidth(1, width2)

        self.script_manager.execute_script('directory_walk', cb_directory_walk,
                                           [self.bin_directory], max_len=1024*1024)

    def upload_files(self):
        print 'upload_files'

    def download_selected_files(self):
        def file_download_pd_closed():
            if len(files_to_download) > 0:
                QMessageBox.warning(None,
                                    'Program | Filess',
                                    'Download could not finish.',
                                    QMessageBox.Ok)
            else:
                QMessageBox.information(None,
                                        'Program | Filess',
                                        'Download complete!',
                                        QMessageBox.Ok)

        selected_indexes = self.tree_files.selectedIndexes()
        if len(selected_indexes) == 0:
            return

        selected_indexes_chunked = zip(*[iter(selected_indexes)] * 3)

        dirs_to_create = []
        files_to_download = {}

        for selected_index_chunked in selected_indexes_chunked:
            selected_item = self.tree_files_model.itemFromIndex\
                (self.tree_files_proxy_model.mapToSource(selected_index_chunked[0]))
            path = merge_path(selected_item, unicode(selected_item.text()))

            for directory in self.available_directories:
                if path in directory:
                    dirs_to_create.append(directory)
            for file_path in self.available_files:
                if path in file_path:
                    files_to_download[file_path] = self.available_files[file_path]

        files_download_dir = unicode(QFileDialog.getExistingDirectory(self, "Choose Download Location"))

        if files_download_dir == "":
            return

        for directory in dirs_to_create:
            try:
                dir_path = os.path.join(files_download_dir, directory)

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                with open(os.path.join(unicode(dir_path),
                                       unicode('write_test_file')),
                          'wb') as fh_write_test:
                    fh_write_test.write("1")
                os.remove(os.path.join(unicode(dir_path),
                                       unicode('write_test_file')))
            except:
                QMessageBox.critical(None,
                                     'Program | Logs',
                                     'Directory not writeable.',
                                     QMessageBox.Ok)
                return

        if len(files_to_download) <= 0:
            QMessageBox.information(None,
                                    'Program | Filess',
                                    'Download complete!',
                                    QMessageBox.Ok)
            return

        file_download_pd = QProgressDialog(str(len(files_to_download))+" file(s) remaining...",
                                          "Cancel",
                                          0,
                                          100,
                                          self)
        file_download_pd.setWindowTitle("Download Progress")
        file_download_pd.setAutoReset(False)
        file_download_pd.setAutoClose(False)
        file_download_pd.setMinimumDuration(0)
        file_download_pd.canceled.connect(file_download_pd_closed)
        file_download_pd.setValue(0)

        def cb_open(red_file):
            def cb_read_status(bytes_read, max_length):
                if file_download_pd:
                    if file_download_pd.wasCanceled():
                        return
                    files_remaining = str(len(files_to_download))
                    current_percent = int(float(bytes_read)/float(max_length) * 100)
    
                    file_download_pd.setLabelText(files_remaining+" file(s) remaining...")
                    file_download_pd.setValue(current_percent)
    
                    if current_percent == 100:
                        file_download_pd.setValue(0)

            def cb_read(red_file, result):
                red_file.release()
                if result is not None:
                    # Success
                    read_file_path = unicode(files_to_download.keys()[0])
                    with open(os.path.join(unicode(files_download_dir), read_file_path), 'wb') as fh_file_write:
                        fh_file_write.write(result.data)

                    if file_download_pd.wasCanceled():
                        return

                    if read_file_path in files_to_download:
                        files_to_download.pop(read_file_path, None)

                    if len(files_to_download) == 0:
                        file_download_pd.close()
                        return

                    if not file_download_pd.wasCanceled():
                        file_download_pd.setLabelText(str(len(files_to_download))+" file(s) remaining...")
                        file_download_pd.setValue(0)
                        async_call(REDFile(self.session).open,
                                   (os.path.join(self.bin_directory, files_to_download.keys()[0]),
                                   REDFile.FLAG_READ_ONLY | REDFile.FLAG_NON_BLOCKING, 0, 0, 0),
                                   cb_open,
                                   cb_open_error)

                else:
                    # TODO: Error popup for user?
                    file_download_pd.close()
                    print 'download_selected_files cb_open cb_read', result

            red_file.read_async(int(files_to_dqtreeviewownload.values()[0]['s']),
                                lambda x: cb_read(red_file, x),
                                cb_read_status)

        def cb_open_error(result):
            # TODO: Error popup for user?
            file_download_pd.close()
            print 'download_selected_files cb_open_error', result

        if len(files_to_download) > 0:
            async_call(REDFile(self.session).open,
                       (os.path.join(self.bin_directory, files_to_download.keys()[0]),
                       REDFile.FLAG_READ_ONLY | REDFile.FLAG_NON_BLOCKING, 0, 0, 0),
                       cb_open,
                       cb_open_error)

    def rename_selected_file(self):
        selected_indexes = self.tree_files.selectedIndexes()
        if len(selected_indexes) != 3:
            return

        selected_item = self.tree_files_model.itemFromIndex\
            (self.tree_files_proxy_model.mapToSource(selected_indexes[0]))
        name, ok = QInputDialog.getText(self, "Rename File/Directory", "", QLineEdit.Normal)
        if ok and name != "":
            self.rename_from = unicode(merge_path(selected_item, unicode(selected_item.text())))
            selected_item.setText(unicode(name))

    def delete_selected_files(self):
        selected_items = self.tree_files.selectedItems()

        if len(selected_items) == 0:
            return

        filenames = [unicode(selected_item.text()) for selected_item in selected_items]

        print 'delete_selected_files', filenames
