# Nick Shahin
# shahinna
# Code modified from Project 1 Part 2: Language Identification

import re
import sys
import os
from tweetIdentification_word import test

def main():
    correct = 0
    total = 0
    celeb_dir = "celebrities/"
    for celeb in os.listdir(celeb_dir):
        tweet_dir = celeb_dir + celeb + "/"
        for tweet in os.listdir(tweet_dir):
            # Read tweet to test
            tweet_file = open(tweet_dir+tweet, "r")
            input_text = tweet_file.read()
            tweet_file.close()

            # Save test tweet to test file
            test_file = open("test_tweet.txt", "w")
            test_file.write(input_text)
            test_file.close()

            # Send name of tweet we're withholding
            result = test(tweet)

            # re-save tweet to where it was
            tweet_file = open(tweet_dir+tweet, "w")
            tweet_file.write(input_text)
            tweet_file.close()

            if celeb == result:
                correct+=1
            total+=1
            accuracy = float(correct) / float(total)
            print(str(accuracy))

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()