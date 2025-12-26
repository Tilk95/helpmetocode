"""
Orchestrateur du pipeline Challenger → Reviewer → Arbiter
"""

from typing import Dict, Any, Optional
from src.core.models import Report, Context, Verdict, PipelineConfig, RoleConfig
from src.core.ollama_client import OllamaClient
from src.config.template_engine import TemplateEngine
from src.utils.errors import PipelineError, OllamaError


class PipelineOrchestrator:
    """
    Orchestrateur pour exécuter le pipeline séquentiel
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialise l'orchestrateur
        
        Args:
            config: Configuration du pipeline
        """
        self.config = config
        self.ollama_client = OllamaClient(
            base_url=config.ollama_base_url,
            timeout=config.ollama_timeout
        )
        self.template_engine = TemplateEngine()
    
    def run_pipeline(self, code: str, context: Optional[Context] = None) -> Report:
        """
        Exécute le pipeline complet
        
        Args:
            code: Code source à analyser
            context: Contexte optionnel (utilise les valeurs par défaut si None)
            
        Returns:
            Rapport final avec toutes les sorties
            
        Raises:
            PipelineError: En cas d'erreur lors de l'exécution
        """
        if context is None:
            context = Context()
        
        # Préparer le contexte de base pour les templates
        template_context = {
            "CODE": code,
            "LANGUAGE": context.language,
            "PROJECT_NAME": context.project_name,
            "RUNTIME": context.runtime or "",
            "CONSTRAINTS": str(context.constraints) if context.constraints else "",
        }
        
        # Stockage des sorties de chaque rôle
        outputs = {}
        preserve_outputs = self.config.settings.get("preserve_outputs_on_error", True)
        max_retry = self.config.settings.get("max_retry", 1)
        
        # Exécution séquentielle du pipeline
        for role_name in self.config.pipeline:
            try:
                print(f"[Pipeline] Démarrage du rôle: {role_name}")
                
                # Récupérer la configuration du rôle
                role_config: RoleConfig = self.config.roles[role_name]
                print(f"[Pipeline] Modèle: {role_config.model}, Timeout: {role_config.timeout}s")
                
                # Construire le prompt à partir du template
                template = self.config.templates[role_name]
                
                # Ajouter les sorties précédentes au contexte si disponibles
                if role_name == "reviewer" and "challenger" in outputs:
                    template_context["CRITIQUES"] = outputs["challenger"]
                elif role_name == "arbiter":
                    if "challenger" in outputs:
                        template_context["CRITIQUES"] = outputs["challenger"]
                    if "reviewer" in outputs:
                        template_context["CODE_AMELIORE"] = outputs["reviewer"]
                
                # Rendre le template
                prompt = self.template_engine.render(template, template_context)
                print(f"[Pipeline] Prompt généré (longueur: {len(prompt)} caractères)")
                
                # Appeler Ollama
                print(f"[Pipeline] Appel à Ollama en cours...")
                response = self.ollama_client.chat(
                    model=role_config.model,
                    prompt=prompt,
                    temperature=role_config.temperature,
                    top_p=role_config.top_p,
                    num_ctx=role_config.num_ctx,
                    timeout=role_config.timeout,
                    max_retry=max_retry
                )
                
                print(f"[Pipeline] Réponse reçue du rôle {role_name} (longueur: {len(response)} caractères)")
                outputs[role_name] = response
                
            except OllamaError as e:
                if preserve_outputs:
                    # Conserver les sorties déjà produites
                    # On continue avec les sorties disponibles
                    pass
                else:
                    raise PipelineError(
                        f"Erreur lors de l'exécution du rôle '{role_name}': {e}"
                    ) from e
            except Exception as e:
                if preserve_outputs:
                    pass
                else:
                    raise PipelineError(
                        f"Erreur inattendue lors de l'exécution du rôle '{role_name}': {e}"
                    ) from e
        
        # Post-traitement : extraction du verdict et du code final
        verdict = self._extract_verdict(outputs.get("arbiter", ""))
        code_final = self._extract_code_final(outputs.get("reviewer", ""), code)
        
        # Construire le rapport
        return Report(
            challenger=outputs.get("challenger", ""),
            reviewer=outputs.get("reviewer", ""),
            arbiter=outputs.get("arbiter", ""),
            verdict=verdict,
            code_final=code_final
        )
    
    def _extract_verdict(self, arbiter_output: str) -> Verdict:
        """
        Extrait le verdict de la sortie de l'Arbiter
        
        Args:
            arbiter_output: Sortie de l'Arbiter
            
        Returns:
            Verdict extrait ou ACCEPTÉ par défaut
        """
        arbiter_upper = arbiter_output.upper()
        
        if "ACCEPTÉ AVEC RÉSERVES" in arbiter_upper or "ACCEPTE AVEC RESERVES" in arbiter_upper:
            return Verdict.ACCEPTE_AVEC_RESERVES
        elif "REFUSÉ" in arbiter_upper or "REFUSE" in arbiter_upper:
            return Verdict.REFUSE
        else:
            return Verdict.ACCEPTE
    
    def _extract_code_final(self, reviewer_output: str, original_code: str) -> str:
        """
        Extrait le code final amélioré de la sortie du Reviewer
        
        Args:
            reviewer_output: Sortie du Reviewer
            original_code: Code original
            
        Returns:
            Code final extrait ou code original par défaut
        """
        # Chercher des blocs de code dans la sortie (entre ```)
        import re
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', reviewer_output, re.DOTALL)
        
        if code_blocks:
            # Prendre le dernier bloc de code trouvé (généralement le code amélioré)
            return code_blocks[-1].strip()
        else:
            # Si aucun bloc de code trouvé, retourner le code original
            return original_code

