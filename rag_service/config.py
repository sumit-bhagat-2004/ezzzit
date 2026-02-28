"""
Configuration module for Snowflake RAG Service.
Loads all credentials and connection parameters from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "SSE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "SSE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAG_SCHEMA")

# Embedding model configuration
EMBEDDING_MODEL = "snowflake-arctic-embed-m"
EMBEDDING_DIMENSION = 768

# Chunking parameters
CHUNK_SIZE = 400  # words
CHUNK_OVERLAP = 50  # words

# Retrieval parameters
TOP_K_RESULTS = 3

# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set."""
    required_vars = [
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ACCOUNT"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    
    return True