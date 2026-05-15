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
    You are an expert product cataloger and technical writer. I have identified a product from an image and gathered supplementary research from the web.
    
    Vision Analysis (Primary Identification):
    - Brand: {vision_data.brand}
    - Model: {vision_data.model_name}
    - Category: {vision_data.category}
    - Visual Features: {', '.join(vision_data.visual_features)}
    
    Web Research Content (Source Materials):
    {research_context if research_context else "No web research available."}
    
    Task:
    Synthesize all the information above into a professional, highly-detailed product profile.
    
    Requirements:
    1. **Official Description**: Write a cohesive, marketing-ready description (2-4 paragraphs) based on the web research. If no research is found, describe it based on visual features.
    2. **Technical Specifications**: Extract EVERY technical detail found in the research (e.g., Battery Life, Connectivity, Dimensions, Weight, Materials, Features). If no research is available, list specs that are visually obvious.
    3. **Accuracy**: Prioritize data from official product pages or reputable tech review sites found in the research context.
    4. **Formatting**: Ensure the output strictly follows the provided JSON schema.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",

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
