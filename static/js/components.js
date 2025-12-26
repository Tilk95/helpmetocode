/**
 * Module Components - Composants réutilisables
 */

var Components = (function() {
    'use strict';
    
    /**
     * Initialise les gestionnaires d'événements pour les onglets
     */
    function initTabs() {
        var tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var tabName = this.getAttribute('data-tab');
                if (tabName && UI) {
                    UI.switchTab(tabName);
                }
            });
        });
    }
    
    /**
     * Initialise le bouton de fermeture d'erreur
     */
    function initErrorDismiss() {
        var btn = document.getElementById('btn-dismiss-error');
        if (btn) {
            btn.addEventListener('click', function() {
                if (UI) {
                    UI.hideError();
                }
            });
        }
    }
    
    /**
     * Initialise tous les composants
     */
    function init() {
        initTabs();
        initErrorDismiss();
    }
    
    // API publique
    return {
        init: init
    };
})();

