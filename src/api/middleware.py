"""
Middleware pour l'API FastAPI
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def setup_cors(app: FastAPI):
    """
    Configure CORS pour l'application
    
    Args:
        app: Application FastAPI
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En local, on autorise tout
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

