import sys, json, webbrowser
from getTestTweets import get_test_tweets
#from tweetClassifier_nn import run_nn_method
from tweetSimilarity import run_rocchio_method
from tweetIdentification_char import run_bigram_char_method
from tweetIdentification_word import run_bigram_word_method

def read_in():
    # Read username from front end
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    lines = read_in()
    username = ''
    for item in lines:
        username += item

    # Gather 20 most recent tweets from given username
    # Make the testUser/ folder
    print("Retrieving test tweets...")
    get_test_tweets(username)
    print("Done making testUser/!")

    '''# Run Neural Network method 
    # Make nn.out file
    print("Running Neural Network..")
    run_nn_method()
    print("Done with Neural Network!")'''

    # Run Rocchio method
    # Make rocchio.out file
    print("Running Rocchio...")
    run_rocchio_method('testUser')
    print("Done with Rocchio!")

    # Run Bigram Char method
    # Make bigram_char.out file
    print("Running Bigram (Character)...")
    run_bigram_char_method()
    print("Done with Bigram (Character)!")

    # Run Bigram Word method
    # Make bigram_word.out file
    print("Running Bigram (Word)...")
    run_bigram_word_method()
    print("Done with Bigram (Word)!")

if __name__ == '__main__':
    main()