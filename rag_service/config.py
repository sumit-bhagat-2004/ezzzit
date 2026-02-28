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
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

EMBEDDING_MODEL = "snowflake-arctic-embed-m"
EMBEDDING_DIMENSION = 768

# Chunking parameters
CHUNK_SIZE = 100
CHUNK_OVERLAP = 20

# Retrieval parameters
TOP_K_RESULTS = 3

# Execution API parameters
EXECUTION_API_URL = os.getenv("EXECUTION_API_URL", "http://64.227.180.184:8000")

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