import numpy as np
import pandas as pd
import numpy as np
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

df = pd.read_csv('data/labelled_data.csv',encoding='latin1')

maxlen = 50
batch_size = 64

tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['comment_text']))
x = tok.texts_to_sequences(df['comment_text'])
x = sequence.pad_sequences(x, maxlen=maxlen)
y_cat = to_categorical(df['y_true'], num_classes=3)
x_train,x_test,y_train,y_test = train_test_split(x,y_cat,test_size=0.25)
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
model.add(Bidirectional(LSTM(64,return_sequences=True)))
model.add(Dropout(0.5))
model.add(Bidirectional(LSTM(64,return_sequences=True)))
model.add(Dropout(0.5))
model.add(Bidirectional(LSTM(64)))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))
model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])
checkpointer = ModelCheckpoint(filepath='model/model-{epoch:02d}.hdf5', verbose=1)
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=12,
          validation_data=[x_test, y_test],
          callbacks=[checkpointer])
