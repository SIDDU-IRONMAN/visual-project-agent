from firecrawl import FirecrawlApp
from typing import List, Dict

def perform_research(query: str, api_key: str) -> Dict[str, str]:
    """
    Uses Firecrawl to search for a product and scrape the top results for specifications.
    Returns a dictionary mapping URLs to their markdown content.
    """
    app = FirecrawlApp(api_key=api_key)
    
    # Perform search to find relevant product pages
    print(f"Searching for: {query}...")
    search_result = app.search(query, params={"limit": 2})
    
    if not search_result or 'data' not in search_result:
        print("No search results found.")
        return {}
    
    results = {}
    for item in search_result['data']:
        url = item.get('url')
        if url:
            print(f"Scraping: {url}...")
            try:
                scrape_result = app.scrape_url(url, params={"formats": ["markdown"]})
                if scrape_result and 'markdown' in scrape_result:
                    results[url] = scrape_result['markdown']
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                
    return results
