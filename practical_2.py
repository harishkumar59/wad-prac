#CREATE VIRTUAL ENVIRONMENT (OPTIONAL)
#python -m venv .venv
#.venv\Scripts\activate.bat



#pip install requests beautifulsoup4

#python filename





import requests
from bs4 import BeautifulSoup

# URL of Times of India Maharashtra news page
url = "https://timesofindia.indiatimes.com/india/maharashtra"

try:
    # Send request to website
    response = requests.get(url)

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all headlines
    headlines = soup.find_all("span", class_="w_tle")

    print("----- Latest Maharashtra News Headlines -----\n")

    # Loop through headlines
    for headline in headlines:
        text = headline.text.strip()

        # Find link inside headline
        a_tag = headline.find("a")

        if a_tag:
            link = "https://timesofindia.indiatimes.com" + a_tag.get("href")

            print("Headline :", text)
            print("Link     :", link)
            print()

except Exception as e:
    print("Error:", e)
