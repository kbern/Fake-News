#EMMA HEDVIG PIND HANSEN, MAY 30 2019

from __future__ import print_function

import os
import sys
import numpy as np
import json
import codecs
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Dense, Input, GlobalMaxPooling1D
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding
from tensorflow.keras.models import Model
from tensorflow.keras.initializers import Constant
from tensorflow.keras import layers
from tensorflow.keras.callbacks import CSVLogger

from tensorflow.keras.models import load_model

MAX_SEQUENCE_LENGTH = 1000
MAX_NUM_WORDS = 20000
EMBEDDING_DIM = 100

#build index mapping words in the embeddings set to their embedding vector
embeddings_index = {}
with open('/Users/bernsteinkate/Data_science/Project/data/glove/glove.6B.100d.txt', encoding='utf-8') as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, 'f', sep=' ')
        embeddings_index[word] = coefs

#load texts and labels
with open('/Users/bernsteinkate/Dropbox/Datalogi/Data_science/Project/data/content_238.json') as json_file:
    texts = json.load(json_file)

with open('/Users/bernsteinkate/Dropbox/Datalogi/Data_science/Project/data/labels_238.json') as json_file2:
    labels = json.load(json_file2)

#vectorize text
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

word_index = tokenizer.word_index

data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

#split into test and train
from sklearn.model_selection import train_test_split
X_train, x_test, Y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=123) 

#split into train and validation
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(
    X_train, Y_train, test_size=0.2, random_state=123)

#embedding matrix
num_words = min(MAX_NUM_WORDS, len(word_index)) + 1
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i > MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # words not found in embedding index will be all-zeros.
        embedding_matrix[i] = embedding_vector

def CNN(training_data, training_labels, validation_data, validation_labels):
  """Builds a convolutional neural network w. .... layers....."""

  # load pre-trained word embeddings into an Embedding layer
  # note that we set trainable = False so as to keep the embeddings fixed
  embedding_layer = Embedding(num_words,
                        EMBEDDING_DIM,
                        embeddings_initializer=Constant(embedding_matrix),
                        input_length=MAX_SEQUENCE_LENGTH,
                        trainable=False) #set to True if train embeddings

  # train a 1D convnet with global maxpooling
  sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
  embedded_sequences = embedding_layer(sequence_input)
  x = Conv1D(128, 5, activation='relu')(embedded_sequences)
  x = MaxPooling1D(5)(x)
  x = Conv1D(128, 5, activation='relu')(x)
  x = MaxPooling1D(5)(x)
  x = Conv1D(128, 5, activation='relu')(x)
  x = GlobalMaxPooling1D()(x)
  x = Dense(128, activation='relu', name = 'feature_dense')(x) #name this layer so that we can extract features later on
  preds = Dense(len(training_labels), activation='softmax')(x)

  model = Model(sequence_input, preds)
  model.compile(loss='sparse_categorical_crossentropy', #binary crossentropy: 0 1 category
          optimizer='rmsprop', # Root Mean Square Propagation
          metrics=['acc'])
  #model.summary()

  #save training history to log
  csv_logger = CSVLogger('/Desktop/Data_science/Project/models/history/cnn_100d_238_untrained_training.log', separator=',', append=False)

  model.fit(training_data, training_labels,
        batch_size=128,
        epochs=10,
        validation_data=(validation_data, validation_labels),
        callbacks=[csv_logger])

  return model

#model = CNN(x_train, y_train, x_val, y_val)

#save the model to disk
#model.save('/Users/bruger/Dropbox/Datalogi/Data_science/Project/models/cnn_100d_238_untrained.h5') #untrained glove embeddings

#loss, acc = model.evaluate(x_test, y_test, verbose=0)
#print('Test Accuracy: %f' % (acc*100)) 
#print('Test Loss: %f' % (loss*100))
#62.5% accuracy for the 238 articles
#90.9% accuracy for the 100k

#plot loss and accuracy for each epoch
model = load_model('/Desktop/Data_science/Project/models/cnn_100d_238_untrained.h5')

history = pd.read_csv('/Desktop/Data_science/Project/models/history/cnn_100d_238_untrained_training.log', sep=',', engine='python')
#print(history)

def plot_acc(model_history):
  """Plot model accuracy for each training epoch"""
  epoch = model_history['epoch'].T.values
  acc = model_history['acc'].T.values
  val_acc = model_history['val_acc'].T.values

  plt.plot(epoch, acc)
  plt.plot(epoch, val_acc)
  plt.title('Model accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Validation'], loc='upper left')
  plt.show()

def plot_loss(model_history):
  """Plot model loss for each training epoch"""
  epoch = model_history['epoch'].T.values
  loss = model_history['loss'].T.values
  val_loss = model_history['val_loss'].T.values

  plt.plot(epoch, loss)
  plt.plot(epoch, val_loss)
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Validation'], loc='upper left')
  plt.show()

plot_acc(history)
plot_loss(history)

