from flask import Flask,request,render_template, flash

#Google cloud imports
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Import nltk libraries
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words |= {'.',',','!','?'}

#simple flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '10cr441f27d441f28567d441f2b2018j'


@app.route('/', methods=['GET', 'POST'])
def load_page():
    input_text = "Enter Review Text Here!"
    # Normal page load calls 'GET'. 'POST' gets called when one of the buttons is pressed
    if request.method == 'POST':
        # Check which button was pressed
        if request.form['submit'] == 'Analyze':
            input_text = request.form.get("text")
            volume(input_text)
            sentiment_analysis(input_text)


        elif request.form['submit'] == 'Clear':
            input_text = ''

    # Render the HTML template. input_text gets fed into the textarea variable in the template
    return render_template('form.html', textarea=input_text)

def sentiment_analysis(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    if sentiment.score > 0.25:
        sentiment_tone = "Positive"
    elif sentiment.score < -0.25:
        sentiment_tone = "Negative"
    else:
        if sentiment.magnitude < 1:
            sentiment_tone = "Neutral"
        else:
            sentiment_tone = "Mixed"

    #determine emotion level and presence of strong content
    strong_content = "None"
    if sentiment.magnitude < 0.7:
        emotion_level = "Low"
    elif sentiment.magnitude > 1.6:
        if sentiment_tone == "Positive":
            strong_content = "Strong praise"
        elif sentiment_tone == "Negative":
            strong_content = "Strong criticism"
        else:
            strong_content = "Strong praise and criticism"
        emotion_level = "High"
    else:
        emotion_level = "Medium"

    flash('Sentiment metrics')
    flash('Sentiment tone : {}'.format(sentiment_tone))
    flash('Sentiment score : {}'.format(sentiment.score))
    flash('\n')
    flash('Emotion metrics')
    flash('Emotion score : {}'.format(sentiment.magnitude))
    flash('Emotion level : {}'.format(emotion_level))
    flash('Presence of strong content : {}'.format(strong_content))

def volume(text):
    #tokenize the review
    tokens = tokenizer.tokenize(text)
    total_volume = len(tokens)

    #remove all the stopwords
    non_stop_words = [word for word in tokens if word not in stop_words]
    volume_without_stopwords = len(non_stop_words)

    flash('Review text: {}'.format(text))
    flash('\n')
    flash('Volume Metrics')
    flash('Total volume of the review: {}'.format(total_volume))
    flash('Actual useful volume of the review: {}'.format(volume_without_stopwords))
    flash('\n')


if __name__ == '__main__':
    app.run()
