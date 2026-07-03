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