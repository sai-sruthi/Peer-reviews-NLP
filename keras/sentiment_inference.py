#code to supress all warnings
import sys, os
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

#python and keras imports
import numpy as np
import pandas as pd
from keras.preprocessing import sequence,text
from keras.models import load_model
np.random.seed(7)

maxlen = 50

#create tokenizer
df = pd.read_csv('data/labelled_data.csv',encoding='latin1')
tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['comment_text']))

#load model and make predictions
model = load_model('model/model-17.hdf5')
sentences = np.array(["Great work! Well done!"])
test_sentence = tok.texts_to_sequences(sentences)
test_sentence = sequence.pad_sequences(test_sentence, maxlen=maxlen)
labels = ['Neutral','Positive','Negative']
pred = model.predict(test_sentence)
for i in range(len(pred)):
    print("Review:",sentences[i])
    print("%s sentiment with %.2f%% confidence" % (labels[np.argmax(pred[i])], pred[i][np.argmax(pred[i])] * 100))
