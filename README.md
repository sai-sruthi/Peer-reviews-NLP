# Peer-reviews-NLP
Perform Sentiment,  Volume and Emotion Analysis using NLP on peer reviews.

# Try out a live prototype of this application:
# https://expertiza-peer-reviews.herokuapp.com/
 Note: This is just a prototype and the current UI is for demo purposes only and the final UI will be different.

This application also has API endpoints for each of it's metrics and can be used as below:
This accepts input text in JSON format and returns all the metrics or a particular individual metrics as desired

# Here are the various endpoints and url for JSON request:
https://peerlogic.csc.ncsu.edu/all for all the metrics at once

https://peerlogic.csc.ncsu.edu/volume for all the volume metrics only

https://peerlogic.csc.ncsu.edu/sentiment for all the sentiment metrics only

https://peerlogic.csc.ncsu.edu/emotion for all the emotion metrics only

https://peerlogic.csc.ncsu.edu/remarks for identifying level of praise and criticism

https://peerlogic.csc.ncsu.edu/problem for problem detection only



# Input text is to be given in the following JSON format:
{
	"reviews": 
    [
        {
        "text" : "The project can be improved"
        },
        {
        "text" : "This is an excellent project. Keep up the great work"
        },
        {
        "text" : "I liked the way reviews are written"
        }
    ]
        {
        "text" : "This is an excellent project. Keep up the great work"
        }

# Output text will also be in JSON format. Here is an example sent to /all endpoint with the above input text:
{
    "reviews": [
        {
            "Criticism": "None",
            "Praise": "None",
            "Problem": "Present",
            "Sentiment_score": -0.2,
            "Sentiment_tone": "Neutral",
            "Suggestions": "Absent",
            "Total_volume": 6,
            "Volume_without_stopwords": 2,
            "text": "I do not like this."
        },
        {
            "Criticism": "None",
            "Praise": "None",
            "Problem": "Absent",
            "Sentiment_score": 0.0,
            "Sentiment_tone": "Neutral",
            "Suggestions": "Absent",
            "Total_volume": 2,
            "Volume_without_stopwords": 1,
            "text": " bull."
        },
        {
            "Criticism": "Low",
            "Praise": "None",
            "Problem": "Absent",
            "Sentiment_score": -0.8,
            "Sentiment_tone": "Negative",
            "Suggestions": "Absent",
            "Total_volume": 6,
            "Volume_without_stopwords": 3,
            "text": "I did not like the work"
        }
    ]
}
