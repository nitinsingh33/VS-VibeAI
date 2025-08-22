"""
Netlify Functions handler for FastAPI app
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from mangum import Mangum
from main import app

# Create the Mangum handler for Netlify
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda / Netlify Functions handler
    """
    return handler(event, context)
