#flask imports
from flask import Flask,request,render_template, flash,jsonify

#Google cloud imports
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#python imports
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

#Import nltk libraries for volume analysis
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords

#set rules for stopwords ignored in volume analysis
stop_words = set(stopwords.words('english'))
stop_words |= {'.',',','!','?'}

#simple flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '10cr441f27d441f28567d441f2b2018j'

#app routes
#default web application app route
@app.route('/', methods=['GET', 'POST'])
#render the web application page and all it's fields
def renderPage():
    input_text = "Enter Review Text Here!"
    # Normal page load calls 'GET'. 'POST' gets called when one of the buttons is pressed
    if request.method == 'POST':
        # Check which button was pressed
        if request.form['submit'] == 'Analyze':
            input_text = request.form.get("text")
            displayMetrics(input_text)
        elif request.form['submit'] == 'Clear':
            input_text = ''

    # Render the HTML template. input_text gets fed into the textarea variable in the template
    return render_template('form.html', textarea=input_text)

#display all the required metrics on the web application
def displayMetrics(input_text):
    displayVolume(input_text)
    displaySentiment(input_text)
    displayEmotion(input_text)
    displayRemarks(input_text)

#create a sentiment object with all the raw scores
def detectSentiment(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment

#perform sentiment analysis and return sentiment metrics
def sentimentAnalysis(input_text):
    sentiment = detectSentiment(input_text)
    if sentiment.score > 0.25:
        sentiment_tone = "Positive"
    elif sentiment.score < -0.25:
        sentiment_tone = "Negative"
    else:
        if sentiment.magnitude < 0.6:
            sentiment_tone = "Neutral"
        else:
            sentiment_tone = "Mixed"
    return (sentiment_tone,round(sentiment.score,3))

#perform emotion analysis and return emotion metrics
def emotionAnalysis(input_text):
    sentiment = detectSentiment(input_text)
    if sentiment.magnitude < 0.6:
        emotion_level = "Low"
    elif sentiment.magnitude > 1.5:
        emotion_level = "High"
    else:
        emotion_level = "Medium"
    return (round(sentiment.magnitude,3),emotion_level)

def checkRemarks(input_text):
    sentiment = detectSentiment(input_text)
    praise = criticism = "None"
    if sentiment.magnitude >= 0.6 and sentiment.magnitude < 1.5:
        if sentiment.score > 0.25:
            praise = "Low"
        elif sentiment.score < -0.25:
            criticism = "Low"
        else:
            praise = criticism = "Low"
    elif sentiment.magnitude >= 1.5:
        if sentiment.score > 0.25:
            praise = "High"
        elif sentiment.score < -0.25:
            criticism = "High"
        else:
            praise = criticism = "High"
    return (praise,criticism)

#Perform volume analysis on the review text
def volumeAnalysis(text):
    #tokenize the review
    tokens = tokenizer.tokenize(text)
    total_volume = len(tokens)

    #remove all the stopwords
    non_stop_words = [word for word in tokens if word not in stop_words]
    volume_without_stopwords = len(non_stop_words)
    return (total_volume,volume_without_stopwords)

#Display all the volume metrics on the screen in the web application
def displayVolume(input_text):
    total_volume,volume_without_stopwords = volumeAnalysis(input_text)
    flash('Review text: {}'.format(input_text))
    flash('\n')
    flash('Volume Metrics')
    flash('Total volume of the review: {}'.format(total_volume))
    flash('Actual useful volume of the review: {}'.format(volume_without_stopwords))
    flash('\n')

#Display all the sentiment metrics on the screen in the web application
def displaySentiment(input_text):
    sentiment_tone,sentiment_score = sentimentAnalysis(input_text)
    flash('Sentiment metrics')
    flash('Sentiment tone : {}'.format(sentiment_tone))
    flash('Sentiment score : {}'.format(sentiment_score))
    flash('\n')

#display emotion level and score
def displayEmotion(input_text):
    sentiment_magnitude,emotion_level = emotionAnalysis(input_text)
    flash('Emotion metrics')
    flash('Emotion score : {}'.format(sentiment_magnitude))
    flash('Emotion level : {}'.format(emotion_level))
    flash('\n')

#display presence of praise and criticism
def displayRemarks(input_text):
    praise,criticism = checkRemarks(input_text)
    flash('Praise and criticism remarks')
    flash('Praise : {}'.format(praise))
    flash('Criticism : {}'.format(criticism))

#route to get all metrics via JSON request
@app.route('/all', methods = ['POST'])
def allJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    total_volume,volume_without_stopwords = volumeAnalysis(review_text)
    sentiment_tone,sentiment_score = sentimentAnalysis(review_text)
    sentiment_magnitude,emotion_level = emotionAnalysis(review_text)
    praise,criticism = checkRemarks(review_text)
    return jsonify({'text':review_text,'total_volume':total_volume,'useful_volume':volume_without_stopwords,'sentiment_tone':sentiment_tone,'sentiment_score':sentiment_score,'emotion_score':sentiment_magnitude,'emotion_level':emotion_level,'praise':praise,'criticism':criticism})

#route to get only volume metrics via JSON request
@app.route('/volume', methods = ['POST'])
def volumeJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    total_volume,volume_without_stopwords = volumeAnalysis(review_text)
    return jsonify({'text':review_text,'total_volume':total_volume,'useful_volume':volume_without_stopwords})

#route to get only sentiment metrics via JSON request
@app.route('/sentiment', methods = ['POST'])
def sentimentJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    sentiment_tone,sentiment_score = sentimentAnalysis(review_text)
    return jsonify({'text':review_text,'sentiment_tone':sentiment_tone,'sentiment_score':sentiment_score})

#route to get only emotion metrics via JSON request
@app.route('/emotion', methods = ['POST'])
def emotionJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    sentiment_magnitude,emotion_level = emotionAnalysis(review_text)
    return jsonify({'text':review_text,'emotion_score':sentiment_magnitude,'emotion_level':emotion_level})

#route to get only praise and criticism remarks via JSON request
@app.route('/remarks', methods = ['POST'])
def remarksJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    praise,criticism = checkRemarks(review_text)
    return jsonify({'text':review_text,'praise':praise,'criticism':criticism})

if __name__ == '__main__':
    app.run()
