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
        
        if self._datalogger != None:
            self._datalogger.data_queue[self.name] = Queue.Queue()
    
    def stop(self):
        self._exit_flag = True

    
    def _job(self):
        # check for datalogger object
        if self._datalogger == None:
            EventLogger.warning(self.name + " started but did not get a DataLogger Object! No work could be done.")
            return True
        return False

    def _get_data_from_queue(self):
        if self._datalogger != None:
            return self._datalogger.data_queue[self.name].get()
        return None
    
    #Needs to be called when you end the job!
    def _remove_from_data_queue(self):
        try:
            self._datalogger.data_queue.pop(self.name)
        except KeyError as key_err:
        #TODO: key_err usen?
            pass   
    

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
            csv_writer = CSVWriter(self._datalogger.default_file_path)
                                   
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
            
