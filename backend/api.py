import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import the existing agent logic
from src.vision import identify_product
from src.research import perform_research
from src.synthesis import synthesize_product_data

load_dotenv()

app = FastAPI(title="Visual Product Agent API")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/api/analyze-product")
async def analyze_product(file: UploadFile = File(...)):
    # 1. Validate File Type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # 2. Check API Keys
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not gemini_api_key or not firecrawl_api_key:
        raise HTTPException(status_code=500, detail="API keys not configured on server.")

    # 3. Save file temporarily and check size
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_extension = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_extension}"
    temp_path = os.path.join(temp_dir, temp_filename)

    try:
        size = 0
        with open(temp_path, "wb") as buffer:
            while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                size += len(content)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File too large. Maximum 10MB.")
                buffer.write(content)
        
        # 4. Run the Agent Pipeline
        # Phase 1: Vision
        vision_data = identify_product(temp_path, gemini_api_key)
        
        # Phase 2: Research
        research_results = perform_research(vision_data.search_query, firecrawl_api_key)
        
        # Phase 3: Synthesis
        final_catalog_entry = synthesize_product_data(vision_data, research_results, gemini_api_key)
        
        return final_catalog_entry

    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 5. Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
