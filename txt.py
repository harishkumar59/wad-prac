# -------------------practical 1 ---------------
#Scrape an online E-Commerce Site for Data.
# 1. Extract product data from Amazon - be it any product and put these details in
# the MySQL database. One can use pipeline. Like 1 pipeline to process the
# scraped data and other to put data in the database and since Amazon has some
# restrictions on scraping of data, ask them to work on small set of requests
# otherwise proxies and all would have to be used.
# 2. Scrape the details like color, dimensions, material etc. Or customer ratings by
# features



# pip install requests beautifulsoup4 mysql-connector-python








from bs4 import BeautifulSoup
import requests
import mysql.connector

# ---------------- MYSQL CONNECTION ----------------
mydb = mysql.connector.connect(
    host="localhost",
    user="harish",
    password="mypassword",
    database="ecommerce",
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

choice = 'y'

while choice.lower() == 'y':

    try:
        # ---------------- INPUT URL ----------------
        URL = input("Enter Amazon Product URL:\n")

        # ---------------- HEADERS ----------------
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        # ---------------- REQUEST PAGE ----------------
        page = requests.get(URL, headers=headers)

        # ---------------- PARSE HTML ----------------
        soup = BeautifulSoup(page.content, "html.parser")

        # ---------------- PRODUCT TITLE ----------------
        title = soup.find(id='productTitle')

        if title:
            title = title.get_text().strip()
        else:
            title = "Not Available"

        # ---------------- PRICE ----------------
        price = soup.find('span', class_='a-price-whole')

        if price:
            price = price.get_text().strip()

            # Remove commas, dots, spaces
            price = price.replace(",", "")
            price = price.replace(".", "")
            price = price.replace(" ", "")

        else:
            price = "0"

        # ---------------- RATING ----------------
        rating = soup.find('span', class_='a-icon-alt')

        if rating:
            rating = rating.get_text().strip()
        else:
            rating = "No Rating"

        # ---------------- EXTRA DETAILS ----------------
        color = "Not Available"
        material = "Not Available"
        dimensions = "Not Available"

        details = soup.find_all('tr')

        for row in details:

            text = row.get_text().lower()

            if "color" in text:
                color = row.get_text().strip()

            if "material" in text:
                material = row.get_text().strip()

            if "dimensions" in text:
                dimensions = row.get_text().strip()

        # ---------------- INSERT INTO DATABASE ----------------
        sql = """
        INSERT INTO products
        (name, price, rating, color, material, dimensions)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            title[:255],
            int(price),
            rating,
            color,
            material,
            dimensions
        )

        mycursor.execute(sql, values)

        mydb.commit()

        # ---------------- OUTPUT ----------------
        print("\nData Stored Successfully!\n")

        print("Product Name :", title)
        print("Price        :", price)
        print("Rating       :", rating)
        print("Color        :", color)
        print("Material     :", material)
        print("Dimensions   :", dimensions)

    except Exception as e:
        print("Error occurred:", e)

    finally:
        choice = input("\nDo you want to scrape another product? (y/n): ")

# ---------------- CLOSE DATABASE ----------------
mydb.close()










# -------------------practical 2 ---------------
#Scrape an online Social Media Site for Data. Use python to scrape information from twitter.

#CREATE VIRTUAL ENVIRONMENT (OPTIONAL)
#python -m venv .venv
#.venv\Scripts\activate.bat



# pip install requests beautifulsoup4 lxml



import requests
from bs4 import BeautifulSoup

# URL of Times of India Maharashtra page
url = "https://timesofindia.indiatimes.com/india/maharashtra"

# Browser headers
headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Send request
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    print("----- Latest Maharashtra News Headlines -----\n")

    headlines = set()

    # Find all article links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)

        if "/articleshow/" in href and text:
            if href.startswith("/"):
                href = "https://timesofindia.indiatimes.com" + href

            if (text, href) not in headlines:
                headlines.add((text, href))

    if headlines:
        for i, (title, link) in enumerate(headlines, start=1):
            print(f"{i}. {title}")
            print("Link:", link)
            print()
    else:
        print("No headlines found. The website may have changed its structure.")

except requests.exceptions.RequestException as e:
    print("Request Error:", e)

except Exception as e:
    print("Error:", e)





# -------------------practical 3 ---------------
#Page Rank for link analysis using python Create a small set of pages namely page1, page2, page3 and page4 apply random walk on the same


#pip install networkx numpy scipy

#create virtual environment 




import networkx as nx

# Create Directed Graph
G = nx.DiGraph()

# Add pages (nodes)
G.add_nodes_from(['page1', 'page2', 'page3', 'page4'])

# Add links between pages (edges)
G.add_edges_from([
    ('page1', 'page2'),
    ('page1', 'page3'),
    ('page2', 'page3'),
    ('page3', 'page1'),
    ('page3', 'page4'),
    ('page4', 'page2')
])

# Calculate PageRank
pr = nx.pagerank(G, alpha=0.85)

# Random Walk probabilities
rw = nx.pagerank(G)

# Print Random Walk probabilities
print("Random Walk Probabilities:")
print("Page1 =", rw['page1'])
print("Page2 =", rw['page2'])
print("Page3 =", rw['page3'])
print("Page4 =", rw['page4'])

# Print PageRank values
print("\nPageRank Values:")
print("Page1 =", pr['page1'])
print("Page2 =", pr['page2'])
print("Page3 =", pr['page3'])
print("Page4 =", pr['page4'])





# -------------------practical 4 ---------------
#Perform Spam Classifier



#pip install pandas scikit-learn
#make sure you have csv file



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
spam_df = pd.read_csv('spam_data.csv', encoding='latin-1')

# Display first few rows
print(spam_df.head())

# Split data into input and output
X = spam_df['text']
y = spam_df['label']

# Training and Testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Convert text into numerical vectors
vectorizer = CountVectorizer()

X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Train model
clf = MultinomialNB()
clf.fit(X_train_vect, y_train)

# Model Accuracy
accuracy = clf.score(X_test_vect, y_test)

print("Accuracy: {:.2f}%".format(accuracy * 100))

# Testing with new message
new_message = [input("Enter your message:\n")]

new_message_vect = vectorizer.transform(new_message)

prediction = clf.predict(new_message_vect)

# Output result
if prediction[0] == "spam":
    print("The message is SPAM")
else:
    print("The message is GENUINE")


# -------------------practical 5 ---------------
#Demonstrate Text Mining and Webpage Pre-processing using meta information from the web pages (Local/Online).

#pip install requests beautifulsoup4 nltk && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')”



from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download NLTK resources (run once)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Initialize stop words and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Retrieve webpage content
url = "https://www.yahoo.com/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.content, "html.parser")
meta_tags = soup.find_all("meta")

# Extract meta information
title = ""
description = ""
keywords = ""

for tag in meta_tags:
    if tag.get("property") == "og:title":
        title = tag.get("content")

    if tag.get("property") == "og:description":
        description = tag.get("content")

    if tag.get("name") == "keywords":
        keywords = tag.get("content")

# Preprocess content
content = soup.get_text()

tokens = word_tokenize(content)
filtered_tokens = [
    token.lower()
    for token in tokens
    if token.isalpha() and token.lower() not in stop_words
]

stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
preprocessed_content = " ".join(stemmed_tokens)

# Print results
print("Title:", title)
print("\nDescription:", description)
print("\nKeywords:", keywords)
print("\nPreprocessed content:")
print(preprocessed_content[:500])

# -------------------practical 6 ---------------
# Apriori Algorithm implementation in case study.


#pip install pandas mlxtend


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Example dataset
dataset = [['bread', 'milk', 'eggs'],
           ['bread', 'diapers', 'beer', 'eggs'],
           ['milk', 'diapers', 'beer', 'cola'],
           ['bread', 'milk', 'diapers', 'beer', 'cola'],
           ['bread', 'milk', 'diapers', 'beer']]

# Convert the dataset to a one-hot encoded matrix
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)

# Optimization: Explicitly cast to bool to prevent future Pandas/Mlxtend warnings
df = pd.DataFrame(te_ary, columns=te.columns_).astype(bool)

# Apply the Apriori algorithm to generate frequent itemsets
frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)

# Print the frequent itemsets
print(frequent_itemsets)

# -------------------practical 7 ---------------

# Develop a basic crawler for the web search for user defined keywords.


# pip install requests beautifulsoup4



import requests
from bs4 import BeautifulSoup

def web_crawler(url, keywords):
    # Setup headers so websites don't block you as a robotic script
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Make a request to the URL
        response = requests.get(url, headers=headers, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the text on the page
            page_text = soup.get_text()

            print("\n--- Search Results ---")
            # Check if any of the keywords are present on the page
            for keyword in keywords:
                if keyword.lower() in page_text.lower():
                    print(f"✅ '{keyword}' found on {url}")
                else:
                    print(f"❌ '{keyword}' NOT found on {url}")
        else:
            print(f'Request failed with status code {response.status_code}')
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Fixed: Use input() to actually let the user type the URL
url = input("Enter the URL to be searched (e.g., https://en.wikipedia.org/wiki/Web_crawler): ")

keywords = []
print("\nEnter the keywords to be searched:")
while True:
    k = input("Enter the keyword: ")
    if k.strip():  # Avoid adding empty spaces
        keywords.append(k)
    
    # Safer exit condition using strings instead of dangerous integer casting
    x = input("Enter '1' to add more keywords, or '0' to finish: ")
    if x == '0':
        break

# Run the crawler
web_crawler(url, keywords)




# -------------------practical 8 ---------------
# Develop a focused crawler for local search.

# pip install requests beautifulsoup4

import requests

def local_crawler(city, amenity):

    bbox = {
        "mumbai": "18.89,72.77,19.30,73.00",
        "pune": "18.45,73.75,18.65,73.98",
        "delhi": "28.50,76.90,28.90,77.40"
    }

    city = city.lower()

    if city not in bbox:
        print("City not available.")
        return

    query = f"""
    [out:json][timeout:25];
    node["amenity"="{amenity}"]({bbox[city]});
    out body;
    """

    url = "https://overpass.kumi.systems/api/interpreter"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(
            url,
            data={"data": query},
            headers=headers,
            timeout=30
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        if not data["elements"]:
            print("No results found.")
            return

        print("\nSearch Results\n")

        for i, place in enumerate(data["elements"][:10], 1):
            tags = place.get("tags", {})
            print(f"{i}. {tags.get('name','Unknown')}")
            print("Latitude :", place["lat"])
            print("Longitude:", place["lon"])
            print("-"*40)

    except Exception as e:
        print("Error:", e)


city = input("Enter City: ")
amenity = input("Enter Amenity (hospital/school/bank/pharmacy/restaurant): ")

local_crawler(city, amenity)




# -------------------practical 9 ---------------
# Develop a programme for deep search implementation to detect plagiarism in documents online.


# pip install requests beautifulsoup4 nltk

# Import Required Libraries
import requests
from bs4 import BeautifulSoup
import difflib
import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
# Collect Data from User
text = input("Enter Text to Check for Plagiarism: ")

# Text Preprocessing

stop_words = set(nltk.corpus.stopwords.words('english'))
tokens = nltk.word_tokenize(text)
tokens = [token.lower() for token in tokens if token.isalpha()]
tokens = [token for token in tokens if token not in stop_words]

# Scrape Web for Similar Text
url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
soup_text = soup.get_text()
soup_tokens = nltk.word_tokenize(soup_text)
soup_tokens = [token.lower() for token in soup_tokens if token.isalpha()]
soup_tokens = [token for token in soup_tokens if token not in stop_words]
# Calculate Similarity
similarity = difflib.SequenceMatcher(None, tokens, soup_tokens).ratio()

# Set Threshold for Plagiarism
threshold = 0.002
print(similarity)
# Plagiarism Detection
if similarity >= threshold:
    print("Text is Plagiarized.")
else:
    print("Text is Not Plagiarized.")


# -------------------practical 10 a(visualise)---------------
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


# -------------------practical 10 b---------------
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

