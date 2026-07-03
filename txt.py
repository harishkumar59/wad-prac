# -------------------practical 1 ---------------
#Scrape an online E-Commerce Site for Data.
# 1. Extract product data from Amazon - be it any product and put these details in
# the MySQL database. One can use pipeline. Like 1 pipeline to process the
# scraped data and other to put data in the database and since Amazon has some
# restrictions on scraping of data, ask them to work on small set of requests
# otherwise proxies and all would have to be used.
# 2. Scrape the details like color, dimensions, material etc. Or customer ratings by
# features



"""
This practical focuses on web scraping an e-commerce platform like Amazon to extract structured product data.
 The Python script utilizes the Requests library to send HTTP requests with modified User-Agent headers to bypass basic bot-detection,
 and BeautifulSoup to parse the HTML and locate specific elements like product titles, prices, ratings, and specifications using their tags and classes. Once the unstructured web data is extracted and cleaned, it is passed through a pipeline that connects to a local MySQL database via mysql-connector-python. The script dynamically inserts these details into a database table using structured SQL queries, demonstrating a complete pipeline from raw web extraction to persistent database storage.
"""



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


"""
This practical demonstrates how to scrape a news website, specifically the Times of India Maharashtra page, using Python. It uses the Requests library to download the web page source code and BeautifulSoup to traverse the document object model (DOM). The script targets anchor tags with a specific URL pattern containing article IDs to extract live news headlines and their corresponding hyperlinks dynamically. By implementing a Python set data structure, the program automatically filters out duplicate entries to ensure a unique list of fresh headlines, showcasing a foundational approach to building real-time data feeds from media sites.
"""

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



"""
This practical implements the PageRank algorithm and the Random Walk model to analyze link structures in a web graph. Using the NetworkX library, a directed graph is constructed with four custom nodes representing web pages and defined directed edges representing hyperlinks between them. The script applies the PageRank algorithm, which uses a damping factor (alpha=0.85) to simulate a user randomly clicking links or jumping to a new page entirely. The output assigns numerical importance scores to each page based on its incoming and outgoing links, illustrating how modern search engines evaluate and rank web pages based on structural authority.
"""

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



"""
This practical involves building a text classification model to filter out spam messages from genuine ones. It reads a labeled CSV dataset using Pandas and splits the data into training and testing subsets to validate model performance. The script utilizes Scikit-Learn's CountVectorizer to convert raw text into a numerical matrix of token counts, a method known as the Bag-of-Words model. Finally, it trains a Multinomial Naive Bayes classifier on these vectors, which relies on word frequencies and probability to determine whether a newly input message is classified as "spam" or "genuine."
"""


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


"""
This practical demonstrates web page preprocessing and text mining using metadata and raw webpage text content. The script uses Requests and BeautifulSoup to fetch a page like Yahoo and extract specific metadata tags such as Open Graph titles, descriptions, and keywords which search engines use for indexing. It then extracts the visible body text and uses the Natural Language Toolkit (NLTK) to perform tokenization, converting text into individual words. It filters out non-alphabetic tokens and common stop words (like 'and', 'the'), and applies Porter Stemming to reduce words to their base root form, transforming messy web data into a clean, normalized format optimized for text analysis.
"""


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



"""
This practical implements the Apriori algorithm using the Mlxtend library to perform Market Basket Analysis on a transactional dataset. The dataset consists of lists of items bought together, which is converted into a one-hot encoded boolean matrix using a TransactionEncoder. The Apriori algorithm evaluates this matrix to identify frequent itemsets that meet a user-defined minimum support threshold of 60%. This practical demonstrates unsupervised learning used by retailers to find strong associations between items, helping businesses understand customer purchasing behavior for product placements and recommendations.
"""



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



"""
This practical covers the development of a basic web crawler designed to search for user-defined keywords on a specific live website. The script accepts a target URL and a dynamic list of search terms directly from the user, then uses Requests to pull the webpage content. BeautifulSoup parses the HTML to extract all visible text from the page. The program then converts both the web text and the user keywords to lowercase for an un-biased comparison, looping through the data to check for exact keyword matches, showing how search engine spiders index specific content.
"""

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

"""
This practical develops a focused or topical crawler designed to search for specific local amenities within designated geographical boundaries. Instead of crawling random links, it interacts directly with the Overpass API to query the OpenStreetMap crowd-sourced database. The script takes a city name and an amenity type (like a hospital or school) as input, maps the city to its precise latitude and longitude bounding box coordinates, and submits a structured Overpass QL query. The API returns a refined JSON payload containing names, precise coordinates, and metadata of matching local spots, demonstrating how location-based search applications operate.
"""

import requests

def local_crawler(location, amenity):

    if location.lower() != "mumbai":
        print("Currently only Mumbai is supported.")
        return

    query = f"""
    [out:json];
    node["amenity"="{amenity}"](18.89,72.77,19.27,72.99);
    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    headers = {
        "User-Agent": "Python Local Crawler"
    }

    response = requests.post(
        url,
        data={"data": query},
        headers=headers
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        if not data["elements"]:
            print("No results found.")
            return

        for i, place in enumerate(data["elements"], 1):
            print(i, place.get("tags", {}).get("name", "Unknown"))
            print(place["lat"], place["lon"])
            print()

    else:
        print(response.text)


city = input("Enter city: ")
amenity = input("Enter search (hospital/school/pharmacy/bank/restaurant): ")

local_crawler(city, amenity)


# -------------------practical 9 ---------------
# Develop a programme for deep search implementation to detect plagiarism in documents online.

"""
This practical builds a deep search plagiarism detection program that analyzes document similarity against online web resources. The user inputs a block of text, which is tokenized and stripped of stop words using NLTK to isolate the core vocabulary. The script then live-scrapes a reference web page, such as a Wikipedia article, and processes its text using the exact same pipeline. Finally, it uses Python’s difflib library to run a SequenceMatcher algorithm, calculating a ratio that measures the longest common subsequences. If this similarity score crosses a specified threshold, the system flags the user's document as plagiarized.
"""


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




# -------------------practical 10 ---------------
#Sentiment analysis for reviews by customers and visualize the same.

# pip install pandas matplotlib textblob vaderSentiment

"""
This practical focuses on analyzing and visualizing customer reviews using rule-based sentiment analysis tools. It reads text reviews from a CSV file using Pandas and passes them through two distinct NLP libraries: TextBlob and VADER (Valence Aware Dictionary and sEntiment Reasoner). Both libraries calculate a polarity score between -1 (highly negative) and +1 (highly positive), with VADER being specifically tuned for social media and informal review language. Finally, the script uses Matplotlib to generate a box plot comparing the distribution of scores across both analyzers, visualizing the overall customer sentiment trend.
This practical implements a targeted customer review sentiment classifier grouped by unique product identification numbers.
 It reads a dataset using Pandas and applies TextBlob to evaluate the text string of each review, assigning it a numerical
  
    polarity score. The script then applies a lambda function to categorize these raw scores into explicit buckets: 'positive' for scores above zero, 'negative' for scores below zero, and 'neutral' for exact zeros. Finally, it groups the data to print a clean statistical breakdown of positive, negative, and neutral feedback counts for each product ID, showcasing how businesses track satisfaction across specific inventory items.
"""
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