import os
from flask import Flask, request, render_template, flash, jsonify
# import predict functions:
from preprocessing.predict import predictVolume, predictSentiment, predictSuggestions, predictEmotion, predictProblem
#from  frontend.displayFile import displayMetrics 
#from endpoints.metrics import Metrics
from flasgger import Swagger
from flasgger.utils import swag_from

# simple flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '10cr441f27d441f28567d441f2b2018j'
app.config["SWAGGER"] = {"title": "Swagger - UI", "universion": 2}

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint" : "All",
            "route" : "/",
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route" : "/swagger/",
}
swagger = Swagger(app, config = swagger_config)


@app.route('/', methods=['GET', 'POST'])
# render the web application page and all it's fields
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


# Returns text from API request
def returnReviewText():
    review_json = request.get_json()
    review_text = review_json['reviews']
    return review_text


# Check for valid API request and return
def processJsonRequest():
    if not request.is_json:
        return 'Error : Request is not in JSON format'
    return returnReviewText()


def renderJsonResponse(output):
    return jsonify({'reviews': output})


# route to get all metrics via JSON request
@app.route('/all', methods=['POST'])
@swag_from('documentation/all_endpoints.yml')
def allJson():
    review_text = processJsonRequest()
    output = []
    for reviews in review_text:
        total_volume, volume_without_stopwords = predictVolume(reviews['text'])
        sentiment_tone, sentiment_score, sentiment_confidence = predictSentiment(reviews['text'])
        suggestions, suggestion_confidence = predictSuggestions(reviews['text'])
        praise, criticism, emotion_confidence = predictEmotion(reviews['text'])
        problem, problem_confidence = predictProblem(reviews['text'])
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
            'Problem': problem,
            'Confidence': {
                "Sentiment" : sentiment_confidence, 
                "Suggestions" : suggestion_confidence,
                "Emotion" : emotion_confidence,
                "Problem" : problem_confidence
            }
        }
        output.append(result)
    return jsonify({'reviews': output})


# route to get only volume metrics via JSON request
@app.route('/volume', methods=['POST'])
@swag_from('documentation/volume.yml')
def volumeJson():
    review_list = processJsonRequest()
    volume_output = []
    for review in review_list:
        total_volume, volume_without_stopwords = predictVolume(review['text'])
        reviews_output = {'id': review['id'], 'text': review['text'], 'total_volume': total_volume,
                        'volume_without_stopwords': volume_without_stopwords}
        volume_output.append(reviews_output)
    return renderJsonResponse(volume_output)


# route to get only sentiment metrics via JSON request
@app.route('/sentiment', methods=['POST'])
@swag_from('documentation/sentiments.yml')
def sentimentJson():
    review_list = processJsonRequest()
    sentiment_output = []
    for review in review_list:
        sentiment_tone, sentiment_score,confidence = predictSentiment(review['text'])
        sentiment_result = {'id': review['id'], 'text': review['text'], 'sentiment_tone': sentiment_tone,
                            'sentiment_score': sentiment_score,"confidence":confidence}
        sentiment_output.append(sentiment_result)
    return renderJsonResponse(sentiment_output)


# route to get only emotion metrics via JSON request
@app.route('/emotions', methods=['POST'])
@swag_from('documentation/emotions.yml')
def emotionsJson():
    review_list = processJsonRequest()
    emotions_output = []
    for review in review_list:
        praise, criticism,confidence = predictEmotion(review['text'])
        result = {'id': review['id'], 'text': review['text'], 'Praise': praise, 'Criticism': criticism,"confidence":confidence}
        emotions_output.append(result)
    return renderJsonResponse(emotions_output)


# route to get only suggestion metrics via JSON request
@app.route('/suggestions', methods=['POST'])
@swag_from('documentation/suggestions.yml')
def suggestionsJson():
    review_list = processJsonRequest()
    suggestions_output = []
    for review in review_list:
        suggestions,confidence = predictSuggestions(review['text'])
        suggestions_result = {'id': review['id'], "text": review['text'], "suggestions": suggestions,"confidence":confidence}
        suggestions_output.append(suggestions_result)
    return renderJsonResponse(suggestions_output)


@app.route('/problem', methods=['POST'])
@swag_from('documentation/problems.yml')
def problemJson():
    review_list = processJsonRequest()
    problem_output = []
    for review in review_list:
        problem,confidence = predictProblem(review['text'])
        problem_result = {'id': review['id'], 'text': review['text'], "problems": problem,"confidence":confidence}
        problem_output.append(problem_result)
    return renderJsonResponse(problem_output)


if __name__ == '__main__':
    app.run(debug = True)
