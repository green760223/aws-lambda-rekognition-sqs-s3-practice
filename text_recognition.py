import boto3

# Create clients for S3, SQS and Rekognition
sqs = boto3.client('sqs')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# Get the queue information from SQS
sqs_response = sqs.create_queue(QueueName='my-sqs-2-queue.fifo', Attributes={'FifoQueue': 'true',
                                                                             'ContentBasedDeduplication': 'true'})
queue_url = sqs_response['QueueUrl']

# Receive the messages from SQS
response = sqs.receive_message(QueueUrl=queue_url,
                               MaxNumberOfMessages=10,
                               WaitTimeSeconds=10)


# Processing the SQS messages
if 'Messages' in response:
    result = response['Messages']
    detected_text = "*********** TEXT DETECTION STARTS ***********\n"

    for msg in result:
        # Set up the S3 object key, receipt handle and path that file located with
        receipt_handle = msg['ReceiptHandle']
        body = msg['Body']
        file_path = "/home/ec2-user/images/{}"

        # Delete a finished message in the SQS queue
        sqs.delete_message(QueueUrl=queue_url,
                           ReceiptHandle=receipt_handle)

        # Handle SQS messages one by one if SQS message is not '-1'
        if body != '-1':
            file_name = file_path.format(body)
            # Download car image from S3 by the index of image from SQS
            s3.download_file('cs642mys3bucket', body, file_name)

            # Text detection from image begin
            with open(file_name, 'rb') as image:
                image_bytes = bytearray(image.read())

            txt = rekognition.detect_text(Image={'Bytes': image_bytes})
            detected_text = detected_text + body + '\n'

            # Add detected texts from each image
            for res in txt['TextDetections']:
                if res['Type'] == 'LINE' or res['Type'] == 'WORD':
                    detected_text = ' ' + detected_text + res['DetectedText'] + '\n'
            detected_text = detected_text + '\n'

        else:
            # Text detection completed
            detected_text = detected_text + \
                            "*********** TEXT DETECTION ENDED ***********\n"

            # Generate a file that both index of car and detected text in a text file
            with open("output.txt", 'w') as file:
                file.write(detected_text.strip())
