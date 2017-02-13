from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
import nltk
from nltk.tokenize import TweetTokenizer

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        positives = open("positive-words.txt", "r")
        self.positives = list(positives)
        del self.positives[0:35]
        
        negatives = open("negative-words.txt", "r")
        self.negatives = negatives.readlines()
        del self.negatives[0:35]
        
        # Close the files 
        positives.close()
        negatives.close()
        
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        total_words = len(text)
        
        negatives_length = len(self.negatives)
        positives_length = len(self.positives)
        
        posneg_sum = 0
        
        for word in text:
            
            for j in range(0, positives_length):
                if word == self.positives[j][:-1]:
                    posneg_sum += 1
            
            for k in range(0, negatives_length):
                if word == self.negatives[k][:-1]:
                    posneg_sum -= 1

        return posneg_sum


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)

    # TODO
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    
    # find out hte number of tweets
    number_of_tweets = len(tweets)

    # break the tweets up
    tokenizer = TweetTokenizer()
    
    positive_sum = 0
    negative_sum = 0
    
    #for each tweet and all of it's individual tokens, add that to a list of tokens
    # analyze user's tweets
    for i in range(0, number_of_tweets):
        single_tweet = tokenizer.tokenize(tweets[i])
        pos_or_neg = analyzer.analyze(single_tweet)
        
        if pos_or_neg > 0:
            positive_sum += 1
        elif pos_or_neg < 0:
            negative_sum += 1

    positive = round(positive_sum / number_of_tweets * 100, 1)
    negative = round(negative_sum / number_of_tweets * 100, 1)
    neutral = 100.0 - (positive + negative)
    
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
