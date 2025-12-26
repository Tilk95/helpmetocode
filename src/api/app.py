"""
Application FastAPI principale
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from src.api.routes import router, set_orchestrator, set_ollama_client
from src.api.middleware import setup_cors
from src.config.loader import ConfigLoader
from src.core.orchestrator import PipelineOrchestrator
from src.core.ollama_client import OllamaClient


def create_app() -> FastAPI:
    """
    Crée et configure l'application FastAPI
    
    Returns:
        Application FastAPI configurée
    """
    app = FastAPI(
        title="Code Challenger Local",
        description="Outil local pour challenger et améliorer du code source",
        version="0.1.0"
    )
    
    # Configuration CORS
    setup_cors(app)
    
    # Charger la configuration
    try:
        config_loader = ConfigLoader("config/config.yaml")
        config = config_loader.load()
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement de la configuration: {e}")
        print("⚠️  L'application peut ne pas fonctionner correctement.")
        config = None
    
    # Initialiser l'orchestrateur si la config est valide
    if config:
        orchestrator = PipelineOrchestrator(config)
        ollama_client = OllamaClient(
            base_url=config.ollama_base_url,
            timeout=config.ollama_timeout
        )
        
        set_orchestrator(orchestrator)
        set_ollama_client(ollama_client)
    
    # Enregistrer les routes API
    app.include_router(router, prefix="/api", tags=["api"])
    
    # Servir les fichiers statiques
    static_dir = Path("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Route racine → index.html
    @app.get("/")
    async def read_root():
        index_path = Path("templates/index.html")
        if index_path.exists():
            return FileResponse(index_path)
        else:
            return {"message": "Code Challenger Local API", "status": "running"}
    
    return app

