import os
import boto3

from dotenv import dotenv_values

input_bucket = "cloudspades-input-bucket"
output_bucket = "cloudspades-output-bucket"
test_cases = "test_cases/"
CONFIG = dotenv_values()


def clear_input_bucket():
    global input_bucket
    s3 = boto3.client('s3',
                      aws_secret_access_key=CONFIG.get('CEPH_SECRET_ACCESS_KEY'),
                      aws_access_key_id=CONFIG.get('CEPH_ACCESS_KEY_ID'),
                      endpoint_url=CONFIG.get('CEPH_ENDPOINT_URL'))
    list_obj = s3.list_objects_v2(Bucket=input_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=input_bucket, Key=key)
    except:
        print("Nothing to clear in input bucket")


def clear_output_bucket():
    global output_bucket
    s3 = boto3.client('s3',
                      aws_secret_access_key=CONFIG.get('CEPH_SECRET_ACCESS_KEY'),
                      aws_access_key_id=CONFIG.get('CEPH_ACCESS_KEY_ID'),
                      endpoint_url=CONFIG.get('CEPH_ENDPOINT_URL'))
    list_obj = s3.list_objects_v2(Bucket=output_bucket)
    try:
        for item in list_obj["Contents"]:
            key = item["Key"]
            s3.delete_object(Bucket=output_bucket, Key=key)
    except:
        print("Nothing to clear in output bucket")


def upload_to_input_bucket_s3(path, name):
    global input_bucket
    s3 = boto3.resource('s3',
                        aws_secret_access_key=CONFIG.get('CEPH_SECRET_ACCESS_KEY'),
                        aws_access_key_id=CONFIG.get('CEPH_ACCESS_KEY_ID'),
                        endpoint_url=CONFIG.get('CEPH_ENDPOINT_URL'))
    bucket = s3.Bucket(input_bucket)

    bucket.upload_file(Filename=path + name,
                       Key=name)


def upload_files(test_case):
    global input_bucket
    global output_bucket
    global test_cases

    # Directory of test case
    test_dir = test_cases + test_case + "/"

    # Iterate over each video
    # Upload to S3 input bucket
    for filename in os.listdir(test_dir):
        if filename.endswith(".mp4") or filename.endswith(".MP4"):
            print("Uploading to input bucket..  name: " + str(filename))
            upload_to_input_bucket_s3(test_dir, filename)


def workload_generator():
    print("Running Test Case 1")
    upload_files("test_case_1")

    # print("Running Test Case 2")
    # upload_files("test_case_2")


clear_input_bucket()
clear_output_bucket()
workload_generator()
