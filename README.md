# Project-Hybrid Cloud

This project involves the integration of AWS services, OpenFaaS, Ceph, and other tools to perform cloud-based video processing and data analysis. The primary goal is to develop a system that can handle automated video analysis tasks, such as face recognition, using serverless functions and distributed storage.

## Team Members

1. **Shikhar Gupta**: Installed and configured ubuntu 22.04 virtual machine on Oracle virtualbox on a windows machine and configured Ceph on the same.
2. **Maitry Ronakbhai Trivedi**: Worked on building the docker file required for the openfaas function and deployed the same.
3. **Ayushi Agarwal**:  Worked on setting up Openfaas for deployment and configuring Openfaas on Minikube.


## Project Components

#### check.py

This script checks the correctness of the video processing workflow. It verifies the results obtained from the face recognition function by comparing them with predefined mappings. The mappings are specified in the mapping file.

#### face-recognition.yml

This YAML file defines the OpenFaaS function for face recognition. It specifies the Docker image and dependencies required for the serverless function.

#### notification.py

The notification script monitors the input bucket and triggers the face recognition function when new objects are uploaded. It uses a simple HTTP listener to invoke the OpenFaaS function.

#### student_data.json

A JSON file containing sample student data. This data is used for populating a DynamoDB table in the `upload_data.py` script.

#### upload_data.py

This script uploads student data to a DynamoDB table. It reads data from the `student_data.json` file and uses the AWS SDK for Python (Boto3) to interact with DynamoDB.

#### workload.py

The workload script generates a test case by uploading video files to the input bucket. It prepares the system for testing the video processing workflow.

#### Dockerfile

A multi-stage build for an OpenFaaS function with Python runtime. The final runtime image includes the required dependencies, such as ffmpeg, and copies the function code, dependencies, and handler script. The CMD instruction specifies the default command to execute when the container starts, pointing to the handler function for the OpenFaaS function.

#### handler.py

Python script containing the OpenFaas function logic for face recognition.

#### .env

Contain environment variable settings for AWS and Ceph configurations.

## Getting Started

1. **Setup Environment:**
   Ensure that you have the necessary environment variables set, including AWS and Ceph credentials.

2. **Install Dependencies:**
   Install the required Python packages using `pip install -r requirements.txt`.

3. **Run the Workload Script:**
   Execute `workload.py` to simulate a workload by uploading test videos to the input bucket.

4. **Triggers notification:**
   Execute `notification.py` to trigger the openfaas function.