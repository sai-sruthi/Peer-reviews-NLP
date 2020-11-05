import os
from flask import Flask, request, render_template, flash, jsonify
from preprocessing.predict import predictVolume, predictSentiment, predictEmotion, predictMetric
from preprocessing.suggestions_and_problem_preprocessing import load_items
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

model = os.path.abspath('.')  # path to locate the saved Machine Learning models
suggestions_model = model + "/model/suggestions_cnn_model.h5"
suggestions_tokenizer = model + "/model/suggestions_tokenizer"
problems_model = model + "/model/problems_cnn_model.h5"
problems_tokenizer = model + "/model/problems_tokenizer"

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
    suggestions_model, suggestions_tokenizer = load_items(suggestions_model, suggestions_tokenizer)
    problems_model, problems_tokenizer = load_items(problems_model, problems_tokenizer)  
    for reviews in review_text:
        total_volume, volume_without_stopwords = predictVolume(reviews['text'])
        sentiment_tone, sentiment_score, sentiment_confidence = predictSentiment(reviews['text'])
        suggestions, suggestion_confidence = predictMetric(reviews['text'], suggestions_model, suggestions_tokenizer)
        praise, criticism, emotion_confidence = predictEmotion(reviews['text'])
        problem, problem_confidence = predictMetric(reviews['text'], problems_model, problems_tokenizer)
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
        }
        output.append(result)
    return jsonify({'reviews': output})

# route to get all confidence metrics via JSON request
@app.route('/all_confidence', methods=['POST'])
@swag_from('documentation/all_endpoints.yml')
def allConfidenceJson():
    review_text = processJsonRequest()
    output = []
    suggestions_model, suggestions_tokenizer = load_items(suggestions_model, suggestions_tokenizer)
    problems_model, problems_tokenizer = load_items(problems_model, problems_tokenizer)
    for reviews in review_text:
        sentiment_tone, sentiment_score, sentiment_confidence = predictSentiment(reviews['text'])
        suggestions, suggestion_confidence = predictMetric(reviews['text'], suggestions_model, suggestions_tokenizer)
        praise, criticism, emotion_confidence = predictEmotion(reviews['text'])
        problem, problem_confidence = predictMetric(reviews['text'], problems_model, problems_tokenizer)
        result = {
            'id': reviews['id'],
            'text': reviews['text'],
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
        sentiment_tone, sentiment_score, confidence = predictSentiment(review['text'])
        sentiment_result = {'id': review['id'], 'text': review['text'], 'sentiment_tone': sentiment_tone,
                            'sentiment_score': sentiment_score}
        sentiment_output.append(sentiment_result)
    return renderJsonResponse(sentiment_output)

# route to get only sentiment confidence metrics via JSON request
@app.route('/sentiment_confidence', methods=['POST'])
@swag_from('documentation/sentiments.yml')
def sentimentConfidenceJson():
    review_list = processJsonRequest()
    sentiment_confidence_output = []
    for review in review_list:
        sentiment_tone, sentiment_score, confidence = predictSentiment(review['text'])
        sentiment_result = {'id': review['id'], 'text': review['text'],"confidence":confidence}
        sentiment_confidence_output.append(sentiment_result)
    return renderJsonResponse(sentiment_confidence_output)


# route to get only emotion metrics via JSON request
@app.route('/emotions', methods=['POST'])
@swag_from('documentation/emotions.yml')
def emotionsJson():
    review_list = processJsonRequest()
    emotions_output = []
    for review in review_list:
        praise, criticism, confidence = predictEmotion(review['text'])
        result = {'id': review['id'], 'text': review['text'], 'Praise': praise, 'Criticism': criticism}
        emotions_output.append(result)
    return renderJsonResponse(emotions_output)

# route to get only emotion confidence metrics via JSON request
@app.route('/emotions_confidence', methods=['POST'])
@swag_from('documentation/emotions.yml')
def emotionsConfidenceJson():
    review_list = processJsonRequest()
    emotions_confidence_output = []
    for review in review_list:
        praise, criticism, confidence = predictEmotion(review['text'])
        result = {'id': review['id'], 'text': review['text'],"confidence":confidence}
        emotions_confidence_output.append(result)
    return renderJsonResponse(emotions_confidence_output)


# route to get only suggestion metrics via JSON request
@app.route('/suggestions', methods=['POST'])
@swag_from('documentation/suggestions.yml')
def suggestionsJson():
    review_list = processJsonRequest()
    suggestions_output = []
    suggestions_model, suggestions_tokenizer = load_items(suggestions_model, suggestions_tokenizer)
    for review in review_list:
        suggestions, confidence = predictMetric(review['text'],suggestions_model, suggestions_tokenizer)
        suggestions_result = {'id': review['id'], "text": review['text'], "suggestions": suggestions}
        suggestions_output.append(suggestions_result)
    return renderJsonResponse(suggestions_output)

# route to get only suggestion metrics via JSON request
@app.route('/suggestions_confidence', methods=['POST'])
@swag_from('documentation/suggestions.yml')
def suggestionsConfidenceJson():
    review_list = processJsonRequest()
    suggestions_confidence_output = []
    suggestions_model, suggestions_tokenizer = load_items(suggestions_model, suggestions_tokenizer)
    for review in review_list:
        suggestions, confidence = predictMetric(review['text'],suggestions_model, suggestions_tokenizer)
        suggestions_result = {'id': review['id'], "text": review['text'],"confidence":confidence}
        suggestions_confidence_output.append(suggestions_result)
    return renderJsonResponse(suggestions_confidence_output)

# route to get only problem metrics via JSON request
@app.route('/problem', methods=['POST'])
@swag_from('documentation/problems.yml')
def problemJson():
    review_list = processJsonRequest()
    problem_output = []
    problems_model, problems_tokenizer = load_items(problems_model, problems_tokenizer)
    for review in review_list:
        problem, confidence = predictMetric(review['text'], problems_model, problems_tokenizer)
        problem_result = {'id': review['id'], 'text': review['text'], "problems": problem}
        problem_output.append(problem_result)
    return renderJsonResponse(problem_output)

# route to get only problem confidence metrics via JSON request
@app.route('/problem_confidence', methods=['POST'])
@swag_from('documentation/problems.yml')
def problemConfidenceJson():
    review_list = processJsonRequest()
    problem_confidence_output = []
    problems_model, problems_tokenizer = load_items(problems_model, problems_tokenizer)
    for review in review_list:
        problem, confidence = predictMetric(review['text'], problems_model, problems_tokenizer)
        problem_result = {'id': review['id'], 'text': review['text'],"confidence":confidence}
        problem_confidence_output.append(problem_result)
    return renderJsonResponse(problem_confidence_output)


if __name__ == '__main__':
    app.run(debug = True)
