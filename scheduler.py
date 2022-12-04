"""
This module is a simple wrap for sending a POST request every X seconds to the backend
TODO [YOTAM] this mechanism should be improved !!
"""

import time
import json
import requests

filepath = ''

with open(filepath + 'config.json', encoding="utf8") as f:
    config = json.load(f)

# Closing json file
f.close()
POST_INFERENCE_INTERVAL_SECONDS = config['POST_INFERENCE_INTERVAL_SECONDS']
BACKEND_URL = config['BACKEND_URL']


def call_get_internally_upload_to_s3_and_make_post_request_to_backend():
    pass


while True:
    # Sleep for some fixed time
    time.sleep(POST_INFERENCE_INTERVAL_SECONDS)

    # Get detection_results from object detection model
    detection_results = requests.get(url='http://localhost:5000/detect_trucks')
    detection_results = json.loads(detection_results.text)

    print(detection_results)
    # response = requests.post(BACKEND_URL, json=users_data)
