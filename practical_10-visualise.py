#Sentiment analysis for reviews by customers and visualize the same.

#pip install pandas matplotlib textblob vaderSentiment




# Import necessary libraries
#pip install textblob
#pip install vaderSentiment
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load customer reviews into a dataframe
reviews_df = pd.read_csv('customer_reviews.csv')

# Define functions for sentiment analysis using TextBlob and VaderSentiment
def get_textblob_sentiment(review):
    return TextBlob(review).sentiment.polarity

def get_vader_sentiment(review):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(review)['compound']

# Apply sentiment analysis functions to customer reviews dataframe
reviews_df['TextBlob_Sentiment'] = reviews_df['review_text'].apply(get_textblob_sentiment)
reviews_df['Vader_Sentiment'] = reviews_df['review_text'].apply(get_vader_sentiment)

# Visualize sentiment analysis results using a box plot
plt.boxplot([reviews_df['TextBlob_Sentiment'], reviews_df['Vader_Sentiment']])
plt.xticks([1, 2], ['TextBlob', 'Vader'])
plt.ylabel('Sentiment Score')
plt.title('Customer Review Sentiment Analysis')
plt.show()
