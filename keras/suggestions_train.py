import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing import sequence,text
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional, BatchNormalization, Activation
from keras.datasets import imdb
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder
np.random.seed(7)

df = pd.read_csv('data/suggestions_data.csv',encoding='latin1')

maxlen = 50
batch_size = 32

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

model = Sequential()
model.add(Embedding(len(word_index) + 1,300,weights=[embedding_matrix],input_length=maxlen,trainable=False))
model.add(LSTM(128,recurrent_dropout=0.7))
model.add(Dropout(0.7))
model.add(Dense(1, activation='sigmoid'))
model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath='model/suggestions/model-{epoch:02d}.hdf5', verbose=1)
model_history = model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=20,
          validation_split=0.1,
          callbacks=[checkpointer])
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test accuracy:', acc)

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


plot_history([('model', model_history)])
