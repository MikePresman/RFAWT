import os
import datetime as dt
import math
import pprint

def walk_root_folder(directory =  r'C:\LAN_Public'):
    directory_info = {}
    for dirname, dirnames, filenames in os.walk(directory):
        if directory_info.get(dirname) is None:
            directory_info[dirname] = []

        #file handling
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            
            #file size in kb
            file_size = os.stat(file_path).st_size
            file_size = int(file_size)/1024
            file_size = math.ceil(file_size)

            #date modified
            dt_timestamp = dt.datetime.fromtimestamp(os.stat(file_path).st_ctime)
            date_added_to_folder = dt.datetime.strftime(dt_timestamp, "%a %b %d %H:%M:%S %Y")

            directory_info[dirname].append([file_path, filename, file_size, date_added_to_folder, viewable_file_type(filename) ])

 
    for subdir in dirnames:
        folder_path = os.path.join(dirname, subdir)
        if os.path.isdir(folder_path):
            walk_root_folder(directory_info, directory) #a little bit of recursion magic
    '''
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(directory_info)
    '''
    return directory_info
    


def viewable_file_type(filename) -> bool:
    file_extension = os.path.splitext(filename)[1]
    acceptable_file_types = [".jpg", ".jpeg", ".mp3", ".mp4", ".gif", ".webm", ".avi", ".mpg", ".flv", ".mpeg", ".png", ".tiff"]
    if file_extension in acceptable_file_types:
        return True
    return False
    


       
                
                

            


  





