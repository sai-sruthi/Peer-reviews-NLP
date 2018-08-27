#python and keras imports
import numpy as np
from keras.preprocessing import sequence,text
np.random.seed(7)

#Import nltk libraries for volume analysis
from nltk.tokenize import TreebankWordTokenizer
treebank_tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords

#set rules for stopwords ignored in volume analysis
stop_words = set(stopwords.words('english'))
stop_words |= {'.',',','!','?'}

#import the model and the keras_tokenizer
import app

#predict sentiment and confidence of the review
def predictSentiment(review):
    review = np.array([review])
    review = app.keras_tokenizer.texts_to_sequences(review)
    review = sequence.pad_sequences(review, maxlen=app.maxlen)
    labels = ['Neutral','Positive','Negative']
    pred = app.sentiment_model.predict(review)
    sentiment_tone = labels[np.argmax(pred[0])]
    sentiment_confidence = pred[0][np.argmax(pred[0])] * 100
    return(sentiment_tone,round(sentiment_confidence,2))

#predict sentiment and confidence of the review
def predictSuggestions(review):
    review = np.array([review])
    review = app.keras_tokenizer.texts_to_sequences(review)
    review = sequence.pad_sequences(review, maxlen=app.maxlen)
    labels = ['absent','present']
    pred = app.suggestions_model.predict(review)
    suggestions = labels[1 if pred[0] > 0.25 else 0]
    suggestions_chances = pred[0][0] * 100
    return(suggestions,round(suggestions_chances,2))

#predict volume metrics of the review
def predictVolume(review):
    #tokenize the review using NLTK tokenizer
    tokens = treebank_tokenizer.tokenize(review)
    total_volume = len(tokens)
    #remove all the stopwords
    non_stop_words = [word for word in tokens if word not in stop_words]
    volume_without_stopwords = len(non_stop_words)
    return (total_volume,volume_without_stopwords)
