from typing import List, Optional
from pydantic import BaseModel, Field

class ProductSpecification(BaseModel):
    label: str = Field(..., description="The name of the specification (e.g., 'Weight', 'Battery Life')")
    value: str = Field(..., description="The value of the specification")

class ProductCatalogEntry(BaseModel):
    brand: str = Field(..., description="The brand or manufacturer of the product")
    model_name: str = Field(..., description="The specific model name or number")
    category: str = Field(..., description="The product category (e.g., Electronics, Footwear)")
    official_description: Optional[str] = Field(None, description="Detailed description found from official sources")
    visual_features: List[str] = Field(default_factory=list, description="Key visual characteristics identified from the image")
    specifications: List[ProductSpecification] = Field(default_factory=list, description="Technical specifications extracted from research")
    estimated_retail_value_range: Optional[str] = Field(None, description="Estimated market value (e.g., '$299 - $349')")
    currency: str = Field(default="INR", description="Currency used for value range")
    source_urls: List[str] = Field(default_factory=list, description="URLs where product information was gathered")
