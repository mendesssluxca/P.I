
document.querySelectorAll('nav ul li a').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        document.getElementById(targetId).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

window.addEventListener('scroll', () => {
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(item => {
        const itemPosition = item.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.2;
        if (itemPosition < screenPosition) {
            item.style.transform = 'translateY(0)';
            item.style.opacity = '1';
            item.style.transition = 'transform 0.5s ease-out, opacity 0.5s ease-out';
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(item => {
        item.style.transform = 'translateY(50px)';
        item.style.opacity = '0';
    });
});