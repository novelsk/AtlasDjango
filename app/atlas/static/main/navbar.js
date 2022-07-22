const navMenu = Array.from(document.getElementsByClassName('nav-link'));
navMenu.forEach((item) => {
    item.addEventListener('mouseover', function () {
        jQuery(item).addClass('active');
    });
    item.addEventListener('mouseout', function () {
        jQuery(item).removeClass('active');
    });
});
