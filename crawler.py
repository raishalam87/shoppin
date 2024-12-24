import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawler.utils import extract_product_urls, fetch_page
from crawler.settings import USER_AGENT

# List of domains to crawl
domains = ["http://example1.com", "http://example2.com", "http://example3.com"]

# Function to extract product URLs from a page
def extract_product_urls_from_page(page_url, html_content):
    product_urls = set()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Regex pattern to identify product URLs
    product_pattern = re.compile(r'/product/[A-Za-z0-9-]+')
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if product_pattern.search(href):
            full_url = urljoin(page_url, href)
            product_urls.add(full_url)
    
    return product_urls

# Async function to fetch and parse a page
async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

# Function to crawl a single domain
async def crawl_domain(domain, session):
    print(f"Crawling {domain}")
    discovered_urls = set()
    try:
        homepage = await fetch_page(session, domain)
        product_urls = extract_product_urls_from_page(domain, homepage)
        discovered_urls.update(product_urls)
        
        # Handle pagination (simplified example)
        # Check for a 'Next' page and recursively fetch it
        
    except Exception as e:
        print(f"Error crawling {domain}: {e}")
    
    return domain, discovered_urls

# Main crawl function to handle multiple domains asynchronously
async def crawl_domains(domains):
    async with aiohttp.ClientSession() as session:
        tasks = [crawl_domain(domain, session) for domain in domains]
        results = await asyncio.gather(*tasks)
    
    # Store the results (mapping domains to their product URLs)
    product_data = {domain: urls for domain, urls in results}
    
    return product_data

# Start crawling
async def main():
    product_data = await crawl_domains(domains)
    # Save the output to a file
    with open('output/product_urls.json', 'w') as f:
        json.dump(product_data, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())