import re, os


def main():
	path = 'celebrities/Ariana_Grande/'
	files = ['tweet_0.txt', 'tweet_1.txt', 'tweet_2.txt', 'tweet_3.txt']
	for i in range(0, 4):
		with open(path+str(files[i]), 'r') as inFile:
			tweet = inFile.read()
			result = re.sub(r"http\S+", "", tweet)
			print("File: "+str(files[i]))
			print(result+'\n')
		with open(path+str(files[i]), 'w') as outFile:
			outFile.write(result)		

if __name__ == '__main__':
	main()