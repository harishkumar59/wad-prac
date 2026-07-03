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
