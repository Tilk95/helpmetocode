# Code Challenger Local — Spécifications à fournir à Cursor (V0)

Ce document regroupe, en un seul fichier, les **spécifications** et le **README** nécessaires pour demander à Cursor de développer l’outil.

---

## 1) Spécification fonctionnelle et technique (V0)

### 1.1 Objectif

Créer un outil local permettant de :
- coller ou charger du code source,
- soumettre ce code à plusieurs rôles (challenger, reviewer, arbitre, experts optionnels),
- orchestrer automatiquement les appels aux LLM selon un pipeline défini,
- produire un rapport structuré (critiques, code amélioré, verdict).

Objectif principal : **augmenter la qualité du code** par confrontation multi-agents, en restant **100 % local**.

---

### 1.2 Portée V0

#### Inclus
- Interface simple (Web local ou Desktop)
- Support d’un seul langage à la fois (ex : Python)
- Entrée : texte collé + chargement de fichier
- **1 modèle par rôle**, configurable
- Pipeline linéaire : **Challenger → Reviewer → Arbiter**
- Backend : **Ollama local** uniquement
- Exécution séquentielle (un rôle après l’autre) pour limiter la RAM

#### Exclu (V0)
- Authentification
- Multi-utilisateur
- Historique long terme et recherche
- RAG / indexation / base documentaire
- Connexion cloud
- Exécution de code (l’outil ne doit pas exécuter le code analysé)

---

### 1.3 Architecture

```
[ UI locale ]  →  [ Orchestrateur Python ]  →  [ Ollama API locale (127.0.0.1:11434) ]
```

Composants :
- **UI** : saisie et affichage (web local ou Streamlit)
- **Orchestrateur** : gère pipeline et appels modèles
- **Config YAML** : modèles + paramètres + templates
- **Ollama** : serveur LLM local

---

### 1.4 Rôles

Rôles V0 obligatoires :
- **Challenger** : critique agressive (bugs, cas limites, perf, lisibilité, maintenance)
- **Reviewer** : propose une version améliorée + explication des changements
- **Arbiter** : verdict final (Accepté / Accepté avec réserves / Refusé)

Rôles optionnels (activables plus tard) :
- **Perf Expert** : analyse scalabilité, complexité, mémoire, IO
- **Security Expert** : robustesse, entrées non fiables, crash, risques
- **Domain Expert** : règles métier (si besoin)

Chaque rôle = 1 modèle Ollama + 1 template prompt + paramètres (temperature, num_ctx, etc.).

---

### 1.5 Pipeline V0

Pipeline par défaut :

```
Input code → Challenger → Reviewer → Arbiter → Rapport final
```

Le pipeline doit :
- être **déterministe** (même entrée + même config → résultats comparables)
- être **séquentiel** pour éviter surcharge RAM
- produire un **report** structuré

---

### 1.6 Interface utilisateur (V0)

#### Écran unique
- Zone texte : **Code source**
- Bouton : **Lancer le challenge**
- (Option) Sélecteur : langage (valeur unique “Python” en V0 si souhaité)
- Indicateur de progression par rôle :
  - Challenger…
  - Reviewer…
  - Arbiter…

#### Résultats (onglets ou sections)
- **Critiques** (sortie Challenger)
- **Code amélioré** (sortie Reviewer)
- **Verdict** (sortie Arbiter)
- (Option) **Perf** / **Sécurité**

---

### 1.7 Configuration (YAML)

Un fichier `config.yaml` doit permettre :
- définir l’URL Ollama
- définir **1 modèle par rôle**
- définir les templates prompts
- définir les paramètres d’inférence par rôle

#### Exemple (structure attendue)
- providers.ollama_local.base_url
- roles.<role>.model / temperature / top_p / num_ctx
- templates.<role> = prompt template
- placeholders communs (PROJECT_NAME, LANGUAGE, RUNTIME, CONSTRAINTS, CODE, etc.)

---

### 1.8 Orchestrateur — Comportement attendu

#### Étapes
1. Charger `config.yaml`
2. Préparer un `context` (project_name, language, runtime, constraints, etc.)
3. Pour chaque rôle du pipeline :
   1) Construire le prompt à partir du template (remplacement placeholders)
   2) Appeler Ollama API `/api/chat`
   3) Collecter et stocker la réponse
4. Post-traitement :
   - extraire `verdict` et `code_final` si possible
   - générer un report final

#### Gestion d’erreurs
- Timeout : afficher erreur + arrêter le pipeline
- Réponse vide : retry 1 fois
- Erreur HTTP : message clair à l’utilisateur
- Toujours conserver les sorties déjà produites (si un rôle échoue)

---

### 1.9 API interne (contrat)

Signature logique :

```python
def run_pipeline(code: str, context: dict) -> dict:
    ...
```

Sortie minimale :

```json
{
  "challenger": "...",
  "reviewer": "...",
  "arbiter": "...",
  "verdict": "ACCEPTÉ|ACCEPTÉ AVEC RÉSERVES|REFUSÉ",
  "code_final": "..."
}
```

---

### 1.10 Contraintes

- **100 % local**
- Aucun appel réseau externe (hors `127.0.0.1`)
- Python 3.12
- Dépendances minimales
- Ne jamais exécuter le code soumis (analyse uniquement)
- Support de gros fichiers : l’UI doit accepter de coller/charger un fichier volumineux (limite raisonnable), le backend doit supporter un traitement texte stable.

---

### 1.11 Critères de succès V0

- Coller du code → lancer pipeline → obtenir :
  - critiques structurées
  - code amélioré complet
  - verdict final
- Tout tourne en local via Ollama
- La RAM reste maîtrisée (un modèle à la fois)

---

### 1.12 Livrables V0

- `app.py` (web local) OU `streamlit_app.py`
- `orchestrator.py`
- `config.yaml`
- `templates.yaml` (optionnel si intégré dans config)
- `ui/` (si web static) : `index.html`, `app.js`, `style.css`
- `cli.py` (optionnel)
- `README.md`
- `SPEC_CODE_CHALLENGER.md` (ce document ou version dédiée)

---

## 2) README (à intégrer dans le projet)

### Code Challenger Local

Outil local permettant de challenger, auditer et améliorer du code source en s’appuyant sur plusieurs modèles LLM exécutés localement via Ollama.

#### Fonctionnalités
- Coller / charger du code
- Pipeline multi-rôles : Challenger → Reviewer → Arbiter
- 1 modèle par rôle (configurable)
- Résultats structurés : critiques, code amélioré, verdict
- 100 % local

#### Prérequis
- macOS ou Linux
- Python 3.12+
- Ollama installé et fonctionnel
- Au moins un modèle téléchargé

#### Installation
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Lancement (exemple)
```bash
python app.py
```
Ouvrir ensuite l’URL locale indiquée (ou Streamlit si utilisé).

#### Structure projet (suggestion)
```
code-challenger/
├── app.py
├── orchestrator.py
├── config.yaml
├── requirements.txt
├── SPEC_CODE_CHALLENGER.md
└── README.md
```

#### Sécurité
- Aucune donnée envoyée vers l’extérieur
- Le code fourni n’est **pas exécuté**

---

## 3) Indications pratiques (pour Cursor)

### 3.1 Choix UI (V0)
- Option A (simple) : **Streamlit** (1 fichier, rapide à prototyper)
- Option B (web local) : `FastAPI` + page HTML statique (un peu plus long)

### 3.2 Recommandation V0
Commencer avec **Streamlit** (MVP), puis migrer si besoin vers FastAPI.

### 3.3 Configuration “1 modèle par rôle” (exemple)
Modèles indicatifs (à adapter selon RAM) :
- generator (optionnel) : `qwen2.5-coder:14b`
- challenger : `deepseek-coder-v2:lite`
- reviewer : `codestral:22b`
- arbiter : `qwen2.5-coder:32b` (sinon `codestral:22b` si RAM limite)

### 3.4 Prompts
Utiliser des templates avec placeholders (PROJECT_NAME, CODE, CRITIQUES, etc.) et produire des sorties structurées.

---

## 4) Backlog technique minimal (V0)

1. Charger config YAML
2. Implémenter client Ollama `/api/chat` (timeout + retry)
3. Implémenter moteur de templates (remplacement `{{PLACEHOLDER}}`)
4. Implémenter orchestrateur pipeline (Challenger → Reviewer → Arbiter)
5. Implémenter UI :
   - zone code
   - bouton run
   - affichage progress + résultats
6. Export optionnel du report (Markdown ou JSON)

---

Fin du document.
