from path import path
import time
import os.path
import os


def housekeeping(dir_path, user):
    # Change the DAYS to your liking
    removed = 0
    dir = path(dir_path)
    # Replace DIRECTORY with your required directory
    time_in_secs = time.time() - (1)

    for i in dir.walk():
        if i.isfile():
            if i.mtime <= time_in_secs:
                i.remove()
                removed += 1
