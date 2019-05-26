import subprocess
import glob
import os

from config import CAPTURES_DIR, CAMERA_DEVICE

CAPTURE_SHELL_COMMAND = 'ffmpeg -f video4linux2 -i {} -ss 0:0:1 -frames 1 -strftime 1 "{}/%Y-%m-%d-%H-%M-%S_capture.jpg"'

class Camera:

    def capture(self):
        subprocess.run(CAPTURE_SHELL_COMMAND.format(CAMERA_DEVICE, CAPTURES_DIR), shell=True)
        return self.last_capture()

    def last_capture(self):
        list_of_files = glob.glob('%s/*.jpg' % CAPTURES_DIR)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
