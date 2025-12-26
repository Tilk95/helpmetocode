"""
Point d'entrée de l'application Code Challenger Local
"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH pour les imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.api.app import create_app


if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

