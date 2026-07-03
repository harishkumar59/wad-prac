# Sentiment Analysis for Customer Reviews and Visualization

# Import necessary libraries
# pip install textblob
# pip install vaderSentiment

import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load customer reviews dataset
reviews_df = pd.read_csv("customer_reviews.csv")

# Create VADER analyzer object
analyzer = SentimentIntensityAnalyzer()

# Function to calculate TextBlob sentiment
def get_textblob_sentiment(review):
    return TextBlob(review).sentiment.polarity

# Function to calculate VADER sentiment
def get_vader_sentiment(review):
    return analyzer.polarity_scores(review)["compound"]

# Apply sentiment analysis
reviews_df["TextBlob_Sentiment"] = reviews_df["review_text"].apply(get_textblob_sentiment)
reviews_df["Vader_Sentiment"] = reviews_df["review_text"].apply(get_vader_sentiment)

# Categorize TextBlob sentiment scores
def sentiment_category(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

reviews_df["Sentiment_Category"] = reviews_df["TextBlob_Sentiment"].apply(sentiment_category)

# Display sentiment count for each product
print("Sentiment Analysis by Product - practical_10.1.py:42")
print("" * 40)

for product_id in reviews_df["product_id"].unique():
    product_reviews = reviews_df[reviews_df["product_id"] == product_id]

    print("Product: - practical_10.1.py:48", product_id)
    print("Positive Reviews: - practical_10.1.py:49", len(product_reviews[product_reviews["Sentiment_Category"] == "Positive"]))
    print("Negative Reviews: - practical_10.1.py:50", len(product_reviews[product_reviews["Sentiment_Category"] == "Negative"]))
    print("Neutral Reviews : - practical_10.1.py:51", len(product_reviews[product_reviews["Sentiment_Category"] == "Neutral"]))
    print()

# ---------------- Visualization ----------------

# Box Plot for sentiment scores
plt.figure(figsize=(8,5))

plt.boxplot([
    reviews_df["TextBlob_Sentiment"],
    reviews_df["Vader_Sentiment"]
])

plt.xticks([1, 2], ["TextBlob", "VADER"])
plt.title("Customer Review Sentiment Scores")
plt.ylabel("Sentiment Score")
plt.grid(True)

plt.show()

# Bar Chart for sentiment categories
sentiment_counts = reviews_df["Sentiment_Category"].value_counts()

plt.figure(figsize=(6,5))
plt.bar(sentiment_counts.index, sentiment_counts.values)

plt.title("Customer Review Sentiment Categories")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.grid(axis="y")

plt.show()