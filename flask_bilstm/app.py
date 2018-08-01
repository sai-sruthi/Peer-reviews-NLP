#flask imports
from flask import Flask,request,render_template, flash,jsonify

#import load and predict functions:
from initialize import loadModel
from predict import predictVolume,predictSentiment

#simple flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '10cr441f27d441f28567d441f2b2018j'

#app routes
#default web application app route
@app.route('/', methods=['GET', 'POST'])
#render the web application page and all it's fields
def renderPage():
    review = "Enter Review Text Here!"
    # Normal page load calls 'GET'. 'POST' gets called when one of the buttons is pressed
    if request.method == 'POST':
        # Check which button was pressed
        if request.form['submit'] == 'Analyze':
            review = request.form.get("text")
            displayMetrics(review)
        elif request.form['submit'] == 'Clear':
            review = ''

    # Render the HTML template. review gets fed into the textarea variable in the template
    return render_template('form.html', textarea=review)

#display all the required metrics on the web application
def displayMetrics(review):
    displayVolume(review)
    displaySentiment(review)

#Display all the volume metrics on the screen in the web application
def displayVolume(review):
    total_volume,volume_without_stopwords = predictVolume(review)
    flash('Review text: {}'.format(review))
    flash('\n')
    flash('Volume Metrics')
    flash('Total volume of the review: {}'.format(total_volume))
    flash('Actual useful volume of the review: {}'.format(volume_without_stopwords))
    flash('\n')

#Display all the sentiment metrics on the screen in the web application
def displaySentiment(review):
    sentiment_tone,sentiment_confidence = predictSentiment(review)
    flash('Sentiment metrics')
    flash('Sentiment tone : {}'.format(sentiment_tone))
    flash('Sentiment confidence : {}'.format(sentiment_confidence))
    flash('\n')

#route to get all metrics via JSON request
@app.route('/all', methods = ['POST'])
def allJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    total_volume,volume_without_stopwords = predictVolume(review_text)
    sentiment_tone,sentiment_confidence = predictSentiment(review_text)
    return jsonify({'text':review_text,'total_volume':total_volume,'useful_volume':volume_without_stopwords,'sentiment_tone':sentiment_tone,'sentiment_confidence':sentiment_confidence})

#route to get only volume metrics via JSON request
@app.route('/volume', methods = ['POST'])
def volumeJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    total_volume,volume_without_stopwords = predictVolume(review_text)
    return jsonify({'text':review_text,'total_volume':total_volume,'useful_volume':volume_without_stopwords})

#route to get only sentiment metrics via JSON request
@app.route('/sentiment', methods = ['POST'])
def sentimentJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['text']
    sentiment_tone,sentiment_confidence = predictSentiment(review_text)
    return jsonify({'text':review_text,'sentiment_tone':sentiment_tone,'sentiment_confidence':sentiment_confidence})

if __name__ == '__main__':
    loadModel()
    app.run()
