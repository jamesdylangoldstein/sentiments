import nltk
from collections import deque

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
        
        positives.close()
        negatives.close()
        
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        sentiment_sum = 0
        
        negatives_length = len(self.negatives)
        positives_length = len(self.positives)
        
        for word in text:
            
            for j in range(0, positives_length):
                if word == self.positives[j][:-1]:
                    sentiment_sum += 1
            
            for k in range(0, negatives_length):
                if word == self.negatives[k][:-1]:
                    sentiment_sum -= 1

        return sentiment_sum
