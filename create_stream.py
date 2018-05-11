# create-stream.py
#just boto?

import boto3

client = boto3.client('kinesis')
client.create_stream(StreamName = "twitter", ShardCount = 1)