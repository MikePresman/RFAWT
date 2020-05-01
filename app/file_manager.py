import os
import datetime as dt
import math
import pprint

def walk_root_folder(directory):
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

            directory_info[dirname].append([file_path, filename, file_size, date_added_to_folder, viewable_file_type(filename)])

    
    '''
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(directory_info)
    '''
    return directory_info
    
def viewable_file_type(filename) -> tuple:
    file_extension = os.path.splitext(filename)[1]
    acceptable_video_file_types = [".mp3", ".mp4", ".webm", ".avi", ".mpg", ".flv", ".mpeg"]
    acceptable_photo_file_types = [".jpg", ".jpeg", ".png", ".tiff", ".gif", ".pdf"]

    if file_extension in acceptable_photo_file_types:
        return(True, "photo", file_extension[1:], filename) #stripping the . from .jpg
    elif file_extension in acceptable_video_file_types:
        return(True, "video", file_extension[1:], filename)
    else:
        return(False, file_extension)






       
                
                

            


  





