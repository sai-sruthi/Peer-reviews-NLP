# python and keras imports
import numpy as np
from keras.preprocessing import sequence, text
from preprocessing.suggestions_and_problem_preprocessing import predict_class

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Google cloud imports
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Import nltk libraries for volume analysis
from nltk.tokenize import TreebankWordTokenizer

treebank_tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords

# set rules for stopwords ignored in volume analysis
stop_words = set(stopwords.words('english'))
stop_words |= {'.', ',', '!', '?'}


# predict sentiment tone and score of the review
def predictSentiment(review):
    client = language.LanguageServiceClient()
    document = types.Document(content=review, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    predicted_confidence = 0
    if sentiment.score > 0.25:
        predicted_confidence = 1
        sentiment_tone = "Positive"

    elif sentiment.score < -0.25:
        sentiment_tone = "Negative"

    else:
        if sentiment.magnitude < 0.6:
            sentiment_tone = "Neutral"
        else:
            sentiment_tone = "Mixed"
    return sentiment_tone, round(sentiment.score, 3), predicted_confidence

# predict model metrics of the review
def predictMetric(review, model, tokenizer):
    output = []
    predicted_comment, predicted_confidence = predict_class(review['text'], model, tokenizer, 200)
    if predicted_comment == 1:
        metric_value = "Present"
    else:
        metric_value = "Absent"
        predicted_confidence = 1 - predicted_confidence
    return metric_value, predicted_confidence

# predict volume metrics of the review
def predictVolume(review):
    # tokenize the review using NLTK tokenizer
    tokens = treebank_tokenizer.tokenize(review)
    total_volume = len(tokens)
    # remove all the stopwords
    non_stop_words = [word for word in tokens if word not in stop_words]
    volume_without_stopwords = len(non_stop_words)
    return (total_volume, volume_without_stopwords)


# predict presence of praise and or criticism in the review
def predictEmotion(review):
    client = language.LanguageServiceClient()
    document = types.Document(content=review, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    praise = criticism = "None"
    predicted_confidence = 0

    if 0.6 <= sentiment.magnitude < 1.5:
        if sentiment.score > 0.25:
            praise = "Low"
        elif sentiment.score < -0.25:
            criticism = "Low"
        else:
            praise = criticism = "Low"

    elif sentiment.magnitude >= 1.5:
        if sentiment.score > 0.25:
            predicted_confidence = 1
            praise = "High"
        elif sentiment.score < -0.25:
            criticism = "High"
        else:
            predicted_confidence = 1
            praise = criticism = "High"

    return praise, criticism, predicted_confidence

