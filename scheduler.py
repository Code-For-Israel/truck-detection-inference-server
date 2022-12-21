"""
This module is a simple wrap for sending a POST request every X seconds to the backend
TODO [YOTAM] this mechanism should be improved !!
"""

import time
import json
import requests
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

cameras_id_to_name = {camera_data['ID']: camera_data['NAME'] for camera_data in cameras.values()}

s3 = Files(s3_bucket=BUCKET, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def call_get_internally_upload_to_s3_and_make_post_request_to_backend():
    pass


# for initial start up
time.sleep(15)

while True:
    # Sleep for some fixed time
    time.sleep(POST_INFERENCE_INTERVAL_SECONDS)

    # Get detection_results from object detection model
    detection_results = requests.get(url='http://localhost:5000/detect_trucks')
    detection_results = json.loads(detection_results.text)

    # Upload images to S3
    absolute_paths_to_images = [
        os.path.join(SCRIPT_DIR, OUTPUT_FOLDER, image_id + '.jpg')
        for image_id in detection_results['image_id']
    ]

    s3_uris = list()
    for path in absolute_paths_to_images:
        s3.upload_to_s3_from_local(file=path, key=os.path.basename(path))
        s3_uris.append(f's3://{BUCKET}/{os.path.basename(path)}')

    cameras_names = list()
    for image_id in detection_results['image_id']:
        cameras_names.append(cameras_id_to_name[image_id[3:7]])

    detection_results = {
        'object_detection_data': [
            {
                'image_id': detection_results['image_id'][i],
                'camera_name': cameras_names[i],
                'detection_results': detection_results['detection_results'][i],
                's3_uri': s3_uris[i],
            }
            for i in range(len(s3_uris))
        ]
    }

    # TODO Add the call to the backend and make sure it works smoothly
    # response = requests.post(BACKEND_URL, json=json.dumps(detection_results))
