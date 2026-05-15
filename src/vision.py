from typing import List
from pydantic import BaseModel
from google import genai
from google.genai import types
from .utils import get_logger, VisionError

logger = get_logger(__name__)

class VisionIdentification(BaseModel):
    brand: str
    model_name: str
    category: str
    visual_features: List[str]
    search_query: str

def get_vision_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)

def identify_product(image_path: str, api_key: str) -> VisionIdentification:
    """
    Analyzes an image using Gemini Vision to identify the product and its features.
    """
    logger.info(f"Analyzing image: {image_path}")
    client = get_vision_client(api_key)
    
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except Exception as e:
        logger.error(f"Failed to read image file: {e}")
        raise VisionError(f"Could not read image file: {e}")
    
    mime_type = "image/jpeg"
    if image_path.lower().endswith(".png"):
        mime_type = "image/png"
    elif image_path.lower().endswith(".webp"):
        mime_type = "image/webp"

    prompt = """
    Analyze the provided image and identify the product precisely. 
    Focus on brand logos, model numbers, and unique design characteristics.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",

            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VisionIdentification,
            )
        )
        return response.parsed
    except Exception as e:
        logger.error(f"Gemini Vision API call failed: {e}")
        raise VisionError(f"Vision analysis failed: {e}")
