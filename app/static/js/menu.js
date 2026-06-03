document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.querySelector('.floating-menu-button');
    const dropdown = document.querySelector('.menu-dropdown');

    if (menuButton && dropdown) {
        menuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('show');
        });

        document.addEventListener('click', function() {
            dropdown.classList.remove('show');
        });

        dropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});