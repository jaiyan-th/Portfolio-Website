/**
 * Theme Toggle Functionality
 * Handles light/dark mode switching with persistence
 */

class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.themeIcon = document.getElementById('theme-icon');
        this.init();
    }

    init() {
        // Load saved theme or default to dark
        const savedTheme = localStorage.getItem('theme') || 'dark';
        this.setTheme(savedTheme);
        
        // Add event listener for theme toggle
        this.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    setTheme(theme) {
        const html = document.documentElement;
        
        if (theme === 'dark') {
            html.classList.add('dark');
            this.themeIcon.className = 'fas fa-sun text-gray-600 dark:text-gray-300 text-lg';
        } else {
            html.classList.remove('dark');
            this.themeIcon.className = 'fas fa-moon text-gray-600 dark:text-gray-300 text-lg';
        }
        
        // Save theme preference
        localStorage.setItem('theme', theme);
        
        // Dispatch custom event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Add transition class for smooth theme switching
        document.body.classList.add('theme-transitioning');
        
        this.setTheme(newTheme);
        
        // Remove transition class after animation
        setTimeout(() => {
            document.body.classList.remove('theme-transitioning');
        }, 300);
    }

    getCurrentTheme() {
        return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}