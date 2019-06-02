import subprocess
import glob
import os

from config import CAPTURES_DIR

CAPTURE_SHELL_COMMAND = 'ffmpeg -f video4linux2 -i {} -ss 0:0:1 -frames 1 -strftime 1 "{}/%Y-%m-%d-%H-%M-%S_capture.jpg"'

RECORD_SHELL_COMMAND = "ffmpeg -f video4linux2 -i {} -s 640x480 -r 15 -vcodec h264 -codec copy -an http://{}:{}/camera.ffm"

class Camera:

    def __init__(self, camera_device):
        self.m_camera = camera_device

    def capture(self):
        subprocess.run(CAPTURE_SHELL_COMMAND.format(m_camera, CAPTURES_DIR), shell=True)
        return self.last_capture()

    def start_record(self):
        subprocess.run(CAPTURE_SHELL_COMMAND.format(m_camera, CAPTURES_DIR), shell=True)

    def start_streaming(self):
        subprocess.run(CAPTURE_SHELL_COMMAND.format(m_camera, CAPTURES_DIR), shell=True)

    def last_capture(self):
        list_of_files = glob.glob('%s/*.jpg' % CAPTURES_DIR)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
