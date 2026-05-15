import os
import argparse
import json
from dotenv import load_dotenv
from .vision import identify_product
from .research import perform_research
from .synthesis import synthesize_product_data

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Visual Product Cataloging Agent")
    parser.add_argument("image_path", help="Path to the product image file")
    args = parser.parse_args()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    
    if not gemini_api_key or not firecrawl_api_key:
        print("Error: Please set GEMINI_API_KEY and FIRECRAWL_API_KEY in your .env file.")
        return

    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found: {args.image_path}")
        return

    try:
        print(f"--- Phase 1: Visual Identification ---")
        vision_data = identify_product(args.image_path, gemini_api_key)
        print(f"Identified: {vision_data.brand} {vision_data.model_name}")
        
        print(f"\n--- Phase 2: Web Research ---")
        research_results = perform_research(vision_data.search_query, firecrawl_api_key)
        print(f"Gathered data from {len(research_results)} sources.")
        
        print(f"\n--- Phase 3: Data Synthesis ---")
        final_catalog_entry = synthesize_product_data(vision_data, research_results, gemini_api_key)
        
        print(f"\n--- Final Results ---")
        print(final_catalog_entry.model_dump_json(indent=2))
        
        # Save to file
        safe_brand = "".join(c for c in vision_data.brand if c.isalnum())
        safe_model = "".join(c for c in vision_data.model_name if c.isalnum())
        output_filename = f"product_{safe_brand}_{safe_model}.json".lower()
        
        with open(output_filename, "w") as f:
            f.write(final_catalog_entry.model_dump_json(indent=2))
        print(f"\nResults saved to {output_filename}")

    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
