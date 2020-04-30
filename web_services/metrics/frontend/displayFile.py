# app routes
# default web application app route


# display all the required metrics on the web application
def displayMetrics(review):
    """
    Returns all the metrics
    ---

    """
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
