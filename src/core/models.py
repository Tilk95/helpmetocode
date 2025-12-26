"""
Modèles de données pour Code Challenger Local
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class Verdict(str, Enum):
    """Verdict possible de l'Arbiter"""
    ACCEPTE = "ACCEPTÉ"
    ACCEPTE_AVEC_RESERVES = "ACCEPTÉ AVEC RÉSERVES"
    REFUSE = "REFUSÉ"


@dataclass
class Context:
    """
    Contexte pour l'exécution du pipeline
    """
    project_name: str = "Code Challenger Local"
    language: str = "python"
    runtime: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le contexte en dictionnaire pour les templates"""
        return {
            "PROJECT_NAME": self.project_name,
            "LANGUAGE": self.language,
            "RUNTIME": self.runtime or "",
            "CONSTRAINTS": str(self.constraints) if self.constraints else "",
        }


@dataclass
class Report:
    """
    Rapport final du pipeline
    """
    challenger: str
    reviewer: str
    arbiter: str
    verdict: Verdict
    code_final: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit le rapport en dictionnaire pour l'API"""
        return {
            "challenger": self.challenger,
            "reviewer": self.reviewer,
            "arbiter": self.arbiter,
            "verdict": self.verdict.value,
            "code_final": self.code_final,
        }


@dataclass
class RoleConfig:
    """
    Configuration d'un rôle (Challenger, Reviewer, Arbiter)
    """
    model: str
    temperature: float
    top_p: float
    num_ctx: int
    timeout: int


@dataclass
class PipelineConfig:
    """
    Configuration complète du pipeline
    """
    ollama_base_url: str
    ollama_timeout: int
    roles: Dict[str, RoleConfig]
    pipeline: list[str]
    templates: Dict[str, str]
    settings: Dict[str, Any]

