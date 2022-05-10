import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadedFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Loop through each file in our download folder
        for filename in os.listdir(download_folder):
            # This checks to make sure that if the destination path is nested inside
            # the download path, it does not attempt to move the folder
            if filename == destination_path.split('/')[-1]:
                continue

            # Find each files type
            file_type = filename[-4:].lower()

            # Loop through our file_types object and determine the destination folder
            # This defaults to 'other'
            file_key = 'other'
            for key, value in file_types.items():
                if file_type in value:
                    file_key = key
                    break
            
            # Here we set our source path for the file to be moved and our destination
            # path that the file will be moved to
            src = download_folder + "/" + filename
            destination = destination_path + file_key + "/" + filename

            # This executed the file change
            os.rename(src, destination)

# Set our file_types dictionary. This can be modified as needed.
file_types = {
    'images': {'.jpg', 'jpeg', '.gif', '.png', 'tiff', '.tif', '.bmp', '.eps', '.raw'},
    'videos': {'.mp4', '.avi', '.mov', '.wmv', '.mkv', 'webm'},
    'documents': {'.pdf', '.txt', 'docx'},
    'installers': {'.exe', '.msi'},
    'compressed': {'.rar', '.zip'}
}

# Set these to your download folder and the folder you wish all the subfolders to be
# stored
# You will need to create subfolders for each file type within your destination folder
# You will also need a folder 'other' for all file types that do not fit in the categories
download_folder = "### SET YOUR DOWNLOAD FOLDER PATH HERE ###"
destination_path = "### SET YOUR DESTINATION FOLDER PATH HERE ###"

# Instantiate our classes and set some parameters
event_handler = DownloadedFileHandler()
observer = Observer()
observer.schedule(event_handler, download_folder, recursive=True)

# Execute our folder observer
observer.start()

# This is set to run unless timing out, or stopped by CTRL + C in the terminal
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()