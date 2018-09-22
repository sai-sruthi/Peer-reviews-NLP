import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing import sequence,text
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
np.random.seed(7)

df = pd.read_csv('data/trial_data.csv',encoding='latin1')



maxlen = 50
batch_size = 128

tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['sentence']))
x = tok.texts_to_sequences(df['sentence'])
x = sequence.pad_sequences(x, maxlen=maxlen)
y = df['label']
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
#model1.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=True))
model1.add(Embedding(len(word_index) + 1,100,input_length=maxlen))
model1.add(Dropout(0.5))
model1.add(LSTM(100,recurrent_dropout=0.5))
model1.add(Dropout(0.5))
#model1.add(Dense(128, activation='relu'))
#model1.add(Dropout(0.5))
model1.add(Dense(1, activation='sigmoid'))
model1.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model1_history = model1.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=10,
          validation_split=0.1)
score1, acc1 = model1.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test accuracy for model 1:', acc1)
y_pred1 = model1.predict(x_test)
y_pred1 = (y_pred1 > 0.5)
print(classification_report(y_test, y_pred1))
#print(confusion_matrix(y_test, y_pred1))

"""model2 = Sequential()
#model2.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=False))
model2.add(Embedding(len(word_index) + 1,100,input_length=maxlen))
model2.add(Dropout(0.2))
model2.add(Conv1D(250,3,padding='valid',activation='relu',strides=1))
model2.add(GlobalMaxPooling1D())
model2.add(Flatten())
model2.add(Dense(250, activation = 'relu'))
model2.add(Dropout(0.2))
model2.add(Dense(1, activation='sigmoid'))
model2.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
model2_history = model2.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=5,
          validation_split=0.1)
score2, acc2 = model2.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test accuracy for model 2:', acc2)

def plot_history(histories, key='acc'):
  plt.figure(figsize=(16,10))

  for name, history in histories:
    val = plt.plot(history.epoch, history.history['val_'+key],
                   '--', label=name.title()+' Validation')
    plt.plot(history.epoch, history.history[key], color=val[0].get_color(),
             label=name.title()+' Train')

  plt.xlabel('Epochs')
  plt.ylabel(key.replace('_',' ').title())
  plt.legend()

  plt.xlim([0,max(history.epoch)])
  plt.show()


plot_history([('model1', model1_history),('model2', model2_history)])"""
