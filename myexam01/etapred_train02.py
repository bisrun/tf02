import tensorflow as tf
import numpy as np
import pysal as ps
import os
import pandas as pd
import geopandas as gpd
import itertools
from shapely.geometry import Point


# hyper parameters

class nn_model:
    def __init__(self, sess, name):

        self.sess = sess
        self._learning_rate = 0.001

        self._out_file_name = ''
        self._selected_col = ['L_CODE', 'geometry']

        self._read_loop_cnt = 0;
        self._set_read_line_count = 5  # 한번에 읽는 라인수
        self._read_line_count = 0  # 실제 읽은 라인수
        self._total_read_line_count = 0  # 이제까지 읽은 전체 라인수
        self._read_line = 0  #

        self._base_folder = 'D:\\project\\temp\\p1\\'
        self._w_folder = 'rst\\'

        self._file_in = None
        self._folder_log = None

        self._batch_loop = 1
        self._df = None

        self._x_data = np.ndarray([], dtype=np.int32)
        self._y_data = np.ndarray([], dtype=np.int32)
        self._ph_x = None
        self._ph_y = None

        self._debug_mode = False # #####################
        self._optimizer = None
        self._cost = None

        self._hypothesis = None
        self._file_line_count = 0
        self.training = True

        self.build_net()

        self.saver = tf.train.Saver()

    def save_model(self, model_path):
        self.saver.save(self.sess, model_path)

    def restore_model(self, model_path):
        self.saver.restore(self.sess, model_path)

    def data_open(self):
        try:
            if self._debug_mode == True:
                self._in_file_name = 'logrx_{0}'.format('s1.txt')
                self._set_read_line_count = 5
                self._file_in = os.path.join(self._base_folder, self._in_file_name)
            else:
                self._in_file_name = 'logrx_{0}'.format('201806.txt')
                self._set_read_line_count = 1000

                self._file_in = os.path.join(self._base_folder, self._in_file_name)
                self._folder_log = os.path.join(self._base_folder, 'logs\\')

                # self._file_line_count = sum(1 for line in open(self._file_in)) -1

        except KeyboardInterrupt:
            print('\n\rquit')

    def fetch_data(self):
        read_line_cnt = 0
        try:
            self._batch_loop = 1;

            for lines in pd.read_csv(self._file_in,
                                     chunksize=self._set_read_line_count):
                # columns
                #   'WD',       'DAYMIN',       'X',            'Y',        'X2',
                #   'Y2',       'A_SPEND_TIME', 'E_SPEND_TIME', 'TOT_LEN',  'L_CODE1',
                #   'L_CODE2',  'LC1_V1',       'LC1_V2',       'LC1_V3',   'LC2_V1',
                #   'LC2_V2',   'LC2_V3'
                self._df = lines.values;

                self._x_data = self._df[:, [0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16]]
                self._y_data = self._df[:, [6]]


                self._read_line_count = len(lines)
                self._read_loop_cnt += 1;


                # columns
                #   'WD',       'DAYMIN',       'X',            'Y',        'X2',
                #   'Y2',       'A_SPEND_TIME', 'E_SPEND_TIME', 'TOT_LEN',  'L_CODE1',
                #   'L_CODE2',  'LC1_V1',       'LC1_V2',       'LC1_V3',   'LC2_V1',
                #   'LC2_V2',   'LC2_V3'

            read_line_cnt = len(lines)
            print("read line count = %d"% read_line_cnt )



        except KeyboardInterrupt:
            print('\n\rquit')

        return read_line_cnt

    def build_net(self):

        self._ph_x = tf.placeholder(tf.float32, [None, 14], name='x-input')
        self._ph_y = tf.placeholder(tf.float32, [None, 1], name='y-input')

        with tf.name_scope("layer1"):
            W1 = tf.Variable(tf.random_normal([14, 32]), name='weight1')
            b1 = tf.Variable(tf.random_normal([32]), name='bias1')
            layer1 = tf.sigmoid(tf.matmul(self._ph_x, W1) + b1)

            # w1_hist = tf.summary.histogram("weights1", W1)
            # b1_hist = tf.summary.histogram("biases1", b1)
            # layer1_hist = tf.summary.histogram("layer1", layer1)

        with tf.name_scope("layer2"):
            W2 = tf.Variable(tf.random_normal([32, 56]), name='weight2')
            b2 = tf.Variable(tf.random_normal([56]), name='bias2')
            layer2 = tf.sigmoid(tf.matmul(layer1, W2) + b2)

            # w2_hist = tf.summary.histogram("weights2", W2)
            # b2_hist = tf.summary.histogram("biases2", b2)
            # layer2_hist = tf.summary.histogram("layer2", layer2)

        with tf.name_scope("layer3"):
            W3 = tf.Variable(tf.random_normal([56, 1]), name='weight3')
            b3 = tf.Variable(tf.random_normal([1]), name='bias3')

            # self._logits = tf.matmul(layer2, W3) + b3
            self._hypothesis = tf.matmul(layer2, W3) + b3

            # self._hypothesis = tf.nn.relu(self._logits)

            # w3_hist = tf.summary.histogram("weights3", W3)
            # b3_hist = tf.summary.histogram("biases3", b3)
            # hypothesis_hist = tf.summary.histogram("hypothesis", hypothesis)

        # cost/loss function
        with tf.name_scope("cost"):
            self._cost = tf.reduce_mean(tf.square(self._hypothesis - self._y_data))

            # cost = -tf.reduce_mean(self._y_data * tf.log(hypothesis) + (1 - self._y_data) *
            #                       tf.log(1 - hypothesis))
            # cost_summ = tf.summary.scalar("cost", self._cost)

        with tf.name_scope("optimizer"):
            self._optimizer = tf.train.AdamOptimizer(learning_rate=self._learning_rate).minimize(self._cost)

        # correct_prediction =  tf.abs( self._hypothesis - tf.argmax(self._y_data ) < 5

        # self._accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        # predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
        # accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, self._y_data), dtype=tf.float32))
        # accuracy_summ = tf.summary.scalar("accuracy", accuracy)

    def predict(self, x_test, training=False):
        return self.sess.run(self._hypothesis,
                             feed_dict={self._x_data: x_test, self.training: training})

    def get_accuracy(self, x_test, y_test, training=False):
        return self.sess.run(self._accuracy,
                             feed_dict={self._x_data: x_test,
                                        self._y_data: y_test, self.training: training})

    def run_train(self, x_data, y_data, training=True):
        return self.sess.run([self._cost, self._optimizer], feed_dict={
            self._ph_x: x_data, self._ph_y: y_data})


def run():
    try:

        sess = tf.Session()
        model = nn_model(sess, "nn_model_")
        model.data_open();
        # Initialize TensorFlow variables
        sess.run(tf.global_variables_initializer())
        fetch_loop = 0
        training_epochs = 20
        batch_size = 100
        avg_cost = 0

        print('Learning Started!')
        # if debug_mode == True:
        #    print(lines)
        for step in range(training_epochs):
            # total_batch = int(model._file_line_count / model._set_read_line_count)

            while model.fetch_data() > 0:
                fetch_loop += 1
                # tensorboard --logdir=./logs/xor_logs
                # merged_summary = tf.summary.merge_all()
                #log_file_name = 'logs_s{0}_f{1}.log'.format(step, fetch_loop)
                #file_log = os.path.join(model._folder_log, log_file_name)

                #writer = tf.summary.FileWriter(file_log)
                #writer.add_graph(sess.graph)  # Show the graph

                c, _ = model.run_train(model._x_data, model._y_data)


                # avg_cost += c / total_batch

                if fetch_loop % 10 == 0:
                    print('step {0} cost={1}'.format(step, c))

                if fetch_loop % 50 == 0:
                    save_name = 'eta_model_{}_{}.model'.format(step, fetch_loop )
                    print('save : step {0} cost={1}'.format(step, c))
                    model.save_model(save_name)


                print('step {0} cost={1}'.format(step, c))
                # Accuracy report
                # h, c, a = sess.run([model._hypothesis, model._predicted, model._accuracy],
                #                   feed_dict={_ph_x: _x_data, _ph_y: _y_data})
                # print("\nHypothesis: ", h, "\nCorrect: ", c, "\nAccuracy: ", a)


    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
