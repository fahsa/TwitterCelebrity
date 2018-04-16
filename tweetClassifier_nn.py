import pandas as pd
import numpy as np
import tensorflow as tf
import nltk
import string
import re
import json
import os
from collections import Counter
from sklearn.model_selection import train_test_split
from features import feature_engineering

# Celebrities
celebrities  = {'Ariana_Grande':0, 'Barack_Obama':1, 'Bill_Gates':2, 'Britney_Spears':3, 'Bruno_Mars':4, 'Demi_Lovato':5, 'Donald_Trump':6, 'Ellen_DeGeneres':7, 'Jimmy_Fallon':8, 'Justin_Bieber':9, 'Justin_Timberlake':10, 'Katy_Perry':11, 'Kevin_Hart':12, 'Kim_Kardashian':13, 'Lady_Gaga':14, 'LeBron_James':15, 'Miley_Cyrus':16, 'Oprah_Winfrey':17, 'Rihanna':18, 'Selena_Gomez':19}

def load_data():
    with open('twitter_data.json') as data:
        temp = json.load(data)

    df = pd.DataFrame({col:dict(vals) for col, vals in temp.items()})
    # Tokenize
    df = feature_engineering(df)
    train_set, test_set = train_test_split(df, test_size=0.2)

    return train_set, test_set

def gen_word_index(train_set):
    # Common Words (top 9999)
    v_counter = Counter()
    for words in train_set['words']:
        for word in words:
            v_counter[word] += 1
    common_words = dict(v_counter.most_common(9999))

    # Vocabulary (<'UNK'> for words not in the most common)
    vocab = {'<UNK>':0}
    for word in v_counter:
        if word in common_words:
            vocab[word] = v_counter[word]
        else:
            vocab['<UNK>'] += 1

    # Word Index
    word_index = {}
    for index, word in enumerate(vocab):
        word_index[word] = index
    return word_index

def multilayer_perceptron(input_tensor, weights, biases):
    layer_1 = tf.add(tf.matmul(input_tensor, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    # Output layer
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

def next_batch(train_set, i, batch_size, word_index):
    batch = []
    result = []
    X_words = train_set['words'][i * batch_size: i * batch_size + batch_size]
    X_features = train_set['features'][i * batch_size: i * batch_size + batch_size]
    Y = train_set['celebrity'][i * batch_size: i * batch_size + batch_size]

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

    # Label vectors
    for label in Y:
        one_hot = np.zeros(20, dtype=float)
        one_hot[celebrities[label]] = 1
        result.append(one_hot)

    return np.array(batch), np.array(result)

def run_nn(train_set, test_set, word_index):
    # Parameters
    learning_rate = 0.01
    training_epochs = 50
    batch_size = 100
    display_step = 1

    # Network Parameters
    n_hidden_1 = 100
    n_hidden_2 = 100
    n_input = len(word_index) + 10
    n_classes = len(celebrities)

    # Placeholders
    input_tensor = tf.placeholder(tf.float32,[None, n_input],name="input")
    output_tensor = tf.placeholder(tf.float32,[None, n_classes],name="output")

    # Weights and Bias
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1]), name="wh1"),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]), name="wh2"),
        'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]), name="wo")
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1]), name="bh1"),
        'b2': tf.Variable(tf.random_normal([n_hidden_2]), name="bh2"),
        'out': tf.Variable(tf.random_normal([n_classes]), name="bo")
    }

    # Initialize model
    pred = multilayer_perceptron(input_tensor, weights, biases)

    # Define loss function and optimizer
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=output_tensor))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

    # Initializing variables
    init = tf.global_variables_initializer()

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver()

    # Launch graph
    with tf.Session() as sess:
        sess.run(init)
        # Training
        for epoch in range(training_epochs):
            avg_loss = 0.
            total_batch = int(len(train_set)/batch_size)
            # Batches
            for i in range(total_batch):
                batch_x, batch_y = next_batch(train_set, i, batch_size, word_index)
                # Run optimization op and loss op
                c,_ = sess.run([loss, optimizer], feed_dict={input_tensor: batch_x, output_tensor: batch_y})
                # Compute average loss
                avg_loss += c / total_batch
            # Display logs per epoch step
            if epoch % display_step == 0:
                print("Epoch:", '%04d' % (epoch + 1), "loss=", \
                    "{:.9f}".format(avg_loss))
        print("Optimization Finished!")

        # Test model
        correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(output_tensor, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_pred, "float"))
        total_test_data = len(test_set)
        batch_x_test, batch_y_test = next_batch(test_set, 0, total_test_data, word_index)
        print("Accuracy:", accuracy.eval({input_tensor: batch_x_test, output_tensor: batch_y_test}))
        # Save the variables to disk.
        saver.save(sess, "./nn_model.ckpt")

def main():
    train_set, test_set = load_data()
    word_index = gen_word_index(train_set)
    with open('nn_word_index.json', 'w') as f:
        json.dump(word_index, f)
    f.close()
    run_nn(train_set, test_set, word_index)

if __name__ == '__main__':
    main()
