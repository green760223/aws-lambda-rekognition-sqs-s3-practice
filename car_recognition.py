import boto3

# Create services of client for S3, SQS, and Rekognition
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
sqs = boto3.client('sqs')

# List S3 bucket name
s3_response = s3.list_buckets()
bucket_name = s3_response['Buckets'][0]['Name']

# List all the images in S3 bucket
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)

# Create a FIFO type of SQS queue and get queue url
sqs_response = sqs.create_queue(QueueName='my-sqs-queue.fifo', Attributes={'FifoQueue': 'true',
                                                                           'ContentBasedDeduplication': 'true'})
queue_url = sqs_response['QueueUrl']

# Get all the images from S3 bucket
for image in bucket.objects.all():

    image_name = image.key

    # Detect car images by rekognition and return the labels that confidence greater than 90%
    detect_result = rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}},
                                              MaxLabels=10,
                                              MinConfidence=90)

    for label_name in detect_result['Labels']:

        # If detected label is Car and Confidence > 90%, send index of image to SQS
        if label_name['Name'] == 'Car':
            # Send index of image that confidence greater than 90% as car to SQS
            msg = sqs.send_message(QueueUrl=queue_url, MessageBody=image_name, MessageGroupId='group-1')

# Send a '-1' index when no image need to be process to SQS as a signal for EC2 B
finish = sqs.send_message(QueueUrl=queue_url, MessageBody="-1", MessageGroupId='group-1')
