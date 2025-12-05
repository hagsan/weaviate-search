"""
FastAPI application for semantic product search using Weaviate.
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from weaviate_client import WeaviateClient
from typing import Optional

app = FastAPI(title="Weaviate Semantic Search")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Weaviate client
weaviate_client = WeaviateClient()


@app.on_event("shutdown")
async def shutdown_event():
    """Close Weaviate connection on app shutdown."""
    weaviate_client.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with search bar."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search")
async def search(query: str = Form(...)):
    """Handle search query and redirect to products page."""
    return RedirectResponse(url=f"/products?q={query}", status_code=303)


@app.get("/products", response_class=HTMLResponse)
async def products(request: Request, q: Optional[str] = None):
    """Display product search results."""
    if q:
        # Perform semantic search
        products_list = weaviate_client.search_products(q, limit=20)
    else:
        # Show all products if no query
        products_list = weaviate_client.get_all_products(limit=20)
    
    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products_list,
            "query": q or ""
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

