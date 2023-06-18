import requests
from bs4 import BeautifulSoup
import time

# URL of the website to scrape
url = 'https://www.investopedia.com/top-stocks-june-2023-7505936'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

time.sleep(2)  # Pause for 2 seconds between requests
response = requests.get(url, headers=headers)


print(response.content)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the text elements you want to extract (h tags, p tags, span tags, li tags, div tags, etc.)
links = soup.find_all('a')

# Extract the text from the elements and concatenate them into a single string
for link in links:
    print(link.text)

