import tweepy, os, shutil
import re

#Twitter API credentials
consumer_key = "t4aP7vw4N8R1G9x691ihMZobR"
consumer_secret = "q9cBS7DeVgkr3bmyu5TWZddMkugN56Rl2wXWuBBdQ6i7L5kkX0"
access_key = "926509240998653952-dEwYPl0Yx9DZ6kQGprLv0iu5KtfjgHf"
access_secret = "8dT6ciAFz0q7MXRN5OFy8o92I9Raj7aWcfXYjaxfRyw9K"

folderSizes = []

def get_all_tweets(folderName, screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	print("---------------------------------------------------------")
	print("Populating: "+folderName+"...") 
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

	print ('Retrieved '+str(len(alltweets))+' tweets for '+screen_name)
	
	count = 0
	#write the files
	for i in range(0, len(alltweets)):
		if alltweets[i].full_text != '':
			with open(folderName+'tweet_'+str(i)+'.txt', 'w') as outFile:
				outFile.write(alltweets[i].full_text)
			count += 1

	print ('Wrote '+str(count)+' text files to '+folderName)
	print("---------------------------------------------------------\n")
	
	folderSizes.append(count)

def main():
	with open('celebrities.txt', 'r') as inFile:
		celebrities = inFile.readlines()

	for celebrity in celebrities:
		celebrity = celebrity.split()
		if os.path.exists('celebrities/'+celebrity[0]):
			shutil.rmtree('celebrities/'+celebrity[0])
		os.makedirs('celebrities/'+celebrity[0])

	for celebrity in celebrities:
		celebrity = celebrity.split()
		get_all_tweets('celebrities/'+str(celebrity[0])+'/', celebrity[1])

	minFolder = min(folderSizes)

	print("Minimum amount of tweets: "+str(minFolder)+'\n')

	for celebrity in celebrities:
		celebrity = celebrity.split()
		files = os.listdir('celebrities/'+str(celebrity[0])+'/')
		for file in files:
			file = str(file)
			num = int(file[6:-4])
			if num >= minFolder:
				os.remove('celebrities/'+str(celebrity[0])+'/'+file)

	print("---------------------------------------------------------")
	for celebrity in celebrities:
		celebrity = celebrity.split()
		files = os.listdir('celebrities/'+str(celebrity[0])+'/')
		size = len(files)
		print("Number of tweets being used for "+str(celebrity[1])+": "+str(size))
	print("---------------------------------------------------------\n")

	print("Removing links and unwanted data...")
	for celebrity in celebrities:
		celebrity = celebrity.split()
		path = 'celebrities/'+str(celebrity[0])+'/'
		files = os.listdir(path)
		for file in files:
			with open(path+str(file), 'r') as inFile:
				tweet = inFile.read()
				result = re.sub(r"http\S+", "", tweet)
			with open(path+str(file), 'w') as outFile:
				outFile.write(result)
			
	print("Database is all set!")

if __name__ == '__main__':
	main()