"""
Weaviate client for managing product schema and semantic search.
Uses Weaviate Python Client v4 API.
"""
import os
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class WeaviateClient:
    def __init__(self, url: str = None):
        """Initialize Weaviate client connection.
        
        Args:
            url: Weaviate URL. If not provided, uses WEAVIATE_URL from .env or defaults to http://localhost:8080
        """
        headers = {
            "X-Cohere-Api-Key": os.getenv("COHERE_APIKEY")
            }
        
        if url is None:
            url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        
        # For local connections, use connect_to_local
        if url.startswith("http://localhost") or url.startswith("http://127.0.0.1"):
            self.client = weaviate.connect_to_local(headers=headers)
        else:
            # Parse URL for custom connection
            if url.startswith("http://"):
                url = url[7:]
            elif url.startswith("https://"):
                url = url[8:]
            
            # Split host and port
            if ":" in url:
                host, port = url.split(":", 1)
                port = int(port)
            else:
                host = url
                port = 8080
            
            # Connect using v4 API for custom URL
            self.client = weaviate.connect_to_custom(
                http_host=host,
                http_port=port,
                grpc_port=50051,
                http_secure=False,
                grpc_secure=False,
                headers=headers
            )
        
        self.collection_name = "Product"
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        self.close()
    
    def close(self):
        """Close the Weaviate client connection."""
        if hasattr(self, 'client') and self.client:
            self.client.close()
    
    def initialize_schema(self):
        """Create Product collection schema if it doesn't exist.
        
        Uses Cohere vectorizer (text2vec-cohere). The COHERE_API_KEY must be configured
        in your Weaviate instance environment variables (typically in Docker).
        """
        # Check if collection already exists
        if self.client.collections.exists(self.collection_name):
            print(f"Collection '{self.collection_name}' already exists.")
            return
        
        try:
            # Create collection with v4 API
            self.client.collections.create(
                name=self.collection_name,
                description="Supermarket products with semantic search capabilities",
                properties=[
                    Property(name="name", data_type=DataType.TEXT, description="Product name"),
                    Property(
                        name="description", 
                        data_type=DataType.TEXT, 
                        description="Product description for semantic search"
                    ),
                    Property(name="price", data_type=DataType.NUMBER, description="Product price"),
                    Property(name="category", data_type=DataType.TEXT, description="Product category"),
                    Property(name="brand", data_type=DataType.TEXT, description="Product brand"),
                    Property(name="image_url", data_type=DataType.TEXT, description="Product image URL"),
                ],
                vectorizer_config=Configure.Vectorizer.text2vec_cohere(
                    model="embed-english-v3.0",
                    truncate="NONE"
                )
            )
            print(f"Collection '{self.collection_name}' created successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")
            print("Note: Make sure COHERE_API_KEY is configured in your Weaviate instance environment variables.")
            raise
    
    def insert_products(self, products: List[Dict[str, Any]]):
        """Insert multiple products into Weaviate using batch operations."""
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Insert products using batch context manager (v4 API)
            with collection.batch.dynamic() as batch:
                for product in products:
                    batch.add_object(properties=product)
            
            print(f"Inserted {len(products)} products successfully.")
        except Exception as e:
            print(f"Error inserting products: {e}")
            raise
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Perform semantic search on products."""
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Perform semantic search using v4 API
            response = collection.query.hybrid(
                query=query,
                alpha=1,
                #certainty=0.5,
                return_metadata=["distance", "certainty"]
            )
            
            # Convert response objects to dictionaries
            products = []
            for obj in response.objects:
                product = obj.properties
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def get_all_products(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products (for testing/display purposes)."""
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Get all products
            response = collection.query.fetch_objects(limit=limit)
            
            # Convert response objects to dictionaries
            products = []
            for obj in response.objects:
                product = obj.properties
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []
