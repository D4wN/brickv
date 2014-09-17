from brickv.data_logger.utils import DataLogger, CSVData

import threading, time, logging
import json, httplib

class Xively:

    #'api.xively.com'
    #"Tinkerforge xively 1.0"
    #'105813.json'
    #'WtXx2m6ItNZyFYoQyR5qnoN1GsOSAKxPMGdIaXRLYzY5ND0g'
    MIN_UPLOAD_RATE = 1         #in seconds
    #TODO: calculate this max_item_lentgh - use timer numbers vor rough estimated value 
    MAX_ITEM_LENGTH = 10000     #max item lentght; is used to prevent memeory overflows when several http errors occure

    def __init__(self, agent, feed, api_key, upload_rate):
        #member vars
        self._host = "api.xively.com"
        self._agent = agent
        self._feed = feed
        self._api_key = api_key
        self._upload_rate = DataLogger.parse_to_int(upload_rate)
        if self._upload_rate < Xively.MIN_UPLOAD_RATE:
            self._upload_rate = Xively.MIN_UPLOAD_RATE
        
        self.q = []     #the xivelqueue with ALL CSVData objects 
        self.items = {}
        self.headers = {
            "Content-Type"  : "application/x-www-form-urlencoded",
            "X-ApiKey"      : self._api_key,
            "User-Agent"    : self._agent,
        }
        self.params = "/v2/feeds/" + str(self._feed)

    def put(self, csv):  
        value = 1#temp solution   
        identifier = str(csv.name) + "-" + str(csv.var_name) 
        try:
            _, min_value, max_value = self.items[identifier]
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value
            self.items[identifier] = (value, min_value, max_value)
        except:
            self.items[identifier] = (value, value, value)  

        self.q.append(csv)
        if len(self.q) > Xively.MAX_ITEM_LENGTH:
            self.q.pop(0)#prevents giant item lists

    def upload(self):
        thread_name = "Work Thread(" + threading.current_thread().name + ")"
        logging.debug(thread_name + " started.")
        while True:
            #time.sleep(self._upload_rate * 60) # Upload data every <upload_rate>min
            
            #TODO: temporaer zum debugging!
            logging.debug(thread_name + " is going to sleep until the the next upload (X minutes).")
            time.sleep(5)
            if len(self.q) == 0:
                #no items? go to sleep
                continue

            stream_items = []
            """
            aufbau des json bodys aka data
            {"version":"1.0.0","datastreams" :[ 
                
                {"id":"example","datapoints":[
                    {"at":"2013-04-22T00:35:43Z","value":"41"},
                    {"at":"2013-04-22T00:55:43Z","value":"84"}
                ],"current_value" : "333"},
                
                {"id":"key","datapoints":[
                    {"at":"2013-04-22T00:35:43Z","value":"revalue"},
                    {"at":"2013-04-22T00:55:43Z","value":"string value"},
                ],"current_value" : "value"},
                
                {"id":"datastream","datapoints":[
                    {"at":"2013-04-22T00:35:43Z","value":"51"},
                    {"at":"2013-04-22T00:55:43Z","value":"102"},
                ],"current_value" : "1337"}
            ]
            }
            
            
            
            """
#             for identifier, value in self.items.items():
#                 stream_items.append({'id': identifier,
#                                      'current_value': value[0],
#                                      'min_value': value[1],
#                                      'max_value': value[2]})
            #temp identifier string objects
            tmp_arr = {}
            for ids in self.items.keys():
                logging.debug("ids="+str(ids))
                tmp_arr[ids] = []
                
            for csv in self.q:
                tmp_arr[str(csv.name) + "-" + str(csv.var_name) ].append((csv.uid, csv.raw_data))
            
            for ids, t in tmp_arr.items():
                logging.debug("ID="+str(ids)+" data="+str(t))

#             data = {'version': '1.0.0',
#                     'datastreams': stream_items}
            self.q = []# temp fix
#             body = json.dumps(data)
# 
#             try:
#                 http = httplib.HTTPSConnection(self._host)
#                 http.request('PUT', self.params, body, self.headers)
#                 response = http.getresponse()
#                 http.close()
# 
#                 if response.status != 200:
#                     logging.warning(thread_name + " could not upload data -> " +
#                               str(response.status) + ": " + response.reason)
#                 else:
#                     self.items = {} #reset items only if there are NO errors while uploading!
#                     
#             except Exception as e:
#                 logging.error(thread_name+ " - HTTP error: " + str(e))

            if DataLogger.THREAD_EXIT_FLAG and len(self.q) == 0: 
                logging.debug(thread_name + " finished his work.")
                break
