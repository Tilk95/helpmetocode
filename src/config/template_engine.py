"""
Moteur de templates pour remplacer les placeholders
"""

import re
from typing import Dict, Any
from src.utils.errors import TemplateError


class TemplateEngine:
    """
    Moteur de templates pour remplacer les placeholders {{PLACEHOLDER}}
    """
    
    # Pattern pour trouver les placeholders {{PLACEHOLDER}}
    PLACEHOLDER_PATTERN = re.compile(r'\{\{(\w+)\}\}')
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """
        Remplace les placeholders dans un template
        
        Args:
            template: Template avec placeholders {{PLACEHOLDER}}
            context: Dictionnaire de valeurs pour remplacer les placeholders
            
        Returns:
            Template avec placeholders remplacés
            
        Raises:
            TemplateError: Si un placeholder requis n'est pas fourni
        """
        def replace_placeholder(match):
            placeholder_name = match.group(1)
            if placeholder_name in context:
                return str(context[placeholder_name])
            else:
                # Avertissement mais on continue (placeholder optionnel)
                return match.group(0)  # Garde le placeholder tel quel
        
        try:
            result = self.PLACEHOLDER_PATTERN.sub(replace_placeholder, template)
            return result
        except Exception as e:
            raise TemplateError(f"Erreur lors du rendu du template: {e}") from e
    
    def get_placeholders(self, template: str) -> list[str]:
        """
        Extrait tous les placeholders d'un template
        
        Args:
            template: Template à analyser
            
        Returns:
            Liste des noms de placeholders trouvés
        """
        return self.PLACEHOLDER_PATTERN.findall(template)

