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

model = load_model('model/model-12.hdf5')
sentences = np.array(["Great project!Wondeful work"])
test_sentence = tok.texts_to_sequences(sentences)
test_sentence = sequence.pad_sequences(test_sentence, maxlen=maxlen)
labels = ['Neutral','Positive','Negative']
pred = model.predict(test_sentence)
for i in range(len(pred)):
    print("Review:",sentences[i])
    print("%s sentiment with %.2f%% confidence" % (labels[np.argmax(pred[i])], pred[i][np.argmax(pred[i])] * 100))
