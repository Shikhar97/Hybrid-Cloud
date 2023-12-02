import os
import time
import json
import requests
import boto3

from datetime import datetime, timezone
from dotenv import dotenv_values

output_bucket = "cloudspades-output-bucket"
CONFIG = dotenv_values()
found_objects_list = []


def main():
    s3 = boto3.client('s3',
                      aws_secret_access_key=CONFIG.get('CEPH_SECRET_ACCESS_KEY'),
                      aws_access_key_id=CONFIG.get('CEPH_ACCESS_KEY_ID'),
                      endpoint_url=CONFIG.get('CEPH_ENDPOINT_URL'))
    while True:
        response = s3.list_objects_v2(Bucket=output_bucket)
        if 'Contents' in response:
            for item in response['Contents']:
                key = item["Key"] + item['LastModified'].strftime("%Y-%m-%d %H:%M:%S %Z")
                if key not in found_objects_list:
                    print("%s downloaded" % item['Key'])
                    filepath = os.path.join("results", item['Key'])
                    s3.download_file(output_bucket, item['Key'], filepath)
                    found_objects_list.append(key)

        else:
            print("Nothing found")
            time.sleep(5)


if __name__ == '__main__':
    main()
