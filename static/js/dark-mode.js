// Dark mode functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved dark mode preference or use system preference
    const savedDarkMode = localStorage.getItem('darkMode');

    if (savedDarkMode === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});
