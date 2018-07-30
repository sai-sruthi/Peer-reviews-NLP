import numpy as np
import pandas as pd
import numpy as np

#keras imports
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

#Import nltk libraries for volume analysis
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords

#set rules for stopwords ignored in volume analysis
stop_words = set(stopwords.words('english'))
stop_words |= {'.',',','!','?'}

#model parameters
maxlen = 50
batch_size = 64

#load the pre-trained model
def loadModel():
    df = pd.read_csv('data/labelled_data.csv',encoding='latin1')
    tok = text.Tokenizer(num_words=200000)
    tok.fit_on_texts(list(df['comment_text']))
    model = load_model('model/model-12.hdf5')
    test_review = np.array(['this is a test review'])
    test_review = tok.texts_to_sequences(test_review)
    test_review = sequence.pad_sequences(test_review, maxlen=maxlen)
    model.predict(test_review)
    return model,tok

#predict sentiment and confidence of the review
def predictSentiment(model,tok,review):
    review = np.array([review])
    review = tok.texts_to_sequences(review)
    review = sequence.pad_sequences(review, maxlen=maxlen)
    labels = ['Neutral','Positive','Negative']
    pred = model.predict(review)
    sentiment_tone = labels[np.argmax(pred[0])]
    sentiment_confidence = pred[0][np.argmax(pred[0])] * 100
    return(sentiment_tone,round(sentiment_confidence,2))

#predict volume metrics of the review
def predictVolume(review):
    #tokenize the review
    tokens = tokenizer.tokenize(review)
    total_volume = len(tokens)
    #remove all the stopwords
    non_stop_words = [word for word in tokens if word not in stop_words]
    volume_without_stopwords = len(non_stop_words)
    return (total_volume,volume_without_stopwords)
