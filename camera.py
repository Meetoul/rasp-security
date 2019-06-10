import subprocess
import glob
import os

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor as Pool

from logger import LOGI
from config import CAPTURES_DIR, RECORDS_DIR, STREAM_PORT, RECORD_DURATION

CAPTURE_SHELL_COMMAND = 'ffmpeg -f video4linux2 \
 -loglevel quiet \
 -i {} \
 -ss 0:0:1 \
 -frames 1 \
 {}'

RECORD_SHELL_COMMAND = 'ffmpeg -f video4linux2 -i {0}  -s 640x480 -r 15 \
 -vcodec h264 \
 -codec copy \
 -an \
 -t {1} \
 http://0.0.0.0:{2}/camera.ffm \
 -vcodec h264 \
 -an \
 -t {1} \
 {3}'

class Camera:

    def __init__(self, camera_device):
        self.m_camera = camera_device
        self.m_stream_started = False
        self.m_pool = Pool(max_workers=1)

    def capture(self):
        capture_filename = os.path.join(CAPTURES_DIR, self.__gen_timestamp_filename('capture.jpg'))
        subprocess.run(CAPTURE_SHELL_COMMAND.format(self.m_camera, capture_filename), shell=True)
        return self.last_capture()

    def start_stream(self):
        if not self.m_stream_started:
            self.m_stream_started = True
            self.m_future = self.m_pool.submit(self.__start_stream_subprocess)
            self.m_future.add_done_callback(self.__on_stream_finished)

    def __start_stream_subprocess(self):
        LOGI('Camera stream started')
        record_filename = os.path.join(RECORDS_DIR, self.__gen_timestamp_filename('record.mpeg'))
        LOGI('Saving camera record to file %s' % record_filename)
        subprocess.run(RECORD_SHELL_COMMAND.format(self.m_camera, RECORD_DURATION, STREAM_PORT, record_filename), shell=True)

    def __on_stream_finished(self, _):
        LOGI('Camera stream finished')
        self.m_stream_started = False

    def __gen_timestamp_filename(self, filename):
        return datetime.now().strftime("%Y%m%d-%H%M%S") + '-' + filename

    def last_capture(self):
        list_of_files = glob.glob('%s/*.jpg' % CAPTURES_DIR)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
