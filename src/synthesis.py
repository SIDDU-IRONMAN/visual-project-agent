from typing import Dict
from google import genai
from google.genai import types
from .models import ProductCatalogEntry
from .vision import VisionIdentification
from .utils import get_logger, SynthesisError

logger = get_logger(__name__)

def synthesize_product_data(
    vision_data: VisionIdentification, 
    research_results: Dict[str, str], 
    api_key: str
) -> ProductCatalogEntry:
    """
    Combines visual identification data and web research content into a structured ProductCatalogEntry.
    """
    logger.info(f"Synthesizing data for {vision_data.brand} {vision_data.model_name}")
    client = genai.Client(api_key=api_key)
    
    research_context = ""
    for url, content in research_results.items():
        truncated_content = content[:10000] 
        research_context += f"Source: {url}\n\n{truncated_content}\n\n---\n\n"
        
    prompt = f"""
    You are an expert product cataloger. I have identified a product from an image and gathered supplementary research from the web.
    
    Vision Analysis:
    - Brand: {vision_data.brand}
    - Model: {vision_data.model_name}
    - Category: {vision_data.category}
    - Visual Features: {', '.join(vision_data.visual_features)}
    
    Web Research Content:
    {research_context if research_context else "No web research available."}
    
    Task:
    Synthesize all the information above into a comprehensive, structured product profile.
    - Use the vision data for initial context and visual feature validation.
    - Use the web research to find official descriptions, technical specifications, and estimated pricing.
    - If specifications conflict, prioritize information from official-looking source URLs.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProductCatalogEntry
            )
        )
        
        final_entry = response.parsed
        
        # Post-processing for completeness
        if not final_entry.source_urls:
            final_entry.source_urls = list(research_results.keys())
        
        if not final_entry.brand:
            final_entry.brand = vision_data.brand
        if not final_entry.model_name:
            final_entry.model_name = vision_data.model_name
            
        logger.info("Successfully synthesized product profile.")
        return final_entry
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        raise SynthesisError(f"Data synthesis failed: {e}")
