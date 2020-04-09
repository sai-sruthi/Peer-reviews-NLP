# flask imports
from flask import Flask, request, render_template, flash, jsonify

# import predict functions:
from predict import predictVolume, predictSentiment, predictSuggestions, predictEmotion, predictProblem
import os

# simple flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '10cr441f27d441f28567d441f2b2018j'



# app routes
# default web application app route
@app.route('/', methods=['GET', 'POST'])
# render the web application page and all it's fields
def renderPage():
    review = "Enter Review Text Here!"
    # Normal page load calls 'GET'. 'POST' gets called when one of the buttons is pressed
    if request.method == 'POST':
        # Check which button was pressed
        if request.form['submit'] == 'Analyze':
            review = request.form.get("text")
            print(review)
            displayMetrics(review)
        elif request.form['submit'] == 'Clear':
            review = ''

    # Render the HTML template. review gets fed into the textarea variable in the template
    return render_template('form.html', textarea=review)


# display all the required metrics on the web application
def displayMetrics(review):
    displayVolume(review)
    displaySentiment(review)
    displaySuggestions(review)
    displayEmotion(review)
    displayProblem(review)
    


# Display all the volume metrics on the screen in the web application
def displayVolume(review):
    total_volume, volume_without_stopwords = predictVolume(review)
    flash('Review text: {}'.format(review))
    flash('\n')
    flash('Volume Metrics')
    flash('Total volume of the review: {}'.format(total_volume))
    flash('Actual useful volume of the review without any stop words: {}'.format(volume_without_stopwords))
    flash('\n')


# Display all the sentiment metrics on the screen in the web application
def displaySentiment(review):
    sentiment_tone, sentiment_score = predictSentiment(review)
    flash('Sentiment metrics')
    flash('Sentiment tone : {}'.format(sentiment_tone))
    flash('Sentiment score : {}'.format(sentiment_score))
    flash('\n')


# Display all the suggestion metrics on the screen in the web application
def displaySuggestions(review):
    suggestions = predictSuggestions(review)
    flash('Suggestion metrics')
    flash('In this review, suggestions are {}'.format(suggestions))
    flash('\n')


# Display presence of praise and criticism
def displayEmotion(review):
    praise, criticism = predictEmotion(review)
    flash('Praise and criticism metrics')
    flash('Praise : {}'.format(praise))
    flash('Criticism : {}'.format(criticism))
    flash('\n')

def displayProblem(review):
    problem = predictProblem(review)
    flash('Problem detection metrics')
    flash('In this review, problems are {}'.format(problem))


# route to get all metrics via JSON request
@app.route('/all', methods=['POST'])
def allJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        total_volume, volume_without_stopwords = predictVolume(reviews['text'])
        sentiment_tone, sentiment_score = predictSentiment(reviews['text'])
        suggestions = predictSuggestions(reviews['text'])
        praise, criticism = predictEmotion(reviews['text'])
        problem = predictProblem(reviews['text'])
        result = {
            'id': reviews['id'],
            'text': reviews['text'], 
            'Total_volume': total_volume, 
            'Volume_without_stopwords': volume_without_stopwords,
            'Sentiment_tone': sentiment_tone, 
            'Sentiment_score': sentiment_score, 
            'Suggestions': suggestions,
            'Praise': praise, 
            'Criticism': criticism,
            'Problem': problem }
        output.append(result)   
    return jsonify ({'reviews':output})



# route to get only volume metrics via JSON request
@app.route('/volume', methods=['POST'])
def volumeJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        total_volume, volume_without_stopwords = predictVolume(reviews['text'])
        result = {'id': reviews['id'],'text': reviews['text'], 'total_volume': total_volume, 'volume_without_stopwords': volume_without_stopwords}
        output.append(result)
    return jsonify ({'reviews':output})
    


# route to get only sentiment metrics via JSON request
@app.route('/sentiment', methods=['POST'])
def sentimentJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        sentiment_tone, sentiment_score = predictSentiment(reviews['text'])
        result = {'id': reviews['id'],'text': reviews['text'], 'sentiment_tone': sentiment_tone, 'sentiment_score': sentiment_score}
        output.append(result)
    return jsonify ({'reviews':output})
    


# route to get only emotion metrics via JSON request
@app.route('/emotions', methods=['POST'])
def emotionsJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        praise, criticism = predictEmotion(reviews['text'])
        result = {'id': reviews['id'],'text': reviews['text'], 'Praise': praise, 'Criticism': criticism}
        output.append(result)
    return jsonify ({'reviews':output})


# route to get only suggestion metrics via JSON request
@app.route('/suggestions', methods=['POST'])
def suggestionsJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        suggestions = predictSuggestions(reviews['text'])
        result = { 'id': reviews['id'],"text": reviews['text'],"suggestions" : suggestions}
        output.append(result)
    return jsonify({'reviews':output})

@app.route('/problem', methods=['POST'])
def problemJson():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    review_json = request.get_json()
    review_text = review_json['reviews']
    output = []
    for reviews in review_text:
        problem = predictProblem(reviews['text'])
        result = { 'id': reviews['id'],'text': reviews['text'], "problems": problem}
        output.append(result)
    return jsonify({'reviews':output})


if __name__ == '__main__':
    app.run()
