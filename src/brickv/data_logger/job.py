""""
/*---------------------------------------------------------------------------
                                Jobs
 ---------------------------------------------------------------------------*/
"""
import Queue
import threading
import time

from brickv.data_logger.event_logger import EventLogger
from brickv.data_logger.utils import CSVWriter


class AbstractJob(threading.Thread):
    
    def __init__(self, datalogger=None, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self._exit_flag = False
        self._datalogger = datalogger
        self._job_name = "[Job:" + self.name + "]"
        
        if self._datalogger is not None:
            self._datalogger.data_queue[self.name] = Queue.Queue()
    
    def stop(self):
        self._exit_flag = True

    
    def _job(self):
        # check for datalogger object
        if self._datalogger is None:
            EventLogger.warning(self.name + " started but did not get a DataLogger Object! No work could be done.")
            return True
        return False

    def _get_data_from_queue(self):
        if self._datalogger is not None:
            return self._datalogger.data_queue[self.name].get()
        return None
    
    # Needs to be called when you end the job!
    def _remove_from_data_queue(self):
        try:
            self._datalogger.data_queue.pop(self.name)
        except KeyError as key_err:
            EventLogger.warning("Job:"+self.name+" was not ine the DataQueue! -> "+ str(key_err))

class CSVWriterJob(AbstractJob):
    '''
    This class enables the data logger to write logged data to an CSV formatted file
    '''
    def __init__(self, datalogger=None, group=None, name="CSVWriterJob", args=(), kwargs=None, verbose=None):
        target = self._job
        AbstractJob.__init__(self, datalogger=datalogger, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        
    def _job(self):
        try:
            # check for datalogger object
            if AbstractJob._job(self):
                return
    
            EventLogger.debug(self._job_name + " Started")
            csv_writer = CSVWriter(self._datalogger.default_file_path, self._datalogger.max_file_size, self._datalogger.max_file_count)
                                   
            while (True):
                if not self._datalogger.data_queue[self.name].empty():
                    csv_data = self._get_data_from_queue()
                    EventLogger.debug(self._job_name + " -> " + str(csv_data))
                    if not csv_writer.write_data_row(csv_data):
                        EventLogger.warning(self._job_name + " Could not write csv row!")
                                              
                if not self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    time.sleep(self._datalogger.job_sleep)
                
                if self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    exit_return_Value = csv_writer.close_file()
                    if exit_return_Value:
                        EventLogger.debug(self._job_name + " Closed his csv_writer")
                    else:
                        EventLogger.debug(self._job_name + " Could NOT close his csv_writer! EXIT_RETURN_VALUE=" + str(exit))
                    EventLogger.debug(self._job_name + " Finished")
                    
                    self._remove_from_data_queue()
                    break
                
        except Exception as e:
            EventLogger.critical(self._job_name + " " + str(e))
            self.stop()

class GuiDataJob(AbstractJob):
    '''
    This class enables the data logger to upload logged data to the Xively platform
    '''

    def __init__(self, datalogger=None, table_widget=None, group=None, name="GuiDataJob", args=(), kwargs=None, verbose=None):
        target = self._job
        AbstractJob.__init__(self, datalogger=datalogger, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        # TODO: implement xively logger
        EventLogger.warning(self._job_name + " Is not supported!")
        self._table_widget = table_widget

    def _job(self):
        try:
            # check for datalogger object
            if AbstractJob._job(self) or self._table_widget is None:
                return

            EventLogger.debug(self._job_name + " Started")
            #csv_writer = CSVWriter(self._datalogger.default_file_path, self._datalogger.max_file_size, self._datalogger.max_file_count)

            while (True):
                if not self._datalogger.data_queue[self.name].empty():
                    csv_data = self._get_data_from_queue()
                    EventLogger.debug(self._job_name + " -> " + str(csv_data))
                    self.__add_data_to_table(csv_data)
                    #schreib daten raus
                    #if not csv_writer.write_data_row(csv_data):
                    #    EventLogger.warning(self._job_name + " Could not write csv row!")

                if not self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    time.sleep(self._datalogger.job_sleep)

                if self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    #exit_return_Value = csv_writer.close_file()
                    #if exit_return_Value:
                    #    EventLogger.debug(self._job_name + " Closed his csv_writer")
                    #else:
                    #    EventLogger.debug(self._job_name + " Could NOT close his csv_writer! EXIT_RETURN_VALUE=" + str(exit))
                    #EventLogger.debug(self._job_name + " Finished")

                    self._remove_from_data_queue()
                    break

        except Exception as e:
            EventLogger.critical(self._job_name + " " + str(e))
            self.stop()

    def __add_data_to_table(self, csv_data):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, str(csv_data.uid))
        self.table_widget.setItem(row, 1, str(csv_data.name))
        self.table_widget.setItem(row, 2, str(csv_data.var_name))
        self.table_widget.setItem(row, 3, str(csv_data.raw_data))
        self.table_widget.setItem(row, 4, str(csv_data.timestamp))

class XivelyJob(AbstractJob):
    '''
    This class enables the data logger to upload logged data to the Xively platform
    '''
    
    def __init__(self, datalogger=None, group=None, name="XivelyJob", args=(), kwargs=None, verbose=None):
        target = self._job
        AbstractJob.__init__(self, datalogger=datalogger, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        # TODO: implement xively logger
        EventLogger.warning(self._job_name + " Is not supported!")
        
    def _job(self):
        # TODO: implement xively logger
        EventLogger.warning(self._job_name + " Is not supported!")
        try:
            # check for datalogger object
            if AbstractJob._job(self):
                return
    
            EventLogger.debug(self._job_name + " Started")
                                   
            while (True):
                if not self._datalogger.data_queue[self.name].empty():
                    # write
                    csv_data = self._get_data_from_queue()
                    EventLogger.debug(self._job_name + " -> " + str(csv_data))
                                              
                if not self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    time.sleep(self._datalogger.job_sleep)
                
                if self._exit_flag and self._datalogger.data_queue[self.name].empty():
                    # close job
                    EventLogger.debug(self._job_name + " Finished")
                    
                    self._remove_from_data_queue()
                    break
                
        except Exception as e:
            EventLogger.critical(self._job_name + " " + str(e))
            self.stop()
