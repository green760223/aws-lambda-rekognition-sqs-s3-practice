
# Cloud Computing - Programming Assignment 2

This project is aim to develop an application that can use existing AWS services to retrieve images from S3, perform image detection by AWS Rekognition, and establish communication between two EC2 instances via AWS SQS.




## Installation

#### AWS CLI
To run this project, please install the AWS CLI with yum in both AWS EC2 instances.

```bash
sudo yum update -y
sudo yum install -y aws-cli
```
Confirm the AWS CLI if install completed. This should display the version number of the AWS CLI that you just installed.

```bash
aws --version
```

Once completed the AWS CLI installation, setup the default config and credentials for programmatic purpose.
```bash
aws configure
```

You will be prompted to enter the following details:
```bash
AWS Access Key ID
AWS Secret Access Key
Default region name (e.g. us-west-2)
Default output format (e.g. json)
```
You can obtain your access key ID and secret access key from the AWS Management Console by security credentials .


#### AWS SDK for Python
Next, install AWS SDK for Python on both EC2 instances.
```bash
sudo yum install -y python3-pip
pip3 install boto3
```

Once the installation is complete, you can verify that Boto3 is installed by opening a Python shell and running the following command:
```bash
import boto3
```
If there are no errors, then Boto3 is installed and you can start using it to interact with AWS services.

#### Preparation for AWS EC2
Copy the files to the corresponding AWS EC2 instances by same pem key.
```bash
scp -i <path_to_key_pair> car_recognition.py ec2-user@<EC2_A_instance_public_IP>:/home/ec2-user/

scp -i <path_to_key_pair> text_recognition.py ec2-user@<EC2_B_instance_public_IP>:/home/ec2-user/
```

On the EC2 B instance, create an image folder to save the images downloaded from S3 under /home/ec2-user/ path.
```bash
mkdir images
```


## Usage

#### To run this project, please follow these steps:

Run the car_recognition.py in the AWS EC2_A instance.
```
python3 car_recognition.py
```

Then, run the text_recognition.py in the AWS EC2_B instance.
```
python3 text_recognition.py
```

Once "text_recognition.py" run completed, you should be able to see the images downloaded from S3 in the "images" folder, and an "output.txt" file that contains the index of image and the detected text from that image.
## Features

- Download images from a predefined and pre-uploaded S3 bucket.
- Detect images and extract text using AWS Rekognition.
- Communicate between two instances using AWS SQS (FIFO type).
- Automatically generate a file that contains the image index and the detected text in a single file.


## Tech Stack

**Client:** PyCharm IDE and boto3 for AWS SDK.

**Cloud Services:** AWS EC2 instance, AWS SQS, AWS Rekognition, AWS Lambda and AWS S3.





## Authors

This project was created by Yi-Hsuan Chuang.


## License
This project is licensed under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.



