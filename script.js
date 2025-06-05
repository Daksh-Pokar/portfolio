/* ===============================================
   PORTFOLIO WEBSITE JAVASCRIPT
   =============================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initializeNavigation();
    initializeSmoothScrolling();
    initializeFormHandling();
    initializeScrollEffects();
    initializeThemeToggle();
    
    console.log('Portfolio website initialized successfully!');
});

/* ===============================================
   NAVIGATION FUNCTIONALITY
   =============================================== */

/**
 * Initialize mobile navigation and active link highlighting
 */
function initializeNavigation() {
    // Get navigation elements
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle functionality
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            // Toggle hamburger animation
            hamburger.classList.toggle('active');
            // Toggle mobile menu visibility
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (hamburger && navMenu) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });
    
    // Highlight active navigation link based on scroll position
    window.addEventListener('scroll', highlightActiveNavLink);
}

/**
 * Highlight the active navigation link based on current scroll position
 */
function highlightActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    
    // Find which section is currently in view
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100; // Offset for navbar height
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });
    
    // Update active nav link
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

/* ===============================================
   SMOOTH SCROLLING FUNCTIONALITY
   =============================================== */

/**
 * Initialize smooth scrolling for navigation links
 */
function initializeSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Only handle internal links (starting with #)
            if (href.startsWith('#')) {
                e.preventDefault();
                
                const targetSection = document.querySelector(href);
                if (targetSection) {
                    // Calculate offset to account for fixed navbar
                    const offsetTop = targetSection.offsetTop - 80;
                    
                    // Smooth scroll to target section
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

/* ===============================================
   FORM HANDLING FUNCTIONALITY
   =============================================== */

/**
 * Initialize contact form handling with validation
 */
function initializeFormHandling() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmission);
        
        // Add real-time validation
        const formInputs = contactForm.querySelectorAll('input, textarea');
        formInputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearFieldError);
        });
    }
}

/**
 * Handle contact form submission
 * @param {Event} e - Form submission event
 */
function handleFormSubmission(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Get form fields
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    // Validate all fields
    if (validateForm(name, email, message)) {
        // Show loading state
        showFormLoading(true);
        
        // Simulate form submission (replace with actual submission logic)
        setTimeout(() => {
            showFormLoading(false);
            showFormSuccess();
            form.reset();
        }, 2000);
        
        console.log('Form submitted:', { name, email, message });
    }
}

/**
 * Validate the entire form
 * @param {string} name - Name field value
 * @param {string} email - Email field value
 * @param {string} message - Message field value
 * @returns {boolean} - True if form is valid
 */
function validateForm(name, email, message) {
    let isValid = true;
    
    // Validate name
    if (!name || name.trim().length < 2) {
        showFieldError('name', 'Name must be at least 2 characters long');
        isValid = false;
    }
    
    // Validate email
    if (!email || !isValidEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    // Validate message
    if (!message || message.trim().length < 10) {
        showFieldError('message', 'Message must be at least 10 characters long');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Validate individual field on blur
 * @param {Event} e - Blur event
 */
function validateField(e) {
    const field = e.target;
    const value = field.value.trim();
    
    switch (field.name) {
        case 'name':
            if (value.length > 0 && value.length < 2) {
                showFieldError('name', 'Name must be at least 2 characters long');
            } else {
                clearFieldError('name');
            }
            break;
            
        case 'email':
            if (value.length > 0 && !isValidEmail(value)) {
                showFieldError('email', 'Please enter a valid email address');
            } else {
                clearFieldError('email');
            }
            break;
            
        case 'message':
            if (value.length > 0 && value.length < 10) {
                showFieldError('message', 'Message must be at least 10 characters long');
            } else {
                clearFieldError('message');
            }
            break;
    }
}

/**
 * Check if email is valid
 * @param {string} email - Email to validate
 * @returns {boolean} - True if email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show error message for a field
 * @param {string} fieldName - Name of the field
 * @param {string} message - Error message
 */
function showFieldError(fieldName, message) {
    const field = document.getElementById(fieldName);
    const formGroup = field.closest('.form-group');
    
    // Remove existing error
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error styling
    field.style.borderColor = '#f56565';
    
    // Add error message
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.color = '#f56565';
    errorElement.style.fontSize = '0.9rem';
    errorElement.style.marginTop = '0.5rem';
    errorElement.textContent = message;
    
    formGroup.appendChild(errorElement);
}

/**
 * Clear error message for a field
 * @param {string} fieldName - Name of the field
 */
function clearFieldError(fieldName) {
    const field = document.getElementById(fieldName);
    const formGroup = field.closest('.form-group');
    
    // Remove error styling
    field.style.borderColor = 'rgba(255, 255, 255, 0.3)';
    
    // Remove error message
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Show form loading state
 * @param {boolean} isLoading - Whether to show loading state
 */
function showFormLoading(isLoading) {
    const submitButton = document.querySelector('#contactForm button[type="submit"]');
    
    if (isLoading) {
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
        submitButton.style.opacity = '0.7';
    } else {
        submitButton.disabled = false;
        submitButton.textContent = 'Send Message';
        submitButton.style.opacity = '1';
    }
}

/**
 * Show form success message
 */
function showFormSuccess() {
    const form = document.getElementById('contactForm');
    
    // Create success message
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.style.cssText = `
        background: rgba(72, 187, 120, 0.2);
        color: #48bb78;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 500;
    `;
    successMessage.textContent = 'Thank you! Your message has been sent successfully.';
    
    // Insert success message at the top of the form
    form.insertBefore(successMessage, form.firstChild);
    
    // Remove success message after 5 seconds
    setTimeout(() => {
        successMessage.remove();
    }, 5000);
}

/* ===============================================
   SCROLL EFFECTS AND ANIMATIONS
   =============================================== */

/**
 * Initialize scroll-based effects and animations
 */
function initializeScrollEffects() {
    // Navbar background on scroll
    window.addEventListener('scroll', handleNavbarScroll);
    
    // Intersection Observer for fade-in animations
    initializeIntersectionObserver();
    
    // Parallax effect for hero section
    window.addEventListener('scroll', handleParallaxEffect);
}

/**
 * Handle navbar background change on scroll
 */
function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
}

/**
 * Initialize Intersection Observer for animations
 */
function initializeIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.project-card, .about-content, .contact-form');
    
    animateElements.forEach(el => {
        // Set initial state
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        // Start observing
        observer.observe(el);
    });
}

/**
 * Handle parallax effect for hero section
 */
function handleParallaxEffect() {
    const heroSection = document.querySelector('.hero-section');
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;
    
    if (heroSection && scrolled < window.innerHeight) {
        heroSection.style.transform = `translateY(${rate}px)`;
    }
}

/* ===============================================
   THEME TOGGLE FUNCTIONALITY
   =============================================== */

/**
 * Initialize theme toggle functionality (optional feature)
 */
function initializeThemeToggle() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('portfolioTheme');
    
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    }
    
    // You can add a theme toggle button here if needed
    // This is a placeholder for future theme switching functionality
}

/* ===============================================
   UTILITY FUNCTIONS
   =============================================== */

/**
 * Debounce function to limit function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} - Debounced function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function to limit function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} - Throttled function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/* ===============================================
   PORTFOLIO SPECIFIC FEATURES
   =============================================== */

/**
 * Initialize portfolio-specific features
 */
function initializePortfolioFeatures() {
    // Add click handlers for project cards
    initializeProjectCards();
    
    // Add resume download functionality
    initializeResumeDownload();
    
    // Add social media link tracking
    initializeSocialTracking();
}

/**
 * Initialize project card interactions
 */
function initializeProjectCards() {
    const projectCards = document.querySelectorAll('.project-card');
    
    projectCards.forEach(card => {
        const viewButton = card.querySelector('.btn-outline');
        
        if (viewButton) {
            viewButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // You can customize this to open project details
                // For now, it shows an alert
                const projectTitle = card.querySelector('.project-title').textContent;
                alert(`Opening project: ${projectTitle}\n\nYou can customize this to open a modal, navigate to project page, or open external link.`);
                
                console.log('Project viewed:', projectTitle);
            });
        }
    });
}

/**
 * Initialize resume download functionality
 */
function initializeResumeDownload() {
    const resumeButtons = document.querySelectorAll('.btn:contains("Resume")');
    
    // Note: You'll need to replace this with actual resume file
    const resumeURL = 'path/to/your/resume.pdf';
    
    resumeButtons.forEach(button => {
        if (button.textContent.includes('Resume')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Create temporary download link
                const link = document.createElement('a');
                link.href = resumeURL;
                link.download = 'Your_Name_Resume.pdf';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                console.log('Resume download initiated');
            });
        }
    });
}

/**
 * Initialize social media link tracking
 */
function initializeSocialTracking() {
    const socialLinks = document.querySelectorAll('.social-link');
    
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const platform = this.querySelector('i').className;
            console.log('Social link clicked:', platform);
            
            // You can add analytics tracking here
            // Example: gtag('event', 'social_click', { platform: platform });
        });
    });
}

/* ===============================================
   PERFORMANCE OPTIMIZATION
   =============================================== */

// Use throttled versions of scroll handlers for better performance
window.addEventListener('scroll', throttle(handleNavbarScroll, 16));
window.addEventListener('scroll', throttle(highlightActiveNavLink, 100));
window.addEventListener('scroll', throttle(handleParallaxEffect, 16));

// Initialize portfolio features when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePortfolioFeatures);

/* ===============================================
   ERROR HANDLING
   =============================================== */

/**
 * Global error handler for JavaScript errors
 */
window.addEventListener('error', function(e) {
    console.error('JavaScript error occurred:', e.error);
    
    // You can add error reporting here
    // Example: Send error to analytics or error reporting service
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    
    // Prevent the default browser behavior
    e.preventDefault();
});

/* ===============================================
   ACCESSIBILITY ENHANCEMENTS
   =============================================== */

/**
 * Enhance keyboard navigation
 */
document.addEventListener('keydown', function(e) {
    // Close mobile menu on Escape key
    if (e.key === 'Escape') {
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        
        if (hamburger && navMenu && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    }
});

/**
 * Improve focus management
 */
function improveFocusManagement() {
    // Add focus indicators for better accessibility
    const focusableElements = document.querySelectorAll(
        'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #667eea';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

// Initialize accessibility enhancements
document.addEventListener('DOMContentLoaded', improveFocusManagement);