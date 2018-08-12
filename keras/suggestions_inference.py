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
df = pd.read_csv('data/suggestions_data.csv',encoding='latin1')
tok = text.Tokenizer(num_words=200000)
tok.fit_on_texts(list(df['comments']))

#load model and make predictions
model = load_model('model/suggestions/model-11.hdf5')
sentences = np.array(["Yes. The team contribute a lot of test code and no obvious missing"])
test_sentence = tok.texts_to_sequences(sentences)
test_sentence = sequence.pad_sequences(test_sentence, maxlen=maxlen)
labels = ['absent','present']
pred = model.predict(test_sentence)
for i in range(len(pred)):
    print("Review:",sentences[i])
    print(pred[i])
    print("In this review, suggestions are %s" % labels[1 if pred[i] > 0.5 else 0])
