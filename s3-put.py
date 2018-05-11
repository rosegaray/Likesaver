from __future__ import print_function
import boto3
from io import BytesIO
import contextlib
import requests

import os
import sys
import dropbox
import twitterCredentials
import glob

     
s3_client = boto3.client('s3')
     
def save_to_dropbox(image_path, key):
    client = dropbox.Dropbox(twitterCredentials.dbx_token)
    f = open('/tmp/' + str(key), 'rb')
    r = client.files_upload(f.read(), '/' + key)
    if os.path.exists(image_path):
        os.remove(image_path)
        print("Removed the file " + image_path)     
    else:
        print("Sorry, file does not exist: " + image_path)
   
    # with Image.open(image_path) as image:
    #     image.thumbnail(tuple(x / 2 for x in image.size))
    #     image.save(resized_path)
     
def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        key2 = key.replace('/', '')
        #os.mkdir('/tmp/') 
        download_path = '/tmp/{}'.format(key2)
        # upload_path = '/tmp/resized-{}'.format(key)
        
        s3_client.download_file(bucket, key, download_path)
        save_to_dropbox(download_path, key2)
        # delete s3 bucket

        s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )


    #     for record in event['Records']:
    # bucket = record['s3']['bucket']['name']
    # key = record['s3']['object']['key']
    # fn='/tmp/xyz'
    # fp=open(fn,'w')
    # response = s3_client.get_object(Bucket=bucket,Key=key)
    # contents = response['Body'].read()
    # fp.write(contents)
    # fp.close()



#arn:aws:iam::406839700264:role/lambda-s3-execution-role
#increase time out, increase file size limit