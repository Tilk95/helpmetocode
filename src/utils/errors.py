"""
Exceptions personnalisées pour Code Challenger Local
"""


class CodeChallengerError(Exception):
    """Exception de base pour Code Challenger Local"""
    pass


class OllamaError(CodeChallengerError):
    """Erreur lors d'un appel à l'API Ollama"""
    pass


class OllamaTimeoutError(OllamaError):
    """Timeout lors d'un appel à l'API Ollama"""
    pass


class ConfigError(CodeChallengerError):
    """Erreur de configuration"""
    pass


class TemplateError(CodeChallengerError):
    """Erreur lors du traitement d'un template"""
    pass


class PipelineError(CodeChallengerError):
    """Erreur lors de l'exécution du pipeline"""
    pass

