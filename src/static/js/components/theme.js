/**
 * Grace City Theme Manager
 * Handles dark/light mode switching with localStorage persistence
 * Load this script FIRST to prevent theme flash
 */

(function() {
    'use strict';

    const THEME_KEY = 'gc-theme-preference';
    const THEME_DARK = 'dark';
    const THEME_LIGHT = 'light';
    const THEME_ATTRIBUTE = 'data-gc-theme';

    /**
     * Get saved theme from localStorage or default to dark
     */
    function getSavedTheme() {
        try {
            const saved = localStorage.getItem(THEME_KEY);
            return saved === THEME_LIGHT ? THEME_LIGHT : THEME_DARK;
        } catch (e) {
            console.warn('localStorage not available:', e);
            return THEME_DARK;
        }
    }

    /**
     * Apply theme immediately to prevent flash
     */
    function applyTheme(theme) {
        document.documentElement.setAttribute(THEME_ATTRIBUTE, theme);
        // Only set on body if it exists (it won't exist during initial head script execution)
        if (document.body) {
            document.body.setAttribute(THEME_ATTRIBUTE, theme);
        }
    }

    /**
     * Save theme preference to localStorage
     */
    function saveTheme(theme) {
        try {
            localStorage.setItem(THEME_KEY, theme);
        } catch (e) {
            console.warn('Could not save theme preference:', e);
        }
    }

    /**
     * Toggle between dark and light themes
     */
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
        applyTheme(newTheme);
        saveTheme(newTheme);
        
        // Dispatch custom event for other scripts to listen to
        window.dispatchEvent(new CustomEvent('gc-theme-changed', { 
            detail: { theme: newTheme } 
        }));
        
        return newTheme;
    }

    /**
     * Get current active theme
     */
    function getCurrentTheme() {
        return document.documentElement.getAttribute(THEME_ATTRIBUTE) || THEME_DARK;
    }

    /**
     * Set specific theme
     */
    function setTheme(theme) {
        if (theme !== THEME_DARK && theme !== THEME_LIGHT) {
            console.warn('Invalid theme:', theme);
            return;
        }
        applyTheme(theme);
        saveTheme(theme);
        
        window.dispatchEvent(new CustomEvent('gc-theme-changed', { 
            detail: { theme: theme } 
        }));
    }

    /**
     * Check if dark mode is active
     */
    function isDarkMode() {
        return getCurrentTheme() === THEME_DARK;
    }

    // Apply saved theme immediately on script load
    const initialTheme = getSavedTheme();
    applyTheme(initialTheme);

    // Expose theme functions globally
    window.GCTheme = {
        toggle: toggleTheme,
        set: setTheme,
        get: getCurrentTheme,
        isDark: isDarkMode,
        DARK: THEME_DARK,
        LIGHT: THEME_LIGHT
    };

    // Initialize theme toggle buttons when DOM is ready
    function initThemeToggleButtons() {
        const toggleButtons = document.querySelectorAll('[data-gc-theme-toggle]');
        
        toggleButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                toggleTheme();
                updateToggleButtonsState();
            });
        });

        updateToggleButtonsState();
    }

    /**
     * Update toggle button states/text based on current theme
     */
    function updateToggleButtonsState() {
        const currentTheme = getCurrentTheme();
        const toggleButtons = document.querySelectorAll('[data-gc-theme-toggle]');
        
        toggleButtons.forEach(button => {
            // Update aria-label for accessibility
            button.setAttribute('aria-label', 
                `Switch to ${currentTheme === THEME_DARK ? 'light' : 'dark'} mode`);
            
            // Update data attribute
            button.setAttribute('data-current-theme', currentTheme);
            
            // Update button text if it has text content
            const lightText = button.getAttribute('data-light-text') || '☀️ Light';
            const darkText = button.getAttribute('data-dark-text') || '🌙 Dark';
            
            if (button.textContent.trim()) {
                button.textContent = currentTheme === THEME_DARK ? lightText : darkText;
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // Apply theme to body now that it exists
            applyTheme(getCurrentTheme());
            initThemeToggleButtons();
        });
    } else {
        // Apply theme to body now that it exists
        applyTheme(getCurrentTheme());
        initThemeToggleButtons();
    }

})();
