import os
import datetime as dt
import math

directory = r'C:\LAN_Public'


def walk_root_folder(directory_info = {}, directory =  r'C:\LAN_Public'):
    for dirname, dirnames, filenames in os.walk(directory):
    
        if directory_info.get(dirname) is None:
            directory_info[dirname] = []
        

        #HANDLE FILES FIRST
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            
            #file size in kb
            file_size = os.stat(file_path).st_size
            file_size = int(file_size)/1024
            file_size = math.ceil(file_size)

            #date modified
            dt_timestamp = dt.datetime.fromtimestamp(os.stat(file_path).st_ctime)
            date_added_to_folder = dt.datetime.strftime(dt_timestamp, "%a %b %d %H:%M:%S %Y")

            directory_info[dirname].append(file_path)
            directory_info[dirname].append(filename)
            directory_info[dirname].append(file_size)
            directory_info[dirname].append(date_added_to_folder)
        
        walk_subfolder(directory, directory_info) #pass current directory, so we can continue and traverse folders
    




def walk_subfolder(directory, directory_info):
    for dirname, dirnames, filenames in os.walk(directory):
        for subdir in dirnames:
            folder_path = os.path.join(dirname, subdir)
            if os.path.isdir(folder_path):
                walk_root_folder(directory_info, directory = folder_path)


        
            


  





