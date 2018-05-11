import boto3

s3_client = boto3.client('s3')

s3_client.download_file('cmsc389l-rgaray', 'test/Dcn5WTFUQAA3nma.jpg', 't/new.jpg')