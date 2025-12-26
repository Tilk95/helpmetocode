"""
Client pour l'API Ollama
"""

import requests
from typing import Dict, Any, Optional
from src.utils.errors import OllamaError, OllamaTimeoutError


class OllamaClient:
    """
    Client pour interagir avec l'API Ollama locale
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout: int = 300):
        """
        Initialise le client Ollama
        
        Args:
            base_url: URL de base de l'API Ollama
            timeout: Timeout par défaut en secondes
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def chat(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_ctx: int = 4096,
        timeout: Optional[int] = None,
        max_retry: int = 1
    ) -> str:
        """
        Envoie une requête de chat à Ollama
        
        Args:
            model: Nom du modèle Ollama
            prompt: Prompt à envoyer
            temperature: Paramètre temperature
            top_p: Paramètre top_p
            num_ctx: Taille du contexte
            timeout: Timeout spécifique (utilise self.timeout si None)
            max_retry: Nombre maximum de tentatives en cas de réponse vide
            
        Returns:
            Réponse du modèle
            
        Raises:
            OllamaError: En cas d'erreur HTTP
            OllamaTimeoutError: En cas de timeout
        """
        url = f"{self.base_url}/api/chat"
        timeout_value = timeout if timeout is not None else self.timeout
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "num_ctx": num_ctx
            }
        }
        
        # Tentatives avec retry en cas de réponse vide
        last_error = None
        for attempt in range(max_retry + 1):
            try:
                print(f"[Ollama] Tentative {attempt + 1}/{max_retry + 1} - Modèle: {model}, URL: {url}")
                print(f"[Ollama] Envoi de la requête (timeout: {timeout_value}s)...")
                
                response = requests.post(
                    url,
                    json=payload,
                    timeout=timeout_value
                )
                
                print(f"[Ollama] Réponse HTTP reçue: {response.status_code}")
                
                # Vérifier le statut HTTP
                response.raise_for_status()
                
                # Extraire la réponse
                data = response.json()
                
                if "message" in data and "content" in data["message"]:
                    content = data["message"]["content"].strip()
                    
                    # Si réponse vide et qu'il reste des tentatives, réessayer
                    if not content and attempt < max_retry:
                        print(f"[Ollama] Réponse vide, nouvelle tentative...")
                        continue
                    
                    print(f"[Ollama] Réponse obtenue (longueur: {len(content)} caractères)")
                    return content
                else:
                    print(f"[Ollama] Format de réponse invalide: {data}")
                    raise OllamaError(f"Format de réponse Ollama invalide: {data}")
                    
            except requests.exceptions.Timeout as e:
                print(f"[Ollama] ⚠️ TIMEOUT après {timeout_value}s (modèle: {model})")
                raise OllamaTimeoutError(
                    f"Timeout lors de l'appel à Ollama (modèle: {model}, timeout: {timeout_value}s)"
                ) from e
                
            except requests.exceptions.RequestException as e:
                print(f"[Ollama] ⚠️ Erreur HTTP: {str(e)}")
                last_error = e
                if attempt < max_retry:
                    print(f"[Ollama] Nouvelle tentative...")
                    continue
                raise OllamaError(
                    f"Erreur HTTP lors de l'appel à Ollama (modèle: {model}): {str(e)}"
                ) from e
        
        # Si on arrive ici, toutes les tentatives ont échoué
        if last_error:
            raise OllamaError(
                f"Échec après {max_retry + 1} tentatives (modèle: {model}): {str(last_error)}"
            ) from last_error
        else:
            raise OllamaError(f"Réponse vide après {max_retry + 1} tentatives (modèle: {model})")
    
    def health_check(self) -> bool:
        """
        Vérifie si Ollama est disponible
        
        Returns:
            True si Ollama est disponible, False sinon
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

