#Sentiment analysis for reviews by customers and visualize the same.

# pip install pandas matplotlib textblob vaderSentiment



import pandas as pd
from textblob import TextBlob

# read in the customer_reviews.csv file as a Pandas dataframe
reviews_df = pd.read_csv('customer_reviews.csv')

# create a new column in the dataframe to hold the sentiment polarity score for each review
reviews_df['sentiment_score'] = reviews_df['review_text'].apply(lambda x: TextBlob(x).sentiment.polarity)

# categorize the sentiment scores into positive, negative, and neutral
reviews_df['sentiment_category'] = reviews_df['sentiment_score'].apply(lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral')

# print out the count of reviews in each sentiment category for each product
for product_id in reviews_df['product_id'].unique():
    product_reviews_df = reviews_df[reviews_df['product_id'] == product_id]
    print('Product', product_id)
    print('Positive reviews:', len(product_reviews_df[product_reviews_df['sentiment_category'] == 'positive']))
    print('Negative reviews:', len(product_reviews_df[product_reviews_df['sentiment_category'] == 'negative']))
    print('Neutral reviews:', len(product_reviews_df[product_reviews_df['sentiment_category'] == 'neutral']))
    print()
