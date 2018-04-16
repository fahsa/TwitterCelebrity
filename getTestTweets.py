import tweepy, os, shutil, re, sys

#Twitter API credentials
consumer_key = "t4aP7vw4N8R1G9x691ihMZobR"
consumer_secret = "q9cBS7DeVgkr3bmyu5TWZddMkugN56Rl2wXWuBBdQ6i7L5kkX0"
access_key = "926509240998653952-dEwYPl0Yx9DZ6kQGprLv0iu5KtfjgHf"
access_secret = "8dT6ciAFz0q7MXRN5OFy8o92I9Raj7aWcfXYjaxfRyw9K"

def get_test_tweets(screen_name):
	if os.path.exists('testUser/'):
		shutil.rmtree('testUser/')
	os.makedirs('testUser/')

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold the tweepy Tweets
	alltweets = api.user_timeline(screen_name=screen_name, count=40, tweet_mode='extended')	
	
	count = 0
	#write the files
	for i in range(0, len(alltweets)):
		tweet = alltweets[i].full_text
		tweet = re.sub(r"http\S+", "", tweet)
		if (tweet != "") and (not tweet.isspace()):
			with open('testUser/tweet_'+str(count)+'.txt', 'w') as outFile:
				outFile.write(tweet)
			count += 1
		if count == 20:
			break

	print ('Wrote '+str(count)+' text files to testUser/')

if __name__ == '__main__':
	get_test_tweets(sys.argv[1])