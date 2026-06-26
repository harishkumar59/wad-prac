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