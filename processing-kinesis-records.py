from __future__ import print_function

import base64
import codecs
import json
import boto3
from io import BytesIO
import contextlib
from botocore.vendored import requests

#process events - look for media urls, upload these urls to s3 as files, 
#then, download s3 file and upload to dropbox, delete the object, delete the file

def lambda_handler(event, context):
	for record in event['Records']:
		#Kinesis data is base64 encoded so decode here
		payload=base64.b64decode(record['kinesis']['data'])
		payload=payload.replace(b'"', b'')
		payload.decode('utf-8')
		upload(payload)
		
		
			
			
			#save the media_url and upload to dropbox
			


# role arn: arn:aws:iam::406839700264:role/lambda-kinesis-execution-role
#bytes(s, 'utf-8').decode("unicode_escape")

def upload(url):
# Get the service client
	s3 = boto3.client('s3')
	print("url")
	url = url.decode('utf-8')

# Rember to set stream = True.
	with contextlib.closing(requests.get(url, stream=True, verify=False)) as response:
		# Set up file stream from response content.
		fp = BytesIO(response.content)
		# Upload data to S3
		print("Y")
		#File obj, bucket, key, extra_args, 
		s3.upload_fileobj(fp, 'cmsc389l-rgaray', 'test/' + url.split('/')[-1], ExtraArgs={'ContentType':"image/jpeg"})

