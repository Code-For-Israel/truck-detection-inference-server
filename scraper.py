import datetime
from VideoCapture import *


class Scraper:
    """
    Class Scraper.
    Reading a frame from a video feed (from VideoCapture class).
    Capturing the frame id which made of the camera's ID, frame serial number, current date and time.
    Saving the frame to a local directory with the frame id .
    """

    def __init__(self, cam, max_count):
        """
        :param: cam: the camera's key.
        :param: max_count: the maximum number of a frame serial number.
        :return: a Scraper instance.
        """
        self.vidcap = VideoCapture(cam)
        self.id = cam['ID']
        self.counter = 0
        self.max_count = max_count
        self.frame_id = None

    def scrape(self, dir_path=''):
        """
        Parsing a frame from a VideoCapture read function and saving it in a folder.
        :param: dir_path: the name of the folder.
        :return: frame_id: in the following format: img dir_path/imgXXXXZZZZZZZ_DD_MM_YYYYTHH_MM_SS.
        Where XXXX is the camera ID, ZZZZZZZ is the frame count and DD_MM_YYYYTHH_MM_SS is the date and the time.
        """
        image = self.vidcap.read()

        current_time = datetime.datetime.now(datetime.timezone.utc)
        day = str(current_time.day) if len(str(current_time.day)) == 2 else '0' + str(current_time.day)
        month = str(current_time.month) if len(str(current_time.month)) == 2 else '0' + str(current_time.month)
        year = str(current_time.year)
        hour = str(current_time.hour) if len(str(current_time.hour)) == 2 else '0' + str(current_time.hour)
        minute = str(current_time.minute) if len(str(current_time.minute)) == 2 else '0' + str(current_time.minute)
        second = str(current_time.second) if len(str(current_time.second)) == 2 else '0' + str(current_time.second)

        self.frame_id = dir_path + '/' + 'img' + self.id + (7 - len(str(self.counter))) * '0' + str(self.counter) \
                        + '_' + day + '_' + month + '_' + year + 'T' + hour + '_' + minute + '_' + second + '.jpg'
        print(self.frame_id)
        cv2.imwrite(self.frame_id, image)

        self.counter += 1
        if self.counter > self.max_count:
            self.reset_counter()

        return self.frame_id

    def reset_counter(self, counter=0):
        """
        Setting/resetting the counter for the serial number of the frame.
        :param: int counter: the counter.
        """
        self.counter = counter
