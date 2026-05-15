import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import the existing agent logic and utilities
from src.vision import identify_product
from src.research import perform_research
from src.synthesis import synthesize_product_data
from src.utils import get_logger, AgentError
from src.models import ProductCatalogEntry

load_dotenv()

# Initialize logger
logger = get_logger("visual-agent-api")

app = FastAPI(title="Visual Product Agent API")

# Configure CORS for local development
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://0.0.0.0:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/api/analyze-product", response_model=ProductCatalogEntry)
async def analyze_product(file: UploadFile = File(...)):
    """
    Endpoint to upload an image and receive a structured product catalog entry.
    """
    logger.info(f"Received request to analyze: {file.filename} ({file.content_type})")
    
    # 1. Validate File Type
    if not file.content_type.startswith("image/"):
        logger.error(f"Invalid file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="File must be an image.")

    # 2. Check API Keys
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
    if not gemini_api_key or not firecrawl_api_key:
        logger.error("API keys missing from environment.")
        raise HTTPException(status_code=500, detail="Server configuration error: Missing API keys.")

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
                    logger.error(f"File size exceeded: {size} bytes")
                    raise HTTPException(status_code=413, detail="File too large. Maximum 10MB.")
                buffer.write(content)
        
        # 4. Run the Agent Pipeline
        logger.info("Starting agent pipeline...")
        
        # Phase 1: Vision
        vision_data = identify_product(temp_path, gemini_api_key)
        
        # Phase 2: Research
        research_results = perform_research(vision_data.search_query, firecrawl_api_key)
        
        # Phase 3: Synthesis
        final_catalog_entry = synthesize_product_data(vision_data, research_results, gemini_api_key)
        
        logger.info("Pipeline completed successfully.")
        return final_catalog_entry

    except AgentError as e:
        logger.error(f"Agent processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
    finally:
        # 5. Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
