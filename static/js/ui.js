/**
 * Module UI - Gestion de l'interface utilisateur
 */

var UI = (function() {
    'use strict';
    
    /**
     * Affiche la section de progression
     */
    function showProgress() {
        var section = document.getElementById('progress-section');
        if (section) {
            section.style.display = 'block';
        }
        resetProgress();
    }
    
    /**
     * Masque la section de progression
     */
    function hideProgress() {
        var section = document.getElementById('progress-section');
        if (section) {
            section.style.display = 'none';
        }
    }
    
    /**
     * Réinitialise l'affichage de progression
     */
    function resetProgress() {
        var roles = ['challenger', 'reviewer', 'arbiter'];
        roles.forEach(function(role) {
            var item = document.getElementById('progress-' + role);
            if (item) {
                var status = item.querySelector('.progress-status');
                if (status) {
                    status.textContent = 'En attente...';
                    status.className = 'progress-status';
                }
            }
        });
        
        var progressBar = document.getElementById('progress-bar');
        if (progressBar) {
            progressBar.style.width = '0%';
        }
    }
    
    /**
     * Met à jour le statut d'un rôle
     * @param {string} role - Nom du rôle (challenger, reviewer, arbiter)
     * @param {string} status - Statut (pending, running, completed, error)
     */
    function updateRoleStatus(role, status) {
        var item = document.getElementById('progress-' + role);
        if (!item) return;
        
        var statusEl = item.querySelector('.progress-status');
        if (!statusEl) return;
        
        var statusText = {
            'pending': 'En attente...',
            'running': 'En cours...',
            'completed': 'Terminé',
            'error': 'Erreur'
        };
        
        statusEl.textContent = statusText[status] || status;
        statusEl.className = 'progress-status status-' + status;
        
        // Mettre à jour la barre de progression
        updateProgressBar(role, status);
    }
    
    /**
     * Met à jour la barre de progression globale
     * @param {string} role - Rôle actuel
     * @param {string} status - Statut
     */
    function updateProgressBar(role, status) {
        var progressBar = document.getElementById('progress-bar');
        if (!progressBar) return;
        
        var progress = 0;
        if (role === 'challenger') {
            progress = status === 'completed' ? 33 : status === 'running' ? 10 : 0;
        } else if (role === 'reviewer') {
            progress = status === 'completed' ? 66 : status === 'running' ? 40 : 33;
        } else if (role === 'arbiter') {
            progress = status === 'completed' ? 100 : status === 'running' ? 70 : 66;
        }
        
        progressBar.style.width = progress + '%';
    }
    
    /**
     * Affiche les résultats
     * @param {object} report - Rapport complet
     */
    function showResults(report) {
        var section = document.getElementById('results-section');
        if (section) {
            section.style.display = 'block';
        }
        
        // Afficher le contenu du Challenger
        var challengerContent = document.getElementById('challenger-content');
        if (challengerContent && report.challenger) {
            challengerContent.textContent = report.challenger;
        }
        
        // Afficher le contenu du Reviewer
        var reviewerContent = document.getElementById('reviewer-content');
        if (reviewerContent && report.code_final) {
            reviewerContent.textContent = report.code_final;
        }
        
        // Afficher le verdict et le contenu de l'Arbiter
        var arbiterContent = document.getElementById('arbiter-content');
        if (arbiterContent && report.arbiter) {
            arbiterContent.textContent = report.arbiter;
        }
        
        var verdictBadge = document.getElementById('verdict-badge');
        if (verdictBadge && report.verdict) {
            verdictBadge.textContent = report.verdict;
            verdictBadge.className = 'verdict-badge verdict-' + report.verdict.toLowerCase().replace(/\s+/g, '-');
        }
        
        // Activer l'onglet Critiques par défaut
        switchTab('challenger');
    }
    
    /**
     * Masque les résultats
     */
    function hideResults() {
        var section = document.getElementById('results-section');
        if (section) {
            section.style.display = 'none';
        }
    }
    
    /**
     * Affiche une erreur
     * @param {string} message - Message d'erreur
     */
    function showError(message) {
        var section = document.getElementById('error-section');
        var errorMessage = document.getElementById('error-message');
        
        if (section) {
            section.style.display = 'block';
        }
        
        if (errorMessage) {
            errorMessage.textContent = message || 'Une erreur est survenue';
        }
    }
    
    /**
     * Masque l'erreur
     */
    function hideError() {
        var section = document.getElementById('error-section');
        if (section) {
            section.style.display = 'none';
        }
    }
    
    /**
     * Change d'onglet
     * @param {string} tabName - Nom de l'onglet à afficher
     */
    function switchTab(tabName) {
        // Désactiver tous les onglets
        var tabButtons = document.querySelectorAll('.tab-btn');
        var tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(function(btn) {
            btn.classList.remove('active');
        });
        
        tabContents.forEach(function(content) {
            content.classList.remove('active');
        });
        
        // Activer l'onglet sélectionné
        var selectedBtn = document.querySelector('.tab-btn[data-tab="' + tabName + '"]');
        var selectedContent = document.getElementById('tab-' + tabName);
        
        if (selectedBtn) {
            selectedBtn.classList.add('active');
        }
        
        if (selectedContent) {
            selectedContent.classList.add('active');
        }
    }
    
    // API publique
    return {
        showProgress: showProgress,
        hideProgress: hideProgress,
        resetProgress: resetProgress,
        updateRoleStatus: updateRoleStatus,
        showResults: showResults,
        hideResults: hideResults,
        showError: showError,
        hideError: hideError,
        switchTab: switchTab
    };
})();

