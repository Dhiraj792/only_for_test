#!/usr/bin/env python3
"""
Legal Advisor Backend - Entry point
Run with: python -m backend.run
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("API_DEBUG", "false").lower() == "true"

    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    )
