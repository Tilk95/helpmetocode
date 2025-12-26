/**
 * Application principale - Point d'entrée
 */

(function() {
    'use strict';
    
    /**
     * Initialise l'application
     */
    function init() {
        // Initialiser les composants
        if (Components) {
            Components.init();
        }
        
        // Gestionnaire pour le bouton de challenge
        var btnChallenge = document.getElementById('btn-challenge');
        if (btnChallenge) {
            btnChallenge.addEventListener('click', handleChallenge);
        }
        
        // Vérifier la santé de l'API au chargement
        checkHealth();
    }
    
    /**
     * Vérifie la santé de l'API
     */
    function checkHealth() {
        if (API && API.checkHealth) {
            API.checkHealth()
                .then(function(response) {
                    if (!response.ollama_available) {
                        console.warn('Ollama n\'est pas disponible');
                        if (UI) {
                            UI.showError('⚠️ Ollama n\'est pas disponible. Assurez-vous qu\'Ollama est démarré et accessible sur http://127.0.0.1:11434');
                        }
                    }
                })
                .catch(function(error) {
                    console.error('Erreur lors de la vérification de santé:', error);
                });
        }
    }
    
    /**
     * Gère le clic sur le bouton de challenge
     */
    function handleChallenge() {
        var codeInput = document.getElementById('code-input');
        var languageSelect = document.getElementById('language-select');
        var btnChallenge = document.getElementById('btn-challenge');
        
        if (!codeInput || !languageSelect || !btnChallenge) {
            return;
        }
        
        var code = codeInput.value.trim();
        
        if (!code) {
            if (UI) {
                UI.showError('Veuillez entrer du code à analyser');
            }
            return;
        }
        
        var language = languageSelect.value || 'python';
        
        // Désactiver le bouton pendant le traitement
        btnChallenge.disabled = true;
        btnChallenge.textContent = 'Traitement en cours...';
        
        // Masquer les résultats précédents et les erreurs
        if (UI) {
            UI.hideResults();
            UI.hideError();
            UI.showProgress();
            
            // Indiquer que le traitement commence
            UI.updateRoleStatus('challenger', 'running');
            console.log('[App] Démarrage du challenge...');
        }
        
        // Appeler l'API
        if (API && API.challengeCode) {
            console.log('[App] Appel API en cours...');
            var startTime = Date.now();
            
            API.challengeCode(code, language, null)
                .then(function(response) {
                    var duration = ((Date.now() - startTime) / 1000).toFixed(1);
                    console.log('[App] Réponse reçue après ' + duration + 's');
                    
                    if (response.status === 'success' && response.report) {
                        // Mettre à jour la progression
                        if (UI) {
                            UI.updateRoleStatus('challenger', 'completed');
                            UI.updateRoleStatus('reviewer', 'completed');
                            UI.updateRoleStatus('arbiter', 'completed');
                            UI.hideProgress();
                            UI.showResults(response.report);
                        }
                    } else {
                        throw new Error('Réponse invalide de l\'API');
                    }
                })
                .catch(function(error) {
                    var duration = ((Date.now() - startTime) / 1000).toFixed(1);
                    console.error('[App] Erreur après ' + duration + 's:', error);
                    
                    if (UI) {
                        UI.hideProgress();
                        var errorMsg = 'Erreur après ' + duration + 's: ' + (error.message || 'Une erreur est survenue');
                        if (error.message && error.message.includes('Timeout')) {
                            errorMsg += '\n\nLe traitement a pris trop de temps. Vérifiez:\n- Que Ollama est démarré\n- Que le modèle est téléchargé\n- Les logs du serveur pour plus de détails';
                        }
                        UI.showError(errorMsg);
                    }
                })
                .finally(function() {
                    // Réactiver le bouton
                    btnChallenge.disabled = false;
                    btnChallenge.textContent = 'Lancer le challenge';
                });
        } else {
            if (UI) {
                UI.hideProgress();
                UI.showError('Module API non disponible');
            }
            btnChallenge.disabled = false;
            btnChallenge.textContent = 'Lancer le challenge';
        }
    }
    
    // Initialiser l'application quand le DOM est prêt
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

