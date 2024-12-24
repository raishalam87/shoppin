import re
from urllib.parse import urljoin
from requests.exceptions import RequestException
import requests

# Function to extract product URLs from HTML content
def extract_product_urls(page_url, html_content):
    product_urls = set()
    pattern = re.compile(r'/product/[A-Za-z0-9-]+')
    
    # Parse HTML content and extract all anchor tags
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        if pattern.search(href):
            full_url = urljoin(page_url, href)
            product_urls.add(full_url)
    
    return product_urls

# Function to make an HTTP request with retries
def fetch_page(url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except RequestException as e:
        if retries > 0:
            print(f"Retrying {url}...")
            return fetch_page(url, retries-1)
        else:
            print(f"Failed to fetch {url}: {e}")
            return None