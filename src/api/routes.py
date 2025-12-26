"""
Routes API pour Code Challenger Local
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.core.orchestrator import PipelineOrchestrator
from src.core.models import Context, Report
from src.core.ollama_client import OllamaClient
from src.utils.errors import PipelineError, OllamaError


router = APIRouter()


class ChallengeRequest(BaseModel):
    """Requête pour lancer un challenge"""
    code: str
    language: Optional[str] = "python"
    context: Optional[Dict[str, Any]] = None


class ChallengeResponse(BaseModel):
    """Réponse d'un challenge"""
    status: str
    report: Dict[str, Any]


class HealthResponse(BaseModel):
    """Réponse du health check"""
    status: str
    ollama_available: bool


# Variable globale pour l'orchestrateur (sera initialisée dans app.py)
_orchestrator: Optional[PipelineOrchestrator] = None
_ollama_client: Optional[OllamaClient] = None


def set_orchestrator(orchestrator: PipelineOrchestrator):
    """Définit l'orchestrateur global"""
    global _orchestrator
    _orchestrator = orchestrator


def set_ollama_client(client: OllamaClient):
    """Définit le client Ollama global"""
    global _ollama_client
    _ollama_client = client


@router.post("/challenge", response_model=ChallengeResponse)
async def challenge_code(request: ChallengeRequest):
    """
    Lance le pipeline de challenge sur le code fourni
    
    Args:
        request: Requête contenant le code et le contexte
        
    Returns:
        Rapport complet du pipeline
    """
    import time
    start_time = time.time()
    
    print(f"[API] Requête reçue - Langage: {request.language}, Code length: {len(request.code)}")
    
    if _orchestrator is None:
        print("[API] ⚠️ Orchestrateur non initialisé!")
        raise HTTPException(
            status_code=500,
            detail="Orchestrateur non initialisé"
        )
    
    try:
        # Construire le contexte
        context = Context(
            language=request.language or "python",
            constraints=request.context
        )
        
        print(f"[API] Démarrage du pipeline...")
        # Exécuter le pipeline
        report: Report = _orchestrator.run_pipeline(request.code, context)
        
        duration = time.time() - start_time
        print(f"[API] Pipeline terminé en {duration:.2f}s")
        
        return ChallengeResponse(
            status="success",
            report=report.to_dict()
        )
        
    except PipelineError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'exécution du pipeline: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur inattendue: {str(e)}"
        ) from e


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Vérifie la santé de l'API et la disponibilité d'Ollama
    
    Returns:
        Statut de santé
    """
    ollama_available = False
    
    if _ollama_client is not None:
        ollama_available = _ollama_client.health_check()
    
    return HealthResponse(
        status="ok",
        ollama_available=ollama_available
    )

