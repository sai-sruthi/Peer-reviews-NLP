#python and keras imports
import pandas as pd
import numpy as np
import config
from keras.models import load_model
from keras.preprocessing import sequence,text
np.random.seed(7)

#load the pre-trained model
def loadModel():
    config.maxlen = 50
    df = pd.read_csv('data/labelled_data.csv',encoding='latin1')
    config.keras_tokenizer = text.Tokenizer(num_words=200000)
    config.keras_tokenizer.fit_on_texts(list(df['comment_text']))
    config.model = load_model('model/model-12.hdf5')
    test_review = np.array(['this is a test review'])
    test_review = config.keras_tokenizer.texts_to_sequences(test_review)
    test_review = sequence.pad_sequences(test_review, maxlen=config.maxlen)
    config.model.predict(test_review)
