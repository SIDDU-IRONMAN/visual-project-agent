# Visual Product Cataloging Agent

A multimodal AI agent that takes an image of a product, identifies it using Gemini Vision, researches details using Firecrawl, and outputs a structured JSON catalog entry.

## Features
- **Visual Identification**: Uses Gemini 2.0 Flash to identify brand, model, and features from an image.
- **Deep Research**: Uses Firecrawl to search the web and scrape official specifications.
- **Structured Synthesis**: Combines all data into a validated Pydantic JSON schema.
- **E-commerce & Insurance Ready**: Tailored for generating professional product profiles.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SIDDU-IRONMAN/visual-project-agent.git
   cd visual-project-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

## Usage

Run the agent by providing a path to a product image:

```bash
python main.py path/to/your/image.jpg
```

The agent will:
1. Identify the product.
2. Search and scrape the web for details.
3. Output the final JSON to the console and save it to a local file.

## Development Workflow
- `main`: Stable release branch.
- `dev`: Active development branch.
- Feature branches are created from `dev` and merged back after testing.
