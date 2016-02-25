from path import path
import time
import os.path


def housekeeping(dir_path, user):

    removed = 0
    dir = path(dir_path)
    time_in_secs = time.time() - (1)

    for i in dir.walk():
        if i.isfile():
            if i.mtime <= time_in_secs:
                i.remove()
                removed += 1
