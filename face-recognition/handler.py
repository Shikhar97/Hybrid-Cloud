import sys

import boto3
import os
import face_recognition
import pickle
from boto3.dynamodb.conditions import Attr
import pandas as pd
from dotenv import dotenv_values
import json

INPUT_BUCKET = "cloudspades-input-bucket"
OUTPUT_BUCKET = "cloudspades-output-bucket"
ENCODING_FILE_KEY = "encoding"
TABLE = "student_table"
CONFIG = dotenv_values()

CEPH_SECRET_ACCESS_KEY = sys.argv[2]
CEPH_ACCESS_KEY_ID = sys.argv[3]
CEPH_ENDPOINT_URL = sys.argv[4]

s3_client = boto3.client('s3',
                         aws_secret_access_key=CEPH_SECRET_ACCESS_KEY,
                         aws_access_key_id=CEPH_ACCESS_KEY_ID,
                         endpoint_url=CEPH_ENDPOINT_URL)
dynamo_client = boto3.resource('dynamodb', aws_secret_access_key=CONFIG.get('AWS_SECRET_ACCESS_KEY'),
                               aws_access_key_id=CONFIG.get('AWS_ACCESS_KEY_ID'),
                               region_name=CONFIG.get('AWS_DEFAULT_REGION'))


# Function to query dynamo db and get academic information in JSON format
def get_info_from_dynamo(query):  # takes a query parameter
    table = dynamo_client.Table(TABLE)
    response = {}
    try:
        response = table.scan(FilterExpression=Attr('name').eq(
            query))  # scans the table where the 'name' attribute is equal to the provided query
    except Exception as e:
        print("DynamoDB query failed ", e)
    if response == {}:
        return response
    return response['Items'][0]


# Function to form a CSV file and upload it to s3 output bucket
def create_csv_file(student_info, file_name):
    print("Info:")
    print(student_info)
    try:
        student_data = {key: [value] for key, value in student_info.items() if
                        key in ['name', 'major', 'year']}
        dataframe = pd.DataFrame(student_data)
        dataframe = dataframe[['name', 'major', 'year']]
        dataframe = dataframe.reset_index(drop=True)
        dataframe.to_csv(file_name, index=False)
    except Exception as e:
        print('Cannot read student information from the table ', e)


# Function to remove the file extension '.mp4' from the file name
def strip_file_name(filename):
    stripped_name = filename.rsplit('.', 1)
    return stripped_name[0]


# Function to upload the csv file generated above to s3
def upload_to_s3(upload_path, key):
    s3 = boto3.resource('s3',
                        aws_secret_access_key=CEPH_SECRET_ACCESS_KEY,
                        aws_access_key_id=CEPH_ACCESS_KEY_ID,
                        endpoint_url=CEPH_ENDPOINT_URL)
    bucket = s3.Bucket(OUTPUT_BUCKET)

    bucket.upload_file(Filename=upload_path,
                       Key=key)


# Function to read the 'encoding' file
def open_encoding(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data


# Function to extract frames from the video
# input_file_path: The path to the input video file.
# upload_path: The path where the extracted frames will be stored.
def extract_frames_from_video(input_file_path):
    try:
        # extract frames from the input video and save them as JPEG images in the output directory
        os.system("/usr/bin/ffmpeg -i " + str(input_file_path) + " -r 1 /tmp/image-%3d.jpeg")
    except Exception as e:
        print('Frame extraction failed ', e)


# Function to match the query image with the encodings, and perform face recognition on the query image
def recognize_face(frame, encodings):
    encoding_from_frame = face_recognition.face_encodings(frame)[0]
    for idx, encoding in enumerate(encodings['encoding']):
        result = face_recognition.compare_faces([encoding], encoding_from_frame)
        if result[0]:
            name = encodings['name'][idx]
            print(f"Name identified from the frame for {name}")
            return name
    return None


def get_first_frame():
    for file in os.listdir("/tmp"):
        if ".jpeg" in file:
            frame = face_recognition.load_image_file("/tmp/{}".format(file))
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                print(f"First frame with a face found in {file}")
                return frame


# OpenFaas function handler
def handle(video_name):
    print(video_name)
    encoding = open_encoding(ENCODING_FILE_KEY)

    video_path = '/tmp/' + video_name
    try:
        s3_client.download_file(INPUT_BUCKET, video_name, video_path)
    except Exception as e:
        print(e)
        raise e
    print(f"{video_name} downloaded from S3 into {video_path}")

    extract_frames_from_video(video_path)
    print(f"Frames extracted from {video_path}")

    first_frame = get_first_frame()
    subject_name = recognize_face(first_frame, encoding)
    student_info = get_info_from_dynamo(subject_name)

    video_name = strip_file_name(video_name)
    output_file_name = "/tmp/{}".format(video_name)
    create_csv_file(student_info, output_file_name)
    upload_to_s3(output_file_name, video_name)
    print(f"Student information of {student_info['name']} stored in output bucket for {video_name}")

    return json.dumps({
        'message': "Done!"
    })


if __name__ == '__main__':
    handle(sys.argv[1])
