# Nick Shahin
# shahinna
# Code modified from Project 1 Part 2: Language Identification

import re
import sys
import os
import math

def run_bigram_char_method():
    celeb_pos = []
    character_frequencies = []
    character_bigrams = []
    train_dir = "celebrities/"
    test_celebs = os.listdir(train_dir)
    for celeb in test_celebs:
        count = 0
        if celeb == ".DS_Store":
            continue
        cur_dir = train_dir+celeb+"/"
        temp = trainBigramModel(cur_dir)
        character_frequencies.append(temp[0])
        character_bigrams.append(temp[1])
        celeb_pos.append(celeb)

    test_dir = "Test/"
    total = 0
    results = []
    idx = 0
    while idx < len(celeb_pos):
        results.append(0)
        idx+=1

    for tweet in os.listdir(test_dir):
        if tweet == ".DS_Store":
            continue
        test_file = open(test_dir+tweet, 'r')
        tweet_text = test_file.read()
        test_file.close()
        celeb = identifyCelebrity(tweet_text, celeb_pos, character_frequencies, character_bigrams)
        total+=1
        results[celeb_pos.index(celeb)]+=1

    output_file = open("char_output", "w")
    idx = 0
    while idx < 3:
        percent = float(max(results)) / float(total)
        if percent != 0:
            output_file.write(celeb_pos[results.index(max(results))] + "\n")
        else:
            output_file.write("None\n")
        output_file.write(str(percent) + "\n")
        del celeb_pos[results.index(max(results))]
        del results[results.index(max(results))]
        idx+=1
    output_file.close()
    # print(celeb)

def trainBigramModel(tweet_directory):
    character_frequencies = {}
    character_bigram = {}
    total_chars = 0

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
    
    celeb = celeb_list[probabilities.index(max(probabilities))]
    return celeb

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    run_bigram_char_method()
