// Dark mode toggle logic
const toggleBtn = document.getElementById('dark-mode-toggle');
const darkModeCss = document.getElementById('dark-mode-css');




function setDarkMode(enabled) {
    const icon = document.getElementById('dark-mode-icon');
    document.body.classList.toggle('dark-mode', enabled);
    if (enabled) {
        darkModeCss.removeAttribute('disabled');
    } else {
        darkModeCss.setAttribute('disabled', '');
    }
    if (icon) {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        icon.classList.remove('fa-solid');
        icon.classList.add('fa-regular');
    }
    localStorage.setItem('darkMode', enabled ? '1' : '0');
}

toggleBtn.addEventListener('click', () => {
    setDarkMode(!document.body.classList.contains('dark-mode'));
});

// On page load, set mode from localStorage
if (localStorage.getItem('darkMode') === '1') {
    setDarkMode(true);
} else {
    setDarkMode(false);
}
