const navMenu = Array.from(document.getElementsByClassName('nav-link'));
navMenu.forEach((item) => {
    item.addEventListener('click', function () {
        navMenu.forEach((temp) => {
            jQuery(temp).removeClass('active');
        });
        jQuery(item).addClass('active');
    });
});
