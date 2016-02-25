from path import path
import time
import os.path


def housekeeping(dir_path):
    """Deletes any temporary files from the file system"""
    removed = 0
    dir = path(dir_path)
    # set how old a file should be in seconds
    time_in_secs = time.time() - (1)
    # iterate each file in the dir
    for i in dir.walk():
        if i.isfile():
            if i.mtime <= time_in_secs:
                i.remove()
                removed += 1
