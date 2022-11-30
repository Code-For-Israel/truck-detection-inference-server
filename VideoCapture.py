import cv2
import requests
import threading
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Netivei Israel - Live cameras
cameras_url = 'https://www.iroads.co.il/%D7%AA%D7%99%D7%A7%D7%99%D7%99%D7%AA-%D7%9E%D7%A6%D7%9C%D7%9E%D7%95%D7%AA/'

# HTTP status codes
status_codes = {200: 'OK', 403: 'Forbidden'}

# Camera's fps:
FPS = 1 / 60


# bufferless VideoCapture
class VideoCapture:
    """
    Class VideoCapture.
    Connecting to a camera's url and reading frames constantly on a thread.
    """

    def __init__(self, cam):
        """
        :param: cam: the camera's key.
        :return: a VideoCapture instance.
        """
        # self.initiate_access_to_camera(cam)  # Check for camera's accessibility.
        self.cap = cv2.VideoCapture(cam['URL'])  # Camera's URL (m3u8).
        self.frame = None

        # start the thread.
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    def initiate_access_to_camera(self, cam):
        """
        Initiate access to camera for reading in case the camera is not accessible.
        :param: cam: the camera's key.
        """
        # Check camera url status
        status = status_codes[requests.get(cam['URL']).status_code]
        print('Access to camera ' + cam['ID'] + ': ' + status)

        # if status is not OK (Forbidden), initiate access to camera.
        if status != 'OK':
            print('Initiate access to camera')
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")

            # start headless webdriver session with Chrome. Get the iroads - live cameras page.
            driver = webdriver.Chrome(options=options)
            driver.get(cameras_url)

            wait = WebDriverWait(driver, 10)
            action = ActionChains(driver)

            # Perform Search of camera's name in the search box.
            searchTextbox = wait.until(EC.presence_of_element_located((By.XPATH, '(//input[@class="searchInput"])')))
            action_chain = action.move_to_element(searchTextbox).click()
            action_chain.send_keys(cam['NAME']).perform()

            # Check for camera url status until OK
            while status_codes[requests.get(cam['URL']).status_code] != 'OK':
                time.sleep(0.1)
                print('.')

            status = status_codes[requests.get(cam['URL']).status_code]
            print('Access to camera ' + cam['ID'] + ': ' + status)

            driver.close()

    def _reader(self):
        """
        Reading frames as soon as they are available in a rate of FPS.
        """
        while True:
            time.sleep(FPS)
            ret, frame = self.cap.read()
            if not ret:
                print('check camera url')
                break
            # print('Read a new frame')
            self.frame = frame

    def read(self):
        """
        Reading frames as soon as they are available in a rate of FPS.
        :return: current frame.
        """
        return self.frame
