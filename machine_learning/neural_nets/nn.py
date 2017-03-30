
# coding: utf-8

# # Neural Networks for MNIST dataset

# ## Loading data

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from keras.datasets import mnist

seed = 7
np.random.seed(seed)

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)
num_classes = Y_test.shape[1]

## Simple 2- layer NN
from keras.models import Sequential
from keras.layers import Dense, Activation

# for the number of neurons in the hidden unit
M = 300
model1 = Sequential()
model1.add(Dense(M, input_dim=num_pixels, init='normal', activation='relu'))
model1.add(Dense(10, activation='softmax'))

learning_rates = [1.0, 0.1, .01, .001, .0001, .00001]

# In[30]:

def get_model(lr=0.001, M=300):
    model = Sequential()
    model.add(Dense(M, input_dim=num_pixels, init='normal', activation='relu'))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])
    model.optimizer.lr.set_value(lr)
    return model

# problem 2.1
print "\n##### Problem 2.1 #######\n"
for lr in learning_rates:
    # print some kind of dividing text here
    print "------------ NN Model with Learning rate %f------------\n" % lr
    model = get_model(lr)
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=10, batch_size=200, verbose=2)
    # Final evaluation of the model
    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Baseline Error: %.2f%%" % (100-scores[1]*100))
    print "\n\n\n"

# problem 2.2
print "\n##### Problem 2.2 #######\n"
layer_sizes = [10,50,100,100,300,1000,2000]
for layer_size in layer_sizes:
    print "------------ NN Model with Hidden Layers Size %d------------\n" % layer_size
    model = get_model(lr=0.01, M=layer_size)
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=10, batch_size=200, verbose=2)
    # Final evaluation of the model
    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Baseline Error: %.2f%%" % (100-scores[1]*100))
    print "\n\n\n"

# ## Models with L2 regularization

from keras.regularizers import l2

def get_reg_model(lr=0.001, M=300, w=0.1):
    model = Sequential()
    model.add(Dense(M, input_dim=num_pixels, init='normal', activation='relu', W_regularizer=l2(w)))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])
    model.optimizer.lr.set_value(lr)
    return model

# 2.3
print "\n##### Problem 2.3 #######\n"
print "\n------------ NN Model with Learning Rate 0.01 ------------\n"
model1 = get_model(lr=0.01, M=300)
model1.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=10, batch_size=200, verbose=2)
scores = model1.evaluate(X_test, Y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

print "\n------------ NN Model with Learning Rate 0.001 ------------\n"
model2 = get_model(lr=0.001, M=300)
model2.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=10, batch_size=200, verbose=2)
scores = model2.evaluate(X_test, Y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

print "\n------------ NN Model with L2 Regularization 0.002 ------------\n"
reg_model = get_reg_model(lr=.001, M=300, w=0.002)
reg_model.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=30, batch_size=200, verbose=2)
scores = reg_model.evaluate(X_test, Y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))


# ## Models with Dropout

def get_dropout_model(lr=0.001, M=300, w=0.2):
    model = Sequential()
    model.add(Dense(M, input_dim=num_pixels, init='normal', activation='relu'))
    model.add(Dropout(w))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])
    model.optimizer.lr.set_value(lr)
    return model

# 2.4
print "\n##### Problem 2.4 #######\n"
dropout_weights = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]
for drp_w in dropout_weights:
    print "------------ NN Model with Dropout Weight %f ------------\n" % drp_w
    model = get_dropout_model(lr=.001, M=300, w=drp_w)
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), nb_epoch=10, batch_size=200, verbose=2)
    scores = model.evaluate(X_test, Y_test, verbose=0)
    print("Baseline Error: %.2f%%" % (100-scores[1]*100))
    print "\n\n\n"

# 2.5

# NN 300 + 100

# NN 500 + 150

# NN 500 + 300
