# Peer-reviews-NLP
Perform Sentiment,  Volume and Emotion Analysis using NLP on peer reviews.

# Try out a live prototype of this application:
# https://expertiza-peer-reviews.herokuapp.com/
# Note: This is just a prototype and the current UI is for demo purposes only and the final UI will be different.

# This application also has API endpoints for each of it's metrics and can be used as below:
This accepts input text in JSON format and returns all the metrics or a particular individual metrics as desired

# Here are the various endpoints and url for JSON request:
https://expertiza-peer-reviews.herokuapp.com/all for all the metrics at once
https://expertiza-peer-reviews.herokuapp.com/volume for all the volume metrics only
https://expertiza-peer-reviews.herokuapp.com/sentiment for all the sentiment metrics only
https://expertiza-peer-reviews.herokuapp.com/emotion for all the emotion metrics only
https://expertiza-peer-reviews.herokuapp.com/remarks for indentifying level of praise and criticism

# Input text is to be given in the following JSON format:
{
	"text" : "This is an excellent project. Keep up the great work"
            }

