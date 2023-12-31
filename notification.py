import os
import time
import json
import requests
import boto3

from datetime import datetime, timezone
from dotenv import dotenv_values

input_bucket = "cloudspades-input-bucket"
output_bucket = "cloudspades-output-bucket"
CONFIG = dotenv_values()


def main():
    found_objects_list = []
    http_listener_url = "http://127.0.0.1:8080/async-function/face-recognition"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = ""
    s3 = boto3.client('s3',
                      aws_secret_access_key=CONFIG.get('CEPH_SECRET_ACCESS_KEY'),
                      aws_access_key_id=CONFIG.get('CEPH_ACCESS_KEY_ID'),
                      endpoint_url=CONFIG.get('CEPH_ENDPOINT_URL'))
    while True:
        response = s3.list_objects_v2(Bucket=input_bucket)
        if 'Contents' in response:
            for item in response['Contents']:
                key = item["Key"] + item['LastModified'].strftime("%Y-%m-%d %H:%M:%S %Z")
                if key not in found_objects_list:
                    print("%s uploaded. Notification triggered!" % item['Key'])
                    data = "%s %s %s %s" % (item['Key'], CONFIG.get('CEPH_SECRET_ACCESS_KEY'), CONFIG.get('CEPH_ACCESS_KEY_ID'), CONFIG.get('CEPH_ENDPOINT_URL'))
                    requests.post(http_listener_url, verify=False, data=data)
                    found_objects_list.append(key)

        else:
            print("Nothing found")
            time.sleep(5)


if __name__ == '__main__':
    main()
