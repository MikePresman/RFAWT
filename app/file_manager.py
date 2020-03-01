import os
import datetime as dt
import math

directory = r'C:\LAN_Public'

class FileManager(object):    
    
    def __init__(self):
        os.chdir(directory)

    def walk_root_folder(self):
        
        #filenames
        print(os.listdir(directory))

        #for file in os.listdir(directory):

        for filename in os.scandir(directory):
            print(filename.path)
            print(filename.stat())

            #file_size in kb
            file_size = (int(filename.stat()[6]))/(1024)
            file_size = math.ceil(file_size)
            print(file_size)

            #date of modified into folder
            dt_timestamp = dt.datetime.fromtimestamp(filename.stat()[9])
            date_added_to_folder = dt.datetime.strftime(dt_timestamp, "%a %b %d %H:%M:%S %Y")
            




