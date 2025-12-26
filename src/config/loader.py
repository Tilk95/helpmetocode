"""
Chargeur de configuration YAML
"""

import yaml
from pathlib import Path
from typing import Dict, Any
from src.core.models import PipelineConfig, RoleConfig
from src.utils.errors import ConfigError


class ConfigLoader:
    """
    Charge et valide la configuration depuis config.yaml
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialise le chargeur de configuration
        
        Args:
            config_path: Chemin vers le fichier config.yaml
        """
        self.config_path = Path(config_path)
    
    def load(self) -> PipelineConfig:
        """
        Charge et valide la configuration
        
        Returns:
            Configuration validée
            
        Raises:
            ConfigError: Si la configuration est invalide
        """
        if not self.config_path.exists():
            raise ConfigError(f"Fichier de configuration introuvable: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"Erreur de parsing YAML: {e}") from e
        except Exception as e:
            raise ConfigError(f"Erreur lors de la lecture du fichier: {e}") from e
        
        # Validation et construction de la configuration
        return self._validate_and_build(config_data)
    
    def _validate_and_build(self, data: Dict[str, Any]) -> PipelineConfig:
        """
        Valide et construit l'objet PipelineConfig
        
        Args:
            data: Données brutes du YAML
            
        Returns:
            Configuration validée
        """
        # Validation providers
        if "providers" not in data:
            raise ConfigError("Section 'providers' manquante dans la configuration")
        
        providers = data["providers"]
        if "ollama_local" not in providers:
            raise ConfigError("Section 'providers.ollama_local' manquante")
        
        ollama_config = providers["ollama_local"]
        base_url = ollama_config.get("base_url", "http://127.0.0.1:11434")
        ollama_timeout = ollama_config.get("timeout", 300)
        
        # Validation roles
        if "roles" not in data:
            raise ConfigError("Section 'roles' manquante dans la configuration")
        
        roles_config = {}
        for role_name, role_data in data["roles"].items():
            if "model" not in role_data:
                raise ConfigError(f"Modèle manquant pour le rôle '{role_name}'")
            
            roles_config[role_name] = RoleConfig(
                model=role_data["model"],
                temperature=role_data.get("temperature", 0.7),
                top_p=role_data.get("top_p", 0.9),
                num_ctx=role_data.get("num_ctx", 4096),
                timeout=role_data.get("timeout", ollama_timeout)
            )
        
        # Validation pipeline
        if "pipeline" not in data:
            raise ConfigError("Section 'pipeline' manquante dans la configuration")
        
        pipeline = data["pipeline"]
        if not isinstance(pipeline, list):
            raise ConfigError("La section 'pipeline' doit être une liste")
        
        # Vérifier que tous les rôles du pipeline existent
        for role in pipeline:
            if role not in roles_config:
                raise ConfigError(f"Rôle '{role}' du pipeline non défini dans 'roles'")
        
        # Validation templates
        if "templates" not in data:
            raise ConfigError("Section 'templates' manquante dans la configuration")
        
        templates = data["templates"]
        
        # Vérifier que tous les rôles du pipeline ont un template
        for role in pipeline:
            if role not in templates:
                raise ConfigError(f"Template manquant pour le rôle '{role}'")
        
        # Settings
        settings = data.get("settings", {})
        
        return PipelineConfig(
            ollama_base_url=base_url,
            ollama_timeout=ollama_timeout,
            roles=roles_config,
            pipeline=pipeline,
            templates=templates,
            settings=settings
        )

