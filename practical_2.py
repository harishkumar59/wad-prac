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