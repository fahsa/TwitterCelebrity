# Nick Shahin
# shahinna
# Code modified from Project 1 Part 2: Language Identification

import re
import sys
import os
import math

def main():
    celeb_pos = []
    character_frequencies = []
    character_bigrams = []
    test_dir = "celebrities/"
    test_celebs = os.listdir(test_dir)
    for celeb in test_celebs:
        count = 0
        if celeb == ".DS_Store":
            continue
        cur_dir = test_dir+celeb+"/"
        temp = trainBigramModel(cur_dir)
        character_frequencies.append(temp[0])
        character_bigrams.append(temp[1])
        celeb_pos.append(celeb)

    test_file = open("test_tweet.txt", 'r')
    test_text = test_file.read()
    test_file.close()
    celeb = identifyCelebrity(test_text, celeb_pos, character_frequencies, character_bigrams)
    print(celeb)

def trainBigramModel(tweet_directory):
    character_frequencies = {}
    character_bigram = {}
    total_chars = 0

    print(tweet_directory)
    for tweet in os.listdir(tweet_directory):
        input_file = open(tweet_directory+tweet, 'r')
        input_string = input_file.read()
        input_file.close()
        input_string = input_string.replace("\n", "")

        # Character frequencies
        for c in input_string:
            if c not in character_frequencies:
                character_frequencies[c] = 1
            else:
                character_frequencies[c] = character_frequencies[c] + 1
            total_chars+=1

        # Character-bigram frequencies
        bigram = ' ' + input_string[0]
        character_bigram[bigram] = 1
        idx = 1
        while idx < len(input_string):
            bigram = input_string[idx-1] + input_string[idx]
            if bigram not in character_bigram:
                character_bigram[bigram] = 1
            else:
                character_bigram[bigram] = character_bigram[bigram] + 1
            idx+=1
    print(total_chars)

    return(character_frequencies, character_bigram)

def identifyCelebrity(test_text, celeb_list, character_frequencies, character_bigrams):
    pos = 0
    test_text = test_text.replace("\n", "")
    test_text = " " + test_text
    probabilities = []

    while pos < len(celeb_list):
        probabilities.append(0.0)
        idx = 0
        while idx < len(test_text)-1:
            bigram_count = 1
            char_count =  int(len(character_frequencies[pos]))

            bigram = test_text[idx] + test_text[idx+1]
            if bigram in character_bigrams[pos]:
                bigram_count = character_bigrams[pos][bigram] + 1

            if test_text[idx] in character_frequencies[pos]:
                char_count = character_frequencies[pos][test_text[idx]] + char_count

            fraction = float(bigram_count) / float(char_count)
            logged_fraction = math.log10(fraction)
            if probabilities[pos] == 0:
                probabilities[pos] = logged_fraction
            else:
                probabilities[pos] = probabilities[pos] + logged_fraction

            idx+=1
        pos+=1
    
    print(probabilities)
    return celeb_list[probabilities.index(max(probabilities))]

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
