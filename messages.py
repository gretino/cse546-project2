import boto3
import time
import datetime as dt
import json
from dotenv import load_dotenv

load_dotenv()
i = 0
sqs_client = boto3.client("sqs", region_name="us-east-1")


def delete_message(receipt_handle):
    # print(receipt_handle)
    response = sqs_client.delete_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/250982311839/project2_queue",
        ReceiptHandle=receipt_handle,
    )


def receive_message():
    message_body = ''
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/250982311839/project2_queue',
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1, )
    for message in response.get("Messages", []):
        message_body = message["Body"]
        delete_message(message["ReceiptHandle"])
    return message_body


print("Receiving SQS messages...")
while True:
    json_data = receive_message()
    if not json_data == '':
        # print(json_data)
        i = i + 1
        y = json.loads(json_data)
        print('-------------------------------')
        print(f'The {i} person detected With original provided model: {y["name"]}, {y["major"]}, {y["year"]}')
        try:
            print(f'The {i} person detected With Online model: {y["name-model2"]}, {y["major-model2"]}, {y["year-model2"]}')
        except:
            pass
        print('-------------------------------')
        start_time = y["filename"][:-5]
        # print(f'start_time: {start_time}, {type(start_time)}')
        time_format = time.strptime(start_time, '%Y-%m-%d_%H.%M.%S.%f')
        millis = float(f"0.{start_time.split('.')[-1]}")
        start_timestamp = time.mktime(time_format) + millis
        current_timestamp = time.time()
        # print(start_time, start_timestamp, current_timestamp)
        print(f'Latency: {"{:.2f}".format(current_timestamp - start_timestamp)} seconds.')
    # print('\n')
    else:
        print("Empty Queue...")
