# Code Challenger Local

Outil local permettant de challenger, auditer et améliorer du code source en s'appuyant sur plusieurs modèles LLM exécutés localement via Ollama.

## Fonctionnalités

- **Pipeline multi-rôles** : Challenger → Reviewer → Arbiter
- **1 modèle par rôle** (configurable)
- **Résultats structurés** : critiques, code amélioré, verdict
- **100% local** : aucune connexion cloud
- **Interface web** : interface JavaScript legacy simple et intuitive

## Prérequis

- macOS ou Linux
- Python 3.12+
- Ollama installé et fonctionnel
- Au moins un modèle Ollama téléchargé (voir configuration)

## Installation

1. Cloner ou télécharger le projet

2. Créer un environnement virtuel :
```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer Ollama :
   - Assurez-vous qu'Ollama est installé et démarré
   - Téléchargez les modèles nécessaires (voir `config/config.yaml`)
   - Par défaut, Ollama doit être accessible sur `http://127.0.0.1:11434`

## Configuration

Le fichier `config/config.yaml` permet de configurer :

- **Providers** : URL et timeout d'Ollama
- **Rôles** : modèles et paramètres pour chaque rôle (Challenger, Reviewer, Arbiter)
- **Pipeline** : ordre d'exécution des rôles
- **Templates** : prompts pour chaque rôle

### Modèles recommandés

Selon votre RAM disponible :

- **Challenger** : `deepseek-coder-v2:lite` (léger)
- **Reviewer** : `codestral:22b` (moyen)
- **Arbiter** : `qwen2.5-coder:32b` ou `codestral:22b` si RAM limitée

Téléchargez les modèles avec :
```bash
ollama pull deepseek-coder-v2:lite
ollama pull codestral:22b
ollama pull qwen2.5-coder:32b
```

## Lancement

1. Démarrer Ollama (si ce n'est pas déjà fait) :
```bash
ollama serve
```

2. Lancer l'application :
```bash
python app.py
```

3. Ouvrir votre navigateur à l'adresse :
```
http://127.0.0.1:8000
```

## Utilisation

1. **Coller ou taper votre code** dans la zone de texte
2. **Sélectionner le langage** (Python par défaut)
3. **Cliquer sur "Lancer le challenge"**
4. **Attendre le traitement** (la progression s'affiche)
5. **Consulter les résultats** dans les onglets :
   - **Critiques** : analyse détaillée du Challenger
   - **Code amélioré** : version améliorée par le Reviewer
   - **Verdict** : verdict final de l'Arbiter

## Structure du projet

```
helpmetocode/
├── src/
│   ├── core/              # Logique métier
│   │   ├── models.py      # Modèles de données
│   │   ├── ollama_client.py  # Client Ollama
│   │   └── orchestrator.py  # Orchestrateur pipeline
│   ├── api/               # API REST
│   │   ├── app.py         # Application FastAPI
│   │   ├── routes.py      # Routes API
│   │   └── middleware.py  # Middleware CORS
│   ├── config/            # Configuration
│   │   ├── loader.py      # Chargeur config
│   │   └── template_engine.py  # Moteur templates
│   └── utils/             # Utilitaires
│       └── errors.py       # Exceptions
├── static/                # Assets statiques
│   ├── css/               # Styles
│   └── js/                # JavaScript
├── templates/             # Templates HTML
│   └── index.html         # Page principale
├── config/                # Configuration
│   └── config.yaml        # Configuration principale
├── app.py                 # Point d'entrée
├── requirements.txt       # Dépendances
└── README.md              # Ce fichier
```

## API REST

L'application expose une API REST sur `/api` :

### POST /api/challenge

Lance le pipeline de challenge.

**Requête** :
```json
{
  "code": "def hello():\n    print('Hello')",
  "language": "python",
  "context": null
}
```

**Réponse** :
```json
{
  "status": "success",
  "report": {
    "challenger": "...",
    "reviewer": "...",
    "arbiter": "...",
    "verdict": "ACCEPTÉ",
    "code_final": "..."
  }
}
```

### GET /api/health

Vérifie la santé de l'API et la disponibilité d'Ollama.

**Réponse** :
```json
{
  "status": "ok",
  "ollama_available": true
}
```

## Sécurité

- ✅ **100% local** : aucune donnée envoyée vers l'extérieur
- ✅ **Pas d'exécution** : le code fourni n'est **jamais exécuté**
- ✅ **Analyse uniquement** : l'outil analyse le code, ne l'exécute pas

## Dépannage

### Ollama n'est pas disponible

- Vérifiez qu'Ollama est démarré : `ollama serve`
- Vérifiez l'URL dans `config/config.yaml` (par défaut `http://127.0.0.1:11434`)
- Vérifiez que les modèles sont téléchargés : `ollama list`

### Erreur de timeout

- Augmentez le timeout dans `config/config.yaml`
- Vérifiez que votre machine a assez de RAM pour les modèles

### Erreur de configuration

- Vérifiez la syntaxe YAML de `config/config.yaml`
- Assurez-vous que tous les rôles du pipeline ont un modèle et un template défini

## Développement

### Tests

Les tests unitaires sont dans le répertoire `tests/` (à implémenter).

### Contribution

Ce projet est en version V0. Les fonctionnalités futures incluront :
- Support multi-langages simultanés
- Historique des challenges
- Export des rapports
- Rôles optionnels (Perf Expert, Security Expert)

## Licence

Ce projet est un outil local pour améliorer la qualité du code.

## Auteur

Développé avec Cursor AI et Ollama.
