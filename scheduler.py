"""
This module is a simple wrap for sending a POST request every X seconds to the backend
TODO [YOTAM] this mechanism should be improved !!
"""

import time
import json
import requests
import threading
import os

from files import *

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))

filepath = ''

with open(filepath + 'config.json', encoding="utf8") as f:
    config = json.load(f)

# Closing json file
f.close()
POST_INFERENCE_INTERVAL_SECONDS = config['POST_INFERENCE_INTERVAL_SECONDS']
BACKEND_URL = config['BACKEND_URL']
OUTPUT_FOLDER = config['OUTPUT_FOLDER']
POST_TO_BACKEND_ONLY_UPON_DETECTION = True if config['POST_TO_BACKEND_ONLY_UPON_DETECTION'] == 'True' else False

with open(filepath + 'credentials.json') as f:
    file = json.load(f)

# Closing json file
f.close()

# Access key to AWS. Write here your aws credentials
AWS_ACCESS_KEY_ID = file['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = file['AWS_SECRET_ACCESS_KEY']

# S3 bucket name. Write here your s3 bucket name
BUCKET = file['BUCKET']

# Cameras json
with open(filepath + 'cameras.json', encoding="utf8") as f:
    file = json.load(f)

# Closing json file
f.close()

# Number of camera
cameras = file['CAMERAS']

# Cameras names in English
cameras_id_to_name_en = {cameras[camera_name]['ID']: camera_name[:-4].split('_') for camera_name in cameras.keys()}
for key, value in cameras_id_to_name_en.items():
    cameras_id_to_name_en[key] = ' '.join([word.capitalize() for word in value])

# Cameras names in Hebrew
cameras_id_to_name_he = {camera_data['ID']: camera_data['NAME'] for camera_data in cameras.values()}

# Coordinates
latitude = {camera_data['ID']: camera_data['LATITUDE'] for camera_data in cameras.values()}
longitude = {camera_data['ID']: camera_data['LONGITUDE'] for camera_data in cameras.values()}

s3 = Files(s3_bucket=BUCKET, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# for initial start up
time.sleep(15)

while True:
    # Sleep for some fixed time
    time.sleep(POST_INFERENCE_INTERVAL_SECONDS)

    # Get detection_results from object detection model
    detection_results = requests.get(url='http://localhost:5000/detect_trucks')
    detection_results = json.loads(detection_results.text)

    # List absolute paths to images only upon detection or not
    if POST_TO_BACKEND_ONLY_UPON_DETECTION:
        absolute_paths_to_images = [
            None if detections == 'no_detections' else
            os.path.join(SCRIPT_DIR, OUTPUT_FOLDER, image_id + '.jpg')
            for image_id, detections in zip(detection_results['image_id'], detection_results['detection_results'])
        ]
    else:
        absolute_paths_to_images = [
            os.path.join(SCRIPT_DIR, OUTPUT_FOLDER, image_id + '.jpg')
            for image_id in detection_results['image_id']
        ]

    # Upload images to S3 with threads
    threads = list()
    s3_uris = list()
    for path in absolute_paths_to_images:
        if path is not None:
            threads.append(threading.Thread(target=s3.upload_to_s3_from_local, args=(path, os.path.basename(path), )))
            # s3.upload_to_s3_from_local(file=path, key=os.path.basename(path))
            s3_uris.append(f's3://{BUCKET}/{os.path.basename(path)}')
        else:
            s3_uris.append('no_upload')

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        thread.join()

    # List of cameras names in English
    cameras_names_en = list()
    for image_id in detection_results['image_id']:
        cameras_names_en.append(cameras_id_to_name_en[image_id[3:7]])

    # List of cameras names in Hebrew
    cameras_names_he = list()
    for image_id in detection_results['image_id']:
        cameras_names_he.append(cameras_id_to_name_he[image_id[3:7]])

    # List of coordinates
    coordinates = list()
    for image_id in detection_results['image_id']:
        coordinates.append({"latitude": latitude[image_id[3:7]], "longitude": longitude[image_id[3:7]]})

    # Detection results dictionary
    detection_results = {
        'object_detection_data': [
            {
                'image_id': detection_results['image_id'][i],
                'camera_name': {'en': cameras_names_en[i], 'he': cameras_names_he[i]},
                'coordinates': coordinates[i],
                'detection_results': detection_results['detection_results'][i],
                's3_uri': s3_uris[i],
            }
            for i in range(len(s3_uris))
        ]
    }

    # Post request to backend server
    try:
        response = requests.post(BACKEND_URL, json=json.dumps(detection_results))
    except:
        print(f'Post request failed. Trying again')
        continue
    print(f'response from backend (sending detection_results): {response}')
