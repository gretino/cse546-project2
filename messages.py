import boto3
import time
import datetime as dt
import json
from dotenv import load_dotenv
load_dotenv()


sqs_client = boto3.client("sqs", region_name="us-east-1")

def delete_message(receipt_handle):
    #print(receipt_handle)
    response = sqs_client.delete_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/053622899218/project2_queue",
        ReceiptHandle=receipt_handle,
    )

def receive_message():
	message_body=''
	response = sqs_client.receive_message(
		QueueUrl='https://sqs.us-east-1.amazonaws.com/053622899218/project2_queue',
		MaxNumberOfMessages=1,
		WaitTimeSeconds=2,)
	for message in response.get("Messages", []):
		message_body = message["Body"]
		# delete_message(message["ReceiptHandle"])
	return message_body

print("Receiving SQS messages...")
while True:
	json_data = receive_message()
	if not json_data == '':
		#print(json_data)
		y = json.loads(json_data)
		print(f'The person detected at {y["filename"]}: {y["name"]}, {y["major"]}, {y["year"]}')
		start_time = y["filename"][:-5]
		print(f'start_time: {start_time}, {type(start_time)}')
		time_format = time.strptime(start_time, '%Y-%m-%d_%H.%M.%S.%f')
		millis = float(start_time.split('.')[-1])
		start_timestamp = time.mktime(time_format)+millis
		current_timestamp = time.time()
		print(start_time, start_timestamp, current_timestamp)
		print(f'Latency: {current_timestamp-start_timestamp} seconds.')
		print('\n')
	else:
		print("Empty Queue...")