import json
import boto3

# Create clients for S3, SQS and Rekognition
sqs = boto3.client('sqs')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# Get the queue information from SQS-2
sqs2_response = sqs.create_queue(QueueName='my-sqs-2-queue.fifo', Attributes={'FifoQueue': 'true',
                                                                              'ContentBasedDeduplication': 'true'})
sqs2_queue_url = sqs2_response['QueueUrl']

# List S3 bucket name
s3_response = s3.list_buckets()
bucket_name = s3_response['Buckets'][0]['Name']


def lambda_handler(event, context):
    # TODO implement
    records = event['Records']

    # Process the messages (index of image) from the SQS-1
    for record in records:
        image_name = record['body']

        if image_name != '-1':
            # Detect images with people by rekognition and return the labels that confidence greater than 90%
            detect_result = rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}},
                                                      MaxLabels=10,
                                                      MinConfidence=90)

            for label_name in detect_result['Labels']:
                if label_name['Name'] == 'Person':
                    print("Image with Person and Car:", image_name)
                    # Send the processed messages to the SQS-2
                    sqs.send_message(QueueUrl=sqs2_queue_url, MessageBody=image_name, MessageGroupId='group-1')

        else:
            print("No more pictures need to handle!")
            sqs.send_message(QueueUrl=sqs2_queue_url, MessageBody='-1', MessageGroupId='group-1')

    return {
        'statusCode': 200,
        'body': json.dumps('The SQS-1 Lambda service has successfully sent messages to SQS-2!')
    }
