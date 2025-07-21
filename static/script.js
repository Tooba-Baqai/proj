// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;

function setDarkMode(on) {
    if (on) {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'on');
    } else {
        body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'off');
    }
}

darkModeToggle.addEventListener('click', () => {
    setDarkMode(!body.classList.contains('dark-mode'));
});

// On load, set dark mode from localStorage
if (localStorage.getItem('darkMode') === 'on') {
    setDarkMode(true);
}

// Client-side search filter
const searchInput = document.getElementById('searchInput');
const notesTable = document.getElementById('notesTable');
if (searchInput && notesTable) {
    searchInput.addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const rows = notesTable.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const content = row.querySelector('.note-content');
            if (content && content.textContent.toLowerCase().includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
} 