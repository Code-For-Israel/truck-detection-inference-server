"""
Configuration file for the Waste Reduction project
"""

import json

filepath = ''

# How to get video url:
# https://stackoverflow.com/questions/42901942/how-do-we-download-a-blob-url-video/49835269#49835269

# load cameras from json file
try:
    with open(filepath + 'cameras.json', encoding="utf8") as f:
        file = json.load(f)

    # Closing json file
    f.close()

    # Number of camera
    cameras = file['CAMERAS']

    found_cameras_json_file = True
    print('cameras json file was found')

except:
    # Cameras dictionary
    CAMERAS = {
        "AYALON_HASHALOM_CAM":
            {
                "ID": "0006",
                "NAME": "איילון השלום תל אביב",
                "URL": "https://5e0da72d486c5.streamlock.net:8443/ayalon/HaShalom.stream/chunklist_w2135066546.m3u8"
            }
    }

    # Number of camera
    cameras = CAMERAS

    found_cameras_json_file = False
    print('cameras json file was not found. Taking default instead')

# read credentials from json file
try:
    with open(filepath + 'credentials.json') as f:
        file = json.load(f)

    # Closing json file
    f.close()

    # Access key to AWS. Write here your aws credentials
    AWS_ACCESS_KEY_ID = file['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = file['AWS_SECRET_ACCESS_KEY']

    # S3 bucket name. Write here your s3 bucket name
    BUCKET = file['BUCKET']

    found_credentials_json_file = True
    print('credentials json file was found')
except:
    # Access key to AWS. Write here your aws credentials
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None

    # S3 bucket name. Write here your s3 bucket name
    BUCKET = None

    found_credentials_json_file = False
    print('credentials json file was not found. Taking default instead')

# load config variables from json file
try:
    with open(filepath + 'config.json', encoding="utf8") as f:
        config = json.load(f)

    # Closing json file
    f.close()

    INPUT_FOLDER = config['INPUT_FOLDER']
    OUTPUT_FOLDER = config['OUTPUT_FOLDER']
    CONF_THRES = config['CONF_THRES']
    MAX_SERIAL_NUM = config['MAX_SERIAL_NUM']
    MAX_SERIAL_NUM = config['MAX_SERIAL_NUM']
    CLASS_NAME = config['CLASS_NAME']
    BACKEND_URL = config['BACKEND_URL']
    POST_INFERENCE_INTERVAL_SECONDS = config['POST_INFERENCE_INTERVAL_SECONDS']
    UPLOAD_LOCAL_DATA_INTERVAL_DAYS = config['UPLOAD_LOCAL_DATA_INTERVAL_DAYS']
    UPLOAD_LOG_FILE_INTERVAL_MINUTES = config['UPLOAD_LOG_FILE_INTERVAL_MINUTES']
    CLEAN_LOCAL_DATA_INTERVAL_DAYS = config['CLEAN_LOCAL_DATA_INTERVAL_DAYS']

    FETCH_DATA_FROM_S3_BUCKET = True if config['FETCH_DATA_FROM_S3_BUCKET'] == 'True' else False
    ENABLE_GET_UI_HOMEPAGE = True if config['ENABLE_GET_UI_HOMEPAGE'] == 'True' else False
    ENABLE_GET_DETECT_TRUCKS = True if config['ENABLE_GET_DETECT_TRUCKS'] == 'True' else False
    UPLOAD_OUTPUT_FOR_EVERY_INFERENCE = True if config['UPLOAD_OUTPUT_FOR_EVERY_INFERENCE'] == 'True' else False
    UPLOAD_OUTPUT_ONLY_UPON_DETECTION = True if config['UPLOAD_OUTPUT_ONLY_UPON_DETECTION'] == 'True' else False
    POST_TO_BACKEND = True if config['POST_TO_BACKEND'] == 'True' else False
    POST_TO_BACKEND_ONLY_UPON_DETECTION = True if config['POST_TO_BACKEND_ONLY_UPON_DETECTION'] == 'True' else False
    ENABLE_GET_SEND_CAMERA_LIST = True if config['ENABLE_GET_SEND_CAMERA_LIST'] == 'True' else False
    ENABLE_GET_SEND_LOCAL_DATA_LIST = True if config['ENABLE_GET_SEND_LOCAL_DATA_LIST'] == 'True' else False
    ENABLE_GET_UPLOAD_LOCAL_DATA_TO_S3 = True if config['ENABLE_GET_UPLOAD_LOCAL_DATA_TO_S3'] == 'True' else False
    ENABLE_UPLOAD_LOG_FILE_TO_S3 = True if config['ENABLE_UPLOAD_LOG_FILE_TO_S3'] == 'True' else False
    ENABLE_GET_DELETE_LOCAL_DATA = True if config['ENABLE_GET_DELETE_LOCAL_DATA'] == 'True' else False

    found_config_json_file = True
    print('config json file was found')

except:
    # Path to input data folder
    INPUT_FOLDER = 'input_data'

    # Path to output data folder
    OUTPUT_FOLDER = 'output_data'

    # Truck classes
    CLASS_NAME = {'0': 'uncovered', '1': 'covered', '2': 'other'}

    # Fetch data from s3 bucket instead of fetching from camera or from local data
    FETCH_DATA_FROM_S3_BUCKET = False

    # Inference threshold
    CONF_THRES = 0.25

    # Serial max number - 7 digits
    MAX_SERIAL_NUM = 9999999

    # Enable or disable REST API GET to index UI and detect_trucks
    ENABLE_GET_UI_HOMEPAGE = True
    ENABLE_GET_DETECT_TRUCKS = True

    # Enable or disable uploading to s3 bucket
    UPLOAD_OUTPUT_FOR_EVERY_INFERENCE = False
    UPLOAD_OUTPUT_ONLY_UPON_DETECTION = False

    # Backend server's url address to send alerts in a json format
    BACKEND_URL = ''

    # classapscheduler.triggers.interval.IntervalTrigger
    # (weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, end_date=None, timezone=None, jitter=None)

    # This method schedules jobs to be run periodically, on selected intervals.

    # weeks (int) – number of weeks to wait
    # days (int) – number of days to wait
    # hours (int) – number of hours to wait
    # minutes (int) – number of minutes to wait
    # seconds (int) – number of seconds to wait
    # start_date (datetime|str) – starting point for the interval calculation
    # end_date (datetime|str) – latest possible date/time to trigger on
    # timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
    # jitter (int|None) – delay the job execution by jitter seconds at most

    # Interval time in seconds between inference to the backend server
    POST_INFERENCE_INTERVAL_SECONDS = 5

    # Enable or disable REST API POST to backend server
    POST_TO_BACKEND = False
    POST_TO_BACKEND_ONLY_UPON_DETECTION = False

    # Enable or disable REST API GET to camera list and local data list
    ENABLE_GET_SEND_CAMERA_LIST = True
    ENABLE_GET_SEND_LOCAL_DATA_LIST = True

    # Enable or disable REST API GET to upload all local data to s3 bucket
    ENABLE_GET_UPLOAD_LOCAL_DATA_TO_S3 = True

    # Interval time in days between uploading local data
    UPLOAD_LOCAL_DATA_INTERVAL_DAYS = 1

    # Enable or disable scheduler for uploading log file to s3 bucket on intervals
    ENABLE_UPLOAD_LOG_FILE_TO_S3 = False

    # Interval time in minutes between uploading local log file
    UPLOAD_LOG_FILE_INTERVAL_MINUTES = 5

    # Enable or disable REST API GET to delete all local data
    ENABLE_GET_DELETE_LOCAL_DATA = True

    # Interval time in days between cleaning (deleting local data)
    CLEAN_LOCAL_DATA_INTERVAL_DAYS = 2

    found_config_json_file = False
    print('config json file was not found. Taking default instead')
