# Weaviate Semantic Search Application

A FastAPI web application that enables semantic search for supermarket products using Weaviate vector database.

## Features

- **Semantic Search**: Search products using natural language queries
- **Product Listing**: Display search results in a clean, modern interface
- **Sample Data Generator**: Script to populate Weaviate with sample supermarket products
- **FastAPI Backend**: Modern Python web framework
- **Responsive UI**: Clean, mobile-friendly design

## Prerequisites

- Python 3.8+
- Weaviate running on `localhost:8080` (Docker container)
- Cohere API key (for vectorization)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
   - Copy `.env.example` to `.env` (if it exists) or create a `.env` file
   - The Cohere API key needs to be set in your Weaviate Docker container environment variables
   - Example Docker run command:
     ```bash
     docker run -e COHERE_API_KEY=your-api-key-here ...
     ```
   - Or in `docker-compose.yml`:
     ```yaml
     environment:
       - COHERE_APIKEY=your-api-key-here
     ```

3. Generate sample product data:
```bash
python generate_data.py
```

## Running the Application

Start the FastAPI server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload
```

The application will be available at `http://localhost:8000`

## Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Enter a search query in natural language (e.g., "healthy breakfast options", "something sweet", "protein-rich foods")
3. View the search results on the products page
4. Click "Back to Search" to perform another search

## Project Structure

```
weaviate-search/
├── app.py                 # Main FastAPI application
├── weaviate_client.py     # Weaviate connection and schema management
├── generate_data.py       # Script to generate sample product data
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page with search bar
│   └── products.html     # Product list page
├── static/
│   └── style.css         # Styling
└── README.md             # This file
```

## Weaviate Configuration

The application uses **Weaviate Python Client v4** and connects to Weaviate at `http://localhost:8080`. It uses:
- **Vectorizer**: text2vec-cohere (requires Cohere API key configured in Weaviate Docker container)
- **Schema**: Product collection with name, description, price, category, brand, and image_url
- **Model**: embed-english-v3.0

### Important: gRPC Port Required

The Weaviate v4 client uses gRPC for communication. Ensure your Weaviate Docker container exposes the gRPC port (default: 50051):

**Docker Run:**
```bash
docker run -p 8080:8080 -p 50051:50051 -e COHERE_API_KEY=your-cohere-api-key-here ...
```

**Docker Compose:**
```yaml
services:
  weaviate:
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      - COHERE_API_KEY=your-cohere-api-key-here
```

### Setting up Cohere API Key

The Cohere API key must be configured as an environment variable in your Weaviate Docker container. The `.env` file in this project is for reference only. The actual API key must be set in the Weaviate container environment.

## Sample Data

The `generate_data.py` script generates sample products across multiple categories:
- Fruits
- Vegetables
- Dairy
- Meat
- Beverages
- Snacks
- Bakery
- Frozen

Each product includes realistic names, descriptions, prices, brands, and categories.

