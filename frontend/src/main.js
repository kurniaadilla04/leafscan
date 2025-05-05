import './styles/style.css'

document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');

    // Create sections for each menu item
    const sections = {
        beranda: '<section></section>',
        prediksi: '<section><h1>Prediksi</h1><p>This is the prediction section.</p></section>',
        riwayat: '<section><h1>Riwayat</h1><p>This is the history section.</p></section>',
    };

    // Function to load the selected section
    const loadSection = (section) => {
        if (sections[section]) {
            app.innerHTML = sections[section];
        } else {
            app.innerHTML = '<section><h1>404 Not Found</h1></section>';
            console.error(`Section "${section}" not found.`);
        }
    };

    // Event listeners for navigation links
    document.querySelectorAll('.navbar-menu a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = e.target.getAttribute('href').substring(1);
            loadSection(section);
        });
    });

    // Load the default section
    loadSection('beranda');
});
