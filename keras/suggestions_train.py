import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from keras.preprocessing import sequence, text
from keras import metrics
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, BatchNormalization, Activation, Conv1D, MaxPooling1D, Flatten, GlobalMaxPooling1D
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from keras.utils import plot_model
np.random.seed(7)
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

df = pd.read_csv('data/suggestions_data_cleaned.csv',encoding='latin1')

maxlen = 50
batch_size = 128

tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['comments']))
x = tok.texts_to_sequences(df['comments'])
x = sequence.pad_sequences(x, maxlen=maxlen)
y = df['is_prompt_exists']
encoder = LabelEncoder()
encoder.fit(y)
y = encoder.transform(y)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.1)
word_index = tok.word_index


#create a dictionary which stores embeddings for every word
embeddings_index = {}
f = open('data/glove.840B.300d.txt',encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    try:
        coefs = np.asarray(values[1:], dtype='float32')
    except:
        pass
    embeddings_index[word] = coefs
f.close()

#create the embedding matrix mapping every index in the corpus to it's respective embedding_vector
embedding_matrix = np.zeros((len(word_index) + 1, 300))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

model1 = Sequential()
model1.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=True))
model1.add(Dropout(0.6))
model1.add(Bidirectional(LSTM(150,recurrent_dropout=0.6)))
model1.add(Dropout(0.6))
model1.add(Dense(1, activation='sigmoid'))
model1.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model1_history = model1.fit(x_train, y_train, batch_size=batch_size, epochs=9,
                            validation_split=0.1)
score1, acc1 = model1.evaluate(x_test, y_test,
                               batch_size=batch_size)
print('Test accuracy for BiLSTM+Glove Model is:', acc1)
y_pred1 = model1.predict(x_test)
y_pred1 = (y_pred1 > 0.5)
print(classification_report(y_test, y_pred1))

model2 = Sequential()
model2.add(Embedding(len(word_index) + 1,100,input_length=maxlen))
model2.add(Dropout(0.5))
model2.add(Conv1D(100,3,padding='valid',activation='relu',strides=1))
model2.add(GlobalMaxPooling1D())
model2.add(Dense(100, activation='relu'))
model2.add(Dropout(0.5))
model2.add(Dense(1, activation='sigmoid'))
model2.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model2_history = model2.fit(x_train, y_train, batch_size=batch_size, epochs=5,
                            validation_split=0.1)
score2, acc2 = model2.evaluate(x_test, y_test, batch_size=batch_size)
print('Test accuracy for CNN+Dense Model is:', acc2)
y_pred2 = model2.predict(x_test)
y_pred2 = (y_pred2 > 0.5)
print(classification_report(y_test, y_pred2))

model3 = Sequential()
model3.add(Embedding(len(word_index) + 1, 100, input_length=maxlen))
model3.add(Dropout(0.5))
model3.add(Conv1D(50, 5, padding='valid', activation='relu', strides=1))
model3.add(MaxPooling1D(pool_size=4))
model3.add(LSTM(100, recurrent_dropout=0.6))
model3.add(Dropout(0.6))
model3.add(Dense(1, activation='sigmoid'))
model3.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model3_history = model3.fit(x_train, y_train, batch_size=batch_size, epochs=4,
                            validation_split=0.1)
score3, acc3 = model3.evaluate(x_test, y_test, batch_size=batch_size)
print('Test accuracy for CNN+LSTM Model is:', acc3)
y_pred3 = model3.predict(x_test)
y_pred3 = (y_pred3 > 0.5)
print(classification_report(y_test, y_pred3))

model4 = Sequential()
model4.add(Embedding(len(word_index) + 1, 100, input_length=maxlen))
model4.add(Dropout(0.6))
model4.add(LSTM(100, recurrent_dropout=0.6))
model4.add(Dropout(0.6))
model4.add(Dense(1, activation='sigmoid'))
model4.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model4_history = model4.fit(x_train, y_train, batch_size=batch_size, epochs=7,
                            validation_split=0.1)
score4, acc4 = model4.evaluate(x_test, y_test,
                               batch_size=batch_size)
print('Test accuracy for LSTM Model is:', acc4)
y_pred4 = model4.predict(x_test)
y_pred4 = (y_pred4 > 0.5)
print(classification_report(y_test, y_pred4))


"""def plot_history(histories, key='acc'):
  plt.figure(figsize=(16, 10))

  for name, history in histories:
    val = plt.plot(history.epoch, history.history['val_'+key],
                   '--', label=name.title()+' Validation')
    plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
             label=name.title()+' Train')

  plt.xlabel('Epochs')
  plt.ylabel('Accuracy')
  plt.legend()

  plt.xlim([0,max(history.epoch)])
  plt.savefig('figures/all_accuracy.png')


plot_history([('BiLSTM+Glove', model1_history), ('CNN+Dense', model2_history),
              ('CNN+LSTM', model3_history), ('LSTM', model4_history)])"""


# Plot training & validation accuracy values
def plot_history(history, model_name):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title(model_name + ' accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()


plot_history(model1_history, 'BiSLTM+Glove unbalanced')
plot_history(model2_history, 'CNN+Dense unbalanced')
plot_history(model3_history, 'CNN+LSTM unbalanced')
plot_history(model4_history, 'LSTM balanced')

"""plot_model(model1, to_file='figures/BiLSTM+Glove.png', show_shapes=True,
           show_layer_names=True)
plot_model(model2, to_file='figures/CNN+Dense.png', show_shapes=True,
           show_layer_names=True)
plot_model(model3, to_file='figures/CNN+LSTM.png', show_shapes=True,
           show_layer_names=True)
plot_model(model4, to_file='figures/LSTM.png', show_shapes=True,
           show_layer_names=True)"""
