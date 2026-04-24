#!/usr/bin/env python3
"""
Legal Advisor Backend - Production Ready Server

Run this script to start the FastAPI backend server with all sample legal documents pre-loaded.
"""

import os
import sys

# Add the parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("API_DEBUG", "false").lower() == "true"
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║           Legal Advisor - Backend Server                   ║
║                                                            ║
║   Starting FastAPI server with pre-loaded legal docs      ║
║   API Documentation: http://localhost:{port}/docs           ║
║   Health Check: http://localhost:{port}/health            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
