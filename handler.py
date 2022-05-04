import urllib.parse
import boto3
# import face_recognition
import pickle
import os
from botocore.exceptions import ClientError
# from eval_face_recognition import fn_face_recognition
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from models.inception_resnet_v1 import InceptionResnetV1
from urllib.request import urlopen
from PIL import Image
import json
import numpy as np
import build_custom_model
from dotenv import load_dotenv

load_dotenv()

region = 'us-east-1'
s3 = boto3.client('s3', region_name=region)
sqs = boto3.resource('sqs', region_name=region)
request_queue = sqs.get_queue_by_name(QueueName='project2_queue')

dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('Project2Table')

input_bucket = 'input-project2'
# output_bucket = 'output-project2'

result = ''


# face recognition function
def fn_face_recognition(filename):
    labels_dir = "./checkpoint/labels.json"
    model_path = "./checkpoint/model_vggface2_best.pth"

    # read labels
    with open(labels_dir) as f:
        labels = json.load(f)
    # print(f"labels: {labels}")

    device = torch.device('cpu')
    model = build_custom_model.build_model(len(labels)).to(device)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))['model'])
    model.eval()
    # print(f"Best accuracy of the loaded model: {torch.load(model_path, map_location=torch.device('cpu'))['best_acc']}")

    # img = Image.open(img_path)
    img = Image.open(filename)
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0).to(device)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)
    result = labels[np.array(predicted.cpu())[0]]
    print(result)
    return result


# Function to read the 'encoding' file
def open_encoding(filename):
    file = open(filename, 'rb')
    data = pickle.load(file)
    file.close()
    return data


# Download object from input bucket
def download_object(bucket_name, item, dest):
    try:
        s3.download_file(bucket_name, item, dest)
        print('Ok')
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('The video does not exist: s3://{}/{}'.format(bucket_name, item))
        else:
            raise e
    return True


def face_recognition_handler(event, context):
    # Listening bucket event
    global result
    bucket = event['Records'][0]['s3']['bucket']['name']

    # Getting the item: video name e.g. test_1.mp4
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print('CONTENT TYPE: ' + response['ContentType'])
        print(response['ContentType'])
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as '
            'this function.'.format(
                key,
                bucket))
        raise e

    # Video path
    path = '/tmp/'
    video_file_path = str(path) + key

    # Downloading video
    download_object(bucket, key, video_file_path)

    # Extracting frames from video using ffmpeg
    img_path = f'{str(path)}image-001.png'
    os.system(f'ffmpeg -sseof -1 -i {str(video_file_path)} -update 1 -q:v 1 {img_path}'
    )

    # Using the first image generated, read face_encoding
    # face_image = face_recognition.load_image_file(
    #    str(path) + 'image-001.jpeg')
    # face_encoding = face_recognition.face_encodings(face_image)[0]

    # Read the 'encoding' file
    # encoding_file = '/home/app/encoding'
    # total_face_encoding = open_encoding(encoding_file)

    # For each known face, determine whether the current face matches it,
    # and the matching name is stored in the result
    # for encoding in enumerate(total_face_encoding['encoding']):
    #    match = face_recognition.compare_faces(
    #        [encoding[1]], face_encoding)
    #    if match[0]:
    #        result = total_face_encoding['name'][encoding[0]]
    #        break

    # Using custom face recognition on student face
    result = fn_face_recognition(img_path)
    tempdict = {
        'Qiang': 2,
        'Kiran': 3,
        'Sreshta': 1
    }
    # Query for matching records in dynamodb
    response = table.get_item(Key={'userid': str(tempdict[result])})
    item = response['Item']
    # Uploading result to the SQS
    sqs_message = {"filename": key, "userid": str(int(item["userid"])), "major": item["major"], "name": item["name"],
                   "year": item["year"]}
    sqs_request_response = request_queue.send_message(MessageBody=json.dumps(sqs_message))