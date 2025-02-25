import os
import json
import random
import logging
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Set up logging configuration
logging.basicConfig(filename='scraper.log', level=logging.INFO)

# List of User-Agents for random selection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
]

# Function to log error messages
def log_error(message):
    logging.error(message)

# Function to log general info messages
def log_info(message):
    logging.info(message)

# Function to fetch page content asynchronously
async def fetch_page_async(url, cookies=None):
    """Async fetch page content."""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': random.choice(USER_AGENTS),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, cookies=cookies, headers=headers) as response:
                return await response.text()
    except Exception as e:
        log_error(f"Error fetching page {url}: {e}")
        return None

# Function to fetch article content and follow redirects if necessary
async def fetch_article_async(url, cookies=None):
    """Async fetch the content of a single article."""
    response = await fetch_page_async(url, cookies)
    if not response:
        return None
    
    # Parse the headers to follow redirects if needed
    soup = BeautifulSoup(response, 'html.parser')
    # You can add a check for 3xx HTTP codes and follow redirects here if necessary
    return soup

# Function to parse the archive page and extract article links
def parse_archive_page(html):
    """Parse the archive page to extract article links."""
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    
    for link in soup.find_all('a', {'data-testid': 'TitleLink'}):
        href = link.get('href')
        if href.startswith("/article/"):
            articles.append("https://www.reuters.com" + href)
    
    return articles

# Function to parse the article page and extract relevant information
def parse_article_page(soup):
    """Parse the article page and extract title, date, content, and tags."""
    title = soup.find('title').get_text(strip=True) if soup.find('title') else ""
    
    date_info = soup.find_all(class_='date-line__date___kNbY')
    date, time_, updated = [d.get_text(strip=True) for d in date_info[:3]] if len(date_info) >= 3 else ("", "", "")
    
    body = "".join([p.get_text(strip=True) for p in soup.find_all(class_='article-body__content__17Yit')])
    
    tags = [tag.get_text(strip=True) for tag in soup.find_all(attrs={'aria-label': 'Tags'})]

    log_info(f'Title={title}')
    return {
        "title": title,
        "date": date,
        "time": time_,
        "updated": updated,
        "body": body,
        "tags": tags
    }

# Function to save article content to a JSON file
def save_article(article, date_str):
    """Save the article data to a JSON file."""
    folder = f"articles/{date_str}"
    os.makedirs(folder, exist_ok=True)
    
    file_name = os.path.join(folder, f"{article['title'].replace('/', '_')}.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=4)

# Function to get cookies by visiting the archive page
async def get_cookies():
    """Fetch the archive page to obtain the cookies."""
    url = "https://www.reuters.com/archive/"
    html = await fetch_page_async(url)
    
    if not html:
        return None
    
    cookies = {}
    for line in html.split("\n"):
        if line.lower().startswith("set-cookie: "):
            cookie = line.split(": ", 1)[1].strip()
            key, value = cookie.split("=", 1)
            cookies[key] = value
    
    return cookies

# Main async function to start the process of scraping articles
async def main():
    base_url = "https://www.reuters.com/archive/{}/{}/{}/"
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 2)
    current_date = start_date
    cookies = await get_cookies()  # Get the initial cookies
    
    while current_date <= end_date:
        yyyy_mm = current_date.strftime("%Y-%m")
        dd = current_date.strftime("%d")
        page = 1
        
        while True:
            archive_url = base_url.format(yyyy_mm, dd, page)
            html = await fetch_page_async(archive_url, cookies)
            if not html:
                break
            
            article_links = parse_archive_page(html)
            if not article_links:
                break
            
            # Print out the current date, article URL, and title
            log_info(f"Date: {current_date.strftime('%Y-%m-%d')}")
            
            tasks = []
            for article_url in article_links:
                log_info(f"Article URL: {article_url}")
                tasks.append(fetch_article_async(article_url, cookies))
            
            # Wait for all article fetch tasks to finish
            article_htmls = await asyncio.gather(*tasks)
            
            for article_html in article_htmls:
                if article_html:
                    article_data = parse_article_page(article_html)
                    save_article(article_data, current_date.strftime("%Y%m%d"))
            
            page += 1
            await asyncio.sleep(random.uniform(5, 10))  # Randomized delay to avoid detection
        
        current_date += timedelta(days=1)
        cookies = await get_cookies()  # Update cookies every day

# Run the scraper
asyncio.run(main())
