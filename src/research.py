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
            limit=2, 
            scrape_options={"formats": ["markdown"]}
        )
        
        # Support various response formats from Firecrawl v2
        search_results = response
        if hasattr(response, 'data'):
            search_results = response.data
        elif isinstance(response, dict) and 'data' in response:
            search_results = response['data']
        elif isinstance(response, tuple):
            search_results = response[0]
            if hasattr(search_results, 'data'):
                search_results = search_results.data
            elif isinstance(search_results, dict) and 'data' in search_results:
                search_results = search_results['data']
        
        if not search_results or not isinstance(search_results, list):
            logger.warning(f"No research results found for query: {query}")
            return {}
        
        results = {}
        for item in search_results:
            if not isinstance(item, dict):
                continue
            url = item.get('url')
            markdown = item.get('markdown')
            if url and markdown:
                logger.info(f"Retrieved content from: {url}")
                results[url] = markdown
                    
        return results
    except Exception as e:
        logger.error(f"Firecrawl research failed: {e}")
        raise ResearchError(f"Research failed: {e}")
