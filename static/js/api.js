/**
 * Module API - Gestion des appels à l'API REST
 */

var API = (function() {
    'use strict';
    
    var BASE_URL = '/api';
    
    /**
     * Effectue un appel API
     * @param {string} method - Méthode HTTP (GET, POST, etc.)
     * @param {string} endpoint - Endpoint API
     * @param {object} data - Données à envoyer (optionnel)
     * @returns {Promise} Promise résolue avec la réponse
     */
    function request(method, endpoint, data) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            var url = BASE_URL + endpoint;
            
            xhr.open(method, url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        resolve(response);
                    } catch (e) {
                        reject(new Error('Erreur de parsing JSON: ' + e.message));
                    }
                } else {
                    try {
                        var error = JSON.parse(xhr.responseText);
                        reject(new Error(error.detail || 'Erreur HTTP ' + xhr.status));
                    } catch (e) {
                        reject(new Error('Erreur HTTP ' + xhr.status + ': ' + xhr.statusText));
                    }
                }
            };
            
            xhr.onerror = function() {
                reject(new Error('Erreur réseau'));
            };
            
            xhr.ontimeout = function() {
                reject(new Error('Timeout de la requête'));
            };
            
            xhr.timeout = 600000; // 10 minutes
            
            if (data) {
                xhr.send(JSON.stringify(data));
            } else {
                xhr.send();
            }
        });
    }
    
    /**
     * Lance un challenge sur du code
     * @param {string} code - Code source
     * @param {string} language - Langage du code
     * @param {object} context - Contexte optionnel
     * @returns {Promise} Promise résolue avec le rapport
     */
    function challengeCode(code, language, context) {
        return request('POST', '/challenge', {
            code: code,
            language: language || 'python',
            context: context || null
        });
    }
    
    /**
     * Vérifie la santé de l'API et d'Ollama
     * @returns {Promise} Promise résolue avec le statut
     */
    function checkHealth() {
        return request('GET', '/health');
    }
    
    // API publique
    return {
        challengeCode: challengeCode,
        checkHealth: checkHealth
    };
})();

