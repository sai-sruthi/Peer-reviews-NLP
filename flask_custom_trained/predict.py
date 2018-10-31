#python and keras imports
import numpy as np
from keras.preprocessing import sequence,text
np.random.seed(7)
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

#Google cloud imports
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Import nltk libraries for volume analysis
from nltk.tokenize import TreebankWordTokenizer
treebank_tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords

#set rules for stopwords ignored in volume analysis
stop_words = set(stopwords.words('english'))
stop_words |= {'.',',','!','?'}

#import the model and the keras_tokenizer
import app

#predict sentiment tone and score of the review
def predictSentiment(review):
    client = language.LanguageServiceClient()
    document = types.Document(content=review, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    if sentiment.score > 0.25:
        sentiment_tone = "Positive"
    elif sentiment.score < -0.25:
        sentiment_tone = "Negative"
    else:
        if sentiment.magnitude < 0.6:
            sentiment_tone = "Neutral"
        else:
            sentiment_tone = "Mixed"
    return(sentiment_tone,round(sentiment.score,3))

#predict presence and chances of suggestions in the review
def predictSuggestions(review):
    review = np.array([review])
    review = app.keras_tokenizer.texts_to_sequences(review)
    review = sequence.pad_sequences(review, maxlen=app.maxlen)
    labels = ['absent','present']
    pred = app.suggestions_model.predict(review)
    suggestions = labels[1 if pred[0] > 0.5 else 0]
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
