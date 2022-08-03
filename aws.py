import os
import boto3

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return 'https://zoeaws.s3-sa-east-1.amazonaws.com/' + file_name


def download_file(file_name, bucket, pathDownload):

	s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

	s3_client = boto3.client('s3')
	response = s3_client.download_file(bucket, file_name, pathDownload)

	return True
