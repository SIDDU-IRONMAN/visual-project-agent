from firecrawl import Firecrawl
from typing import List, Dict
from .utils import get_logger, ResearchError

logger = get_logger(__name__)

def perform_research(query: str, api_key: str) -> Dict[str, str]:
    """
    Uses Firecrawl to search for a product and scrape the top results for specifications.
    Returns a dictionary mapping URLs to their markdown content.
    """
    logger.info(f"Initiating research for query: {query}")
    app = Firecrawl(api_key=api_key)
    
    try:
        response = app.search(
            query, 
            limit=3, 
            scrape_options={"formats": ["markdown"]}
        )
        # In v2, search might return a list, dict, or SearchData object
        logger.info(f"Firecrawl raw response type: {type(response)}")
        search_results = response
        if hasattr(response, 'data'):
            logger.info("Response has 'data' attribute.")
            search_results = response.data
        elif isinstance(response, dict) and 'data' in response:
            logger.info("Response is dict with 'data' key.")
            search_results = response['data']
        elif isinstance(response, tuple):
            logger.info("Response is tuple.")
            search_results = response[0]
            if hasattr(search_results, 'data'):
                search_results = search_results.data
            elif isinstance(search_results, dict) and 'data' in search_results:
                search_results = search_results.get('data')

        # If it's still an object (SearchData), try to convert to list
        if not isinstance(search_results, list) and hasattr(search_results, '__iter__'):
             logger.info("Converting search_results to list.")
             search_results = list(search_results)

        if not search_results or not isinstance(search_results, list):
            logger.warning(f"No valid search results found. Final search_results type: {type(search_results)}")
            return {}
        
        logger.info(f"Processing {len(search_results)} search results.")
        results = {}
        for i, item in enumerate(search_results):
            # Handle both dicts and objects returned by SDK
            url = None
            markdown = None
            
            if isinstance(item, dict):
                url = item.get('url')
                markdown = item.get('markdown')
            else:
                url = getattr(item, 'url', None)
                markdown = getattr(item, 'markdown', None)
            
            # If markdown is still none, check if it's in a 'data' attribute of the item
            if not markdown and hasattr(item, 'data') and isinstance(item.data, dict):
                markdown = item.data.get('markdown')
            
            logger.info(f"Result {i}: URL={url}, MarkdownPresent={bool(markdown)}")
            
            if url and markdown:
                logger.info(f"Collected technical data from: {url}")
                results[url] = markdown
            elif url:
                logger.warning(f"Result from {url} missing markdown content.")

                    
        return results
    except Exception as e:
        logger.error(f"Firecrawl research failed: {e}")
        raise ResearchError(f"Research failed: {e}")
