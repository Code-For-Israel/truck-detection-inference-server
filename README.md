# Inference server for truck detection 

![Traucker](/assets/images/traucker.png "Traucker")

Inference server for truck detection ([waste reduction project](https://www.codeforisrael.org/project/%D7%94%D7%A9%D7%9C%D7%9B%D7%AA-%D7%A4%D7%A1%D7%95%D7%9C%D7%AA-%D7%9C%D7%90-%D7%97%D7%95%D7%A7%D7%99%D7%AA-%D7%91%D7%A0%D7%92%D7%91)) at [Code for Israel](https://www.codeforisrael.org/)

**Inference Server**
* Build and deploy a Flask app using Docker.
* Development framework: PyCharm
* Three json files:
  * cameras.json
  * credentials.json
  * config.json

**Python Classes**
* Config - All configuration variables, extracted from the three json files, needed for the inference server (Cameras’ urls, AWS credentials, directories names, etc...).
* VideoCapture
  * Initiate access to camera - Start the connection to camera (GET 200 response code instead of 403) by using Selenium.
  * Read frames - Reading frames from camera, on a thread, by a given frame rate.
* Scraper - Saving a frame with image name format (camera’s ID, serial number, date and time) into a local input folder.
* Model - Using the model’s weights to infer images. Saving output images and labels (of exist) into a local output folder.
* Files
  * A logger instance for alerts logging and other metadata logging.
  * Creating input and output folders.
  * Deleting local folders and images.
  * Uploading and downloading files from a s3 bucket.

**Automatic scheduler**
 * sends output, in json format, to the backend server every x=0.5 seconds (x can be over 0.2 seconds).
 * Uploads every 5 minutes the log file to s3 bucket.


Inference time on local server:
Scraping and saving a frame: 1 - 14 ms
Inferring and saving outputs (images + labels): 180-190 ms
Total time: around 200 ms (0.2 seconds).

![Truck detection](/assets/images/classes.png "Truck detection")
