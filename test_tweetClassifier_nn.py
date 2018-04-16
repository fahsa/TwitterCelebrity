import pandas as pd
import numpy as np
import tensorflow as tf
import os
import json
from collections import Counter
from tweetClassifier_nn import next_batch, multilayer_perceptron
from features import feature_engineering
from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file

# Celebrities
celebrities = {0:'Ariana_Grande', 1:'Barack_Obama', 2:'Bill_Gates', 3:'Britney_Spears', 4:'Bruno_Mars', 5:'Demi_Lovato', 6:'Donald_Trump', 7:'Ellen_DeGeneres', 8:'Jimmy_Fallon', 9:'Justin_Bieber', 10:'Justin_Timberlake', 11:'Katy_Perry', 12:'Kevin_Hart', 13:'Kim_Kardashian', 14:'Lady_Gaga', 15:'LeBron_James', 16:'Miley_Cyrus', 17:'Oprah_Winfrey', 18:'Rihanna', 19:'Selena_Gomez'}

def next_batch(df, i, batch_size, word_index):
    batch = []
    result = []
    X_words = df['words'][i * batch_size: i * batch_size + batch_size]
    X_features = df['features'][i * batch_size: i * batch_size + batch_size]

    # Word and feature vectors
    for word_vector, feature_vector in zip(X_words, X_features):
        # Length of vocabulary + 10 additional features
        layer = np.zeros(len(word_index) + 10, dtype=float)
        for index, feature in enumerate(feature_vector):
            layer[index] = feature
        for word in word_vector:
            if word in word_index:
                layer[10 + word_index[word]] += 1
            else:
                layer[10 + word_index['<UNK>']] += 1
        batch.append(layer)

    return np.array(batch)

def run_nn_method(directory):
    # Load test data
    data = []
    with open('nn_word_index.json', 'r') as f:
        word_index = json.load(f)
    for fname in os.listdir(directory):
        with open(directory + '/' + fname) as f:
            data.append([f.readlines()[0]])
    df = pd.DataFrame.from_records(data, columns = ['text'])
    df = feature_engineering(df)

    saver = tf.train.import_meta_graph("./nn_model.ckpt.meta")

    # Start session
    with tf.Session() as sess:
        # Restore previously trained variables from disk
        saver.restore(sess, "./nn_model.ckpt")

        # Retrieve protobuf graph definition
        graph = tf.get_default_graph()

        # Access restored placeholder variables
        input_tensor = graph.get_tensor_by_name("input:0")
        output_tensor = graph.get_tensor_by_name("output:0")

        # Access restored weights and bias
        weights = {
            'h1': graph.get_tensor_by_name("wh1:0"),
            'h2': graph.get_tensor_by_name("wh2:0"),
            'out': graph.get_tensor_by_name("wo:0")
        }
        biases = {
            'b1': graph.get_tensor_by_name("bh1:0"),
            'b2': graph.get_tensor_by_name("bh2:0"),
            'out': graph.get_tensor_by_name("bo:0")
        }

        # Predict results
        pred = multilayer_perceptron(input_tensor, weights, biases)

        total_test_data = len(df)
        batch_x = next_batch(df, 0, total_test_data, word_index)
        results = sess.run(tf.nn.softmax(pred), feed_dict={input_tensor: batch_x})

        # Output results
        celeb_index = Counter()
        with open('nn_output', 'w') as f:
            for result in results:
                max_idx = np.argmax(result)
                celeb_index[max_idx] += 1
            for key, val in celeb_index.most_common(3):
                f.write(celebrities[key].replace("_", " ") + '\n' + str(val/total_test_data) + '\n')
        f.close()

def main():
    run_nn_method('testUser/')

if __name__ == '__main__':
    main()
