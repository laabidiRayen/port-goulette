document.addEventListener('DOMContentLoaded', () => {
    // Handle Navigation
    const navLinks = document.querySelectorAll('header nav ul li a');
    const sections = document.querySelectorAll('section');

    // Scroll to Section on Navigation Click
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').slice(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Simulate Login Flow
    const loginForm = document.querySelector('#login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Login Successful! Redirecting to main page...');
            window.location.href = 'main.html';
        });
    }

    // Simulate Registration Flow
    const registerForm = document.querySelector('#register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Registration Successful! Redirecting to login page...');
            window.location.href = 'login.html';
        });
    }

    // Placeholder for Interactive Map
    const mapPlaceholder = document.querySelector('.map-placeholder');
    if (mapPlaceholder) {
        mapPlaceholder.addEventListener('click', () => {
            alert('Interactive Map feature coming soon!');
        });
    }

    // Service Cards Animation
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.style.transform = 'scale(1.05)';
        });

        card.addEventListener('mouseout', () => {
            card.style.transform = 'scale(1)';
        });
    });
});
