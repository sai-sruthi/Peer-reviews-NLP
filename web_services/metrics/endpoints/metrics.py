
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
def allJson():
    review_text = processJsonRequest()
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
            'Problem': problem
        }
        output.append(result)
    return jsonify({'reviews': output})


# route to get only volume metrics via JSON request
@app.route('/volume', methods=['POST'])
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
def sentimentJson():
    review_list = processJsonRequest()
    sentiment_output = []
    for review in review_list:
        sentiment_tone, sentiment_score = predictSentiment(review['text'])
        sentiment_result = {'id': review['id'], 'text': review['text'], 'sentiment_tone': sentiment_tone,
                            'sentiment_score': sentiment_score}
        sentiment_output.append(sentiment_result)
    return renderJsonResponse(sentiment_output)


# route to get only emotion metrics via JSON request
@app.route('/emotions', methods=['POST'])
def emotionsJson():
    review_list = processJsonRequest()
    emotions_output = []
    for review in review_list:
        praise, criticism = predictEmotion(review['text'])
        result = {'id': review['id'], 'text': review['text'], 'Praise': praise, 'Criticism': criticism}
        emotions_output.append(result)
    return renderJsonResponse(emotions_output)


# route to get only suggestion metrics via JSON request
@app.route('/suggestions', methods=['POST'])
def suggestionsJson():
    review_list = processJsonRequest()
    suggestions_output = []
    for review in review_list:
        suggestions = predictSuggestions(review['text'])
        suggestions_result = {'id': review['id'], "text": review['text'], "suggestions": suggestions}
        suggestions_output.append(suggestions_result)
    return renderJsonResponse(suggestions_output)


@app.route('/problem', methods=['POST'])
def problemJson():
    review_list = processJsonRequest()
    problem_output = []
    for review in review_list:
        problem = predictProblem(review['text'])
        problem_result = {'id': review['id'], 'text': review['text'], "problems": problem}
        problem_output.append(problem_result)
    return renderJsonResponse(problem_output)
