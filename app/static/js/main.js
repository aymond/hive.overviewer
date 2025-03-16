// Custom JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    // Add 'active' class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Set current year in footer
    const yearSpan = document.querySelector('.current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Form validation - handle without alerts
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Add validation feedback directly to form
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    const feedbackDiv = field.nextElementSibling || document.createElement('div');
                    feedbackDiv.className = 'invalid-feedback';
                    feedbackDiv.textContent = field.validationMessage;
                    if (!field.nextElementSibling) {
                        field.parentNode.insertBefore(feedbackDiv, field.nextSibling);
                    }
                });
            }
            form.classList.add('was-validated');
        });
    });
}); 