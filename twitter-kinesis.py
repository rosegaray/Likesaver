import tweepy 
from tweepy import OAuthHandler
import boto3
import json
import twitterCredentials as twitterCreds


#Connecting to kinesis
kinesis = boto3.client('kinesis')

#overrides streamlistener
class MyStreamListener(tweepy.StreamListener):
	
	
		

	#Pushing data to kinesis stream
	def on_data(self, data):
		
		b = json.loads(data)
		print(type(data))
		if("event" in list(b.keys())):
			if(b["event"] == 'favorite'):
				print(type(b['target_object']['entities']['media'][0]))
				#if type is photo then save the media_url and upload to dropbox
				#make sure event is a favorite!!
			
				#partition key should be username? identifier in dynamo db for the user
				#print(b["target_object"]["entities"]["media"])
				if(b["target_object"]["entities"]["media"][0]["type"] == "photo"):
					pic_url = b['target_object']['entities']['media'][0]['media_url']
					print(pic_url)
					kinesis.put_record(StreamName="twitter", Data=json.dumps(pic_url), PartitionKey="filler")
					return True
	

## authenticating users' twitter credentials
CONSUMER_KEY = twitterCreds.consumer_key
CONSUMER_SECRET = twitterCreds.consumer_secret
ACCESS_TOKEN_KEY = twitterCreds.access_token_key
ACCESS_TOKEN_SECRET = twitterCreds.access_token_secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)  
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)  
api = tweepy.API(auth)

# Creating a stream to listen for user activity
twitterStream = tweepy.Stream(auth, MyStreamListener())
twitterStream.userstream()




#for item in request:
 #       kinesis.put_record(StreamName="twitter", Data=json.dumps(item), PartitionKey="filler")
