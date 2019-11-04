# -*- coding: utf-8 -*-
import os
import datetime
import pickle
import quandl
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.contrib import rnn

# https://docs.quandl.com/v1.0/docs

def date_obj_to_str(date_obj):
    return date_obj.strftime('%Y-%m-%d')

def save_pickle(something, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as fp:
        pickle.dump(something, fp, pickle.DEFAULT_PROTOCOL)

def load_pickle(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)

def fetch_stock_price(symbol, from_date, to_date, cache_path=os.getcwd()):
    filename = "{}_{}_{}.pk".format(symbol, str(from_date), str(to_date))
    price_filepath = os.path.join(cache_path, filename)
    try:
        prices = load_pickle(price_filepath)
        print("loaded from", price_filepath)
    except IOError:
        historic = quandl.get("WIKI/" + symbol, start_date=date_obj_to_str(from_date), end_date=date_obj_to_str(to_date))
        prices = historic["Adj. Close"].tolist()
        save_pickle(prices, price_filepath)
        print("saved into", price_filepath)
    return prices

def format_dataset(values, temporal_features):
    feat_splits = [values[i:i + temporal_features] for i in range(len(values) - temporal_features)]
    feats = np.vstack(feat_splits)
    labels = np.array(values[temporal_features:])
    return feats, labels
'''
def fetch_cosine_values(seq_len, frequency=0.01, noise=0.1):
    np.random.seed(101)
    x = np.arange(0.0, seq_len, 1.0)
    return np.cos(2 * np.pi * frequency * x) + np.random.uniform(low=-noise, high=noise, size=seq_len)
'''
def matrix_to_array(m):
    return np.asarray(m).reshape(-1)

def evaluate_ts(features, y_true, y_pred):
    print("Evaluation of the predictions:")
    print("MSE:", np.mean(np.square(y_true - y_pred)))
    print("mae:", np.mean(np.abs(y_true - y_pred)))

    print("Benchmark: if prediction == last feature")
    print("MSE:", np.mean(np.square(features[:, -1] - y_true)))
    print("mae:", np.mean(np.abs(features[:, -1] - y_true)))

    plt.plot(matrix_to_array(y_true), 'b')
    plt.plot(matrix_to_array(y_pred), 'r--')
    plt.xlabel("Days")
    plt.ylabel("Predicted and true values")
    plt.title("Predicted (Red) VS Real (Blue)")
    plt.show()

    error = np.abs(matrix_to_array(y_pred) - matrix_to_array(y_true))
    plt.plot(error, 'r')
    fit = np.polyfit(range(len(error)), error, deg=1)
    plt.plot(fit[0] * range(len(error)) + fit[1], '--')
    plt.xlabel("Days")
    plt.ylabel("Prediction error L1 norm")
    plt.title("Prediction error (absolute) and trendline")
    plt.show()

def RNN(x, weights, biases, time_dimension, n_embeddings):
    x_ = tf.unstack(x, time_dimension, 1)
    lstm_cell = rnn.BasicLSTMCell(n_embeddings)
    outputs, _ = rnn.static_rnn(lstm_cell, x_, dtype=tf.float32)
    return tf.add(biases, tf.matmul(outputs[-1], weights))

def main():
    tf.reset_default_graph()
    tf.set_random_seed(101)
    np.random.seed(101)
    
    symbols = ['GOOG', 'MSFT', 'KO', 'AAL', 'MMM', 'AXP', 'GE', 'GM', 'JPM', 'UPS']
    sel = int(input('\n1. Google\n2. Microsoft\n3. Coca-Cola\n4. American Airlines\n5. 3M\n6. American Express\n8. General Electric\n9. General Motors\n10. JPMorgan Chase\n11. United Parcel Service\nSelect : '))
    symbol = symbols[sel - 1]

    time_dimension = 20
    
    tf_logdir = os.getcwd() + '\\graph'
    os.makedirs(tf_logdir, exist_ok=1)
    
    learning_rate = 0.1
    optimizer = tf.train.AdagradOptimizer
    n_epochs = 5000
    n_embeddings = 256

    start_date = input('Input start date(2017.1.1): ')
    end_date = input('Input end date(2018.12.31): ')

    # Fetch the values, and prepare the train/test split
    stock_values = fetch_stock_price(symbol, datetime.date(int(start_date.split('.')[0]), int(start_date.split('.')[1]), int(start_date.split('.')[2])), datetime.date(int(end_date.split('.')[0]), int(end_date.split('.')[1]), int(end_date.split('.')[2])))
    minibatch_cos_X, minibatch_cos_y = format_dataset(stock_values, time_dimension)
    
    train_size = len(stock_values) // 2
    test_size = train_size - time_dimension
    
    train_X = minibatch_cos_X[:train_size, :].astype(np.float32)
    train_y = minibatch_cos_y[:train_size].reshape((-1, 1)).astype(np.float32)
    test_X = minibatch_cos_X[train_size:, :].astype(np.float32)
    test_y = minibatch_cos_y[train_size:].reshape((-1, 1)).astype(np.float32)
    
    train_X_ts = train_X[:, :, np.newaxis]
    test_X_ts = test_X[:, :, np.newaxis]
    
    # Here, the tensorflow code
    X_tf = tf.placeholder('float', shape=(None, time_dimension, 1), name='X')
    y_tf = tf.placeholder('float', shape=(None, 1), name='y')

    # Store layers weight & bias
    weights = tf.Variable(tf.truncated_normal([n_embeddings, 1], mean=0.0, stddev=10.0), name='weights')
    biases = tf.Variable(tf.zeros([1]), name='bias')
    
    # Model, cost and optimizer
    y_pred = RNN(X_tf, weights, biases, time_dimension, n_embeddings)
    with tf.name_scope('cost'):
        cost = tf.reduce_mean(tf.square(y_tf - y_pred))
        train_op = optimizer(learning_rate).minimize(cost)
        tf.summary.scalar('MSE', cost)
    
    with tf.name_scope('mae'):
        mae_cost = tf.reduce_mean(tf.abs(y_tf - y_pred))
        tf.summary.scalar('mae', mae_cost)
    
    with tf.Session() as sess:
        writer = tf.summary.FileWriter(tf_logdir, sess.graph)
        merged = tf.summary.merge_all()
        sess.run(tf.global_variables_initializer())
    
        # For each epoch, the whole training set is feeded into the tensorflow graph
        for i in range(n_epochs):
            summary, train_cost, _ = sess.run([merged, cost, train_op], feed_dict={X_tf: train_X_ts, y_tf: train_y})
            writer.add_summary(summary, i)
            if i % 100 == 0:
                print('Training iteration', i, 'MSE', train_cost)
    
        # After the training, let's check the performance on the test set
        test_cost, y_pr = sess.run([cost, y_pred], feed_dict={X_tf: test_X_ts, y_tf: test_y})
        print('Test dataset :', test_cost)
    
        # Evaluate the results
        evaluate_ts(test_X, test_y, y_pr)
    
        # How does the predicted look like?
        plt.plot(range(len(stock_values)), stock_values, 'b')
        plt.plot(range(len(stock_values)-test_size, len(stock_values)), y_pr, 'r--')
        plt.xlabel('Days')
        plt.ylabel('Predicted and true values')
        plt.title('Predicted (Red) VS Real (Blue)')
        plt.show()

if __name__ == '__main__':
    main()