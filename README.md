# Visual Product Cataloging Agent

A multimodal AI agent that takes an image of a product, identifies it using Gemini Vision, researches details using Firecrawl, and outputs a structured JSON catalog entry.

## Features
- **Visual Identification**: Uses Gemini (Flash) to identify brand, model, and features from an image.
- **Deep Research**: Uses Firecrawl v2 to search the web and scrape official specifications.
- **Structured Synthesis**: Combines all data into a validated Pydantic JSON schema.
- **Localized Pricing**: Automatically researches and provides estimated values in **Indian Rupees (INR)**.
- **E-commerce & Insurance Ready**: Tailored for generating professional product profiles.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SIDDU-IRONMAN/visual-project-agent.git
   cd visual-project-agent
   ```

2. **Install dependencies (using uv)**:
   This project uses `uv` for lightning-fast dependency management.
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Sync dependencies and create virtual environment
   uv sync
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

## Usage

### CLI Version
Run the agent using `uv run`:
```bash
uv run main.py path/to/your/image.jpg
```

### Web Version (SPA)
1. **Start the Backend**:
   ```bash
   uv run uvicorn backend.api:app --reload
   ```
   The API will be available at `http://localhost:8000`.

2. **Open the Frontend**:
   Simply open `frontend/index.html` in your web browser (or use a Live Server extension).

The web interface allows you to:
- Drag and drop images (up to 10MB).
- Watch the analysis progress in real-time.
- View structured product details, specifications, and estimated values in a clean UI.
- Inspect the raw JSON output.

## Development Workflow
- `main`: Stable release branch.
- `dev`: Active development branch.
- Feature branches are created from `dev` and merged back after testing.
