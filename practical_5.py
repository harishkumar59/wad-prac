from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Initialize stop words and stemmer
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Retrieve webpage content
url = 'https://www.yahoo.com/?guccounter=1'
headers = {'User-Agent': 'Mozilla/5.0'} # Added user-agent to prevent getting blocked by Yahoo
response = requests.get(url, headers=headers)

# Parse HTML and extract meta tags
soup = BeautifulSoup(response.content, 'html.parser')
meta_tags = soup.find_all('meta')

# Extract meta information
title = ''
description = '' # Fixed typo here
keywords = []

for tag in meta_tags:
    if tag.get('property') == 'og:title':
        title = tag.get('content')
        
    if tag.get('property') == 'og:description':
        description = tag.get('content') # Fixed typo here
        
    if tag.get('name') == 'keywords':
        keywords = tag.get('content')

# Preprocess content
content = soup.get_text()
tokens = word_tokenize(content)
filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
preprocessed_content = ' '.join(stemmed_tokens)

# Print results
print('Title:', title, '\n')
print('Description:', description, '\n') # Fixed typo here
print('Keywords:', keywords, '\n')
print('Preprocessed content:', preprocessed_content[0:100], '\n') # Fixed /n to \n