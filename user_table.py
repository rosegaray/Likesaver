import boto3

#Create table to store user info - username, twitter auth token, dropbox auth token, 
# running (yes or no) 

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(