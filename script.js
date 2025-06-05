/* ===============================================
   ENVER PORTFOLIO - ENHANCED JAVASCRIPT WITH 3D EFFECTS
   =============================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initializeNavigation();
    initializeSmoothScrolling();
    initializeFormHandling();
    initializeAnimations();
    initialize3DEffects();
    initializeParallax();
    
    console.log('Enver website initialized successfully!');
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
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (hamburger && navMenu && 
            !hamburger.contains(e.target) && 
            !navMenu.contains(e.target) &&
            navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
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
   VIDEO PLAYER FUNCTIONALITY
   =============================================== */

/**
 * Initialize form handling with validation
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
        
        // Simulate form submission
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
 */
function validateForm(name, email, message) {
    let isValid = true;
    
    if (!name || name.trim().length < 2) {
        showFieldError('name', 'Name must be at least 2 characters long');
        isValid = false;
    }
    
    if (!email || !isValidEmail(email)) {
        showFieldError('email', 'Please enter a valid email address');
        isValid = false;
    }
    
    if (!message || message.trim().length < 10) {
        showFieldError('message', 'Message must be at least 10 characters long');
        isValid = false;
    }
    
    return isValid;
}

/**
 * Check if email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show error message for a field
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
    field.style.borderColor = '#e53e3e';
    
    // Add error message
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.color = '#e53e3e';
    errorElement.style.fontSize = '0.9rem';
    errorElement.style.marginTop = '0.5rem';
    errorElement.textContent = message;
    
    formGroup.appendChild(errorElement);
}

/**
 * Clear error message for a field
 */
function clearFieldError(fieldName) {
    if (typeof fieldName === 'object') {
        fieldName = fieldName.target.name;
    }
    
    const field = document.getElementById(fieldName);
    if (!field) return;
    
    const formGroup = field.closest('.form-group');
    
    // Remove error styling
    field.style.borderColor = 'rgba(45, 55, 72, 0.2)';
    
    // Remove error message
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Validate individual field on blur
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
 * Show form loading state
 */
function showFormLoading(isLoading) {
    const submitButton = document.querySelector('#contactForm button[type="submit"]');
    
    if (submitButton) {
        if (isLoading) {
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...';
            submitButton.style.opacity = '0.7';
        } else {
            submitButton.disabled = false;
            submitButton.textContent = 'Send';
            submitButton.style.opacity = '1';
        }
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
        background: rgba(72, 187, 120, 0.1);
        color: #38a169;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 500;
        border: 1px solid rgba(72, 187, 120, 0.2);
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
   ANIMATIONS AND SCROLL EFFECTS
   =============================================== */

/**
 * Initialize scroll-based animations
 */
function initializeAnimations() {
    // Initialize Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Add staggered animation for project cards
                if (entry.target.classList.contains('project-card')) {
                    const index = Array.from(entry.target.parentNode.children).indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.2}s`;
                }
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.project-card, .contact-form-wrapper, .hero-content, .hero-image');
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Add CSS classes for animations
    addAnimationStyles();
}

/**
 * Add animation styles dynamically
 */
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            animation: fadeInUp 0.8s ease-out forwards;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .tilt-active {
            transform: perspective(1000px) rotateX(10deg) rotateY(10deg) scale(1.05);
        }
        
        .parallax-element {
            transition: transform 0.1s ease-out;
        }
    `;
    document.head.appendChild(style);
}

/* ===============================================
   3D EFFECTS AND INTERACTIONS
   =============================================== */

/**
 * Initialize advanced 3D effects for project cards and elements
 */
function initialize3DEffects() {
    // Enhanced 3D tilt effect for project cards
    const projectCards = document.querySelectorAll('.project-card[data-tilt]');
    
    projectCards.forEach(card => {
        card.addEventListener('mousemove', handleCardMouseMove);
        card.addEventListener('mouseenter', handleCardMouseEnter);
        card.addEventListener('mouseleave', handleCardMouseLeave);
    });
    
    // 3D hover effects for buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', handleButtonHover);
        button.addEventListener('mouseleave', handleButtonLeave);
    });
    
    // 3D effects for hero card
    const heroCard = document.querySelector('.hero-card');
    if (heroCard) {
        heroCard.addEventListener('mousemove', handleHeroCardMove);
        heroCard.addEventListener('mouseleave', handleHeroCardLeave);
    }
}

/**
 * Handle mouse movement over project cards for 3D tilt effect
 */
function handleCardMouseMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / 10;
    const rotateY = (centerX - x) / 10;
    
    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    
    // Apply subtle 3D effect to image container
    const imageContainer = card.querySelector('.image-3d-container');
    if (imageContainer) {
        imageContainer.style.transform = `perspective(500px) rotateY(${rotateY / 2}deg) scale(1.05)`;
    }
}

/**
 * Handle mouse enter on project cards
 */
function handleCardMouseEnter(e) {
    const card = e.currentTarget;
    card.style.transition = 'transform 0.1s ease-out, box-shadow 0.3s ease';
    card.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.2)';
}

/**
 * Handle mouse leave on project cards
 */
function handleCardMouseLeave(e) {
    const card = e.currentTarget;
    card.style.transition = 'transform 0.4s ease, box-shadow 0.3s ease';
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
    
    // Reset image container
    const imageContainer = card.querySelector('.image-3d-container');
    if (imageContainer) {
        imageContainer.style.transform = 'perspective(500px) rotateY(-5deg)';
    }
}

/**
 * Handle button hover effects
 */
function handleButtonHover(e) {
    const button = e.currentTarget;
    button.style.transform = 'translateY(-3px) scale(1.05)';
    button.style.transition = 'all 0.3s ease';
}

/**
 * Handle button leave effects
 */
function handleButtonLeave(e) {
    const button = e.currentTarget;
    if (button.classList.contains('btn-primary')) {
        button.style.transform = 'translateY(-2px) scale(1)';
    } else {
        button.style.transform = 'translateY(0px) scale(1)';
    }
}

/**
 * Handle hero card mouse movement
 */
function handleHeroCardMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    const rotateX = (y - centerY) / 20;
    const rotateY = (centerX - x) / 20;
    
    card.style.transform = `rotate(-15deg) perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
}

/**
 * Handle hero card mouse leave
 */
function handleHeroCardLeave(e) {
    const card = e.currentTarget;
    card.style.transform = 'rotate(-15deg) perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
}

/* ===============================================
   PARALLAX SCROLLING EFFECTS
   =============================================== */

/**
 * Initialize parallax scrolling effects
 */
function initializeParallax() {
    // Parallax for decorative elements
    const decorativeElements = document.querySelectorAll('.decoration, .mobile-decoration');
    
    // Throttled scroll handler for performance
    let ticking = false;
    
    function updateParallax() {
        const scrollTop = window.pageYOffset;
        
        decorativeElements.forEach((element, index) => {
            const speed = 0.5 + (index * 0.1); // Different speeds for different elements
            const yPos = -(scrollTop * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
        
        // Parallax for hero section
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const heroOffset = scrollTop * 0.3;
            heroSection.style.transform = `translateY(${heroOffset}px)`;
        }
        
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // Mouse parallax for hero image
    initializeMouseParallax();
}

/**
 * Initialize mouse-based parallax effects
 */
function initializeMouseParallax() {
    const heroImage = document.querySelector('.hero-image');
    
    if (heroImage) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth) * 100;
            const y = (e.clientY / window.innerHeight) * 100;
            
            const decorations = heroImage.querySelectorAll('.decoration');
            decorations.forEach((decoration, index) => {
                const speed = 0.02 + (index * 0.01);
                const xOffset = (x - 50) * speed;
                const yOffset = (y - 50) * speed;
                
                decoration.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
            });
        });
    }
}

/* ===============================================
   BUTTON INTERACTIONS
   =============================================== */

/**
 * Initialize button interactions
 */
function initializeButtons() {
    // Service buttons
    const serviceButtons = document.querySelectorAll('.btn-primary');
    
    serviceButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add click animation
            this.style.transform = 'translateY(-2px) scale(0.98)';
            
            setTimeout(() => {
                this.style.transform = 'translateY(-2px) scale(1)';
            }, 150);
            
            // Handle button action based on text content
            const buttonText = this.textContent.trim();
            
            if (buttonText.includes('Our Services')) {
                console.log('Services button clicked');
                // You can add navigation to services section here
                // For example: scrollToSection('#services');
                
                // Demo alert
                alert('Services section would be shown here. You can customize this behavior.');
            }
        });
    });
    
    // Contact button
    const contactButton = document.querySelector('.btn-outline');
    
    if (contactButton) {
        contactButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            console.log('Contact button clicked');
            
            // Demo alert - you can replace with actual contact functionality
            alert('Contact form or modal would open here. You can customize this behavior.');
        });
    }
}

/* ===============================================
   UTILITY FUNCTIONS
   =============================================== */

/**
 * Scroll to a specific section
 * @param {string} selector - CSS selector for the target section
 */
function scrollToSection(selector) {
    const targetSection = document.querySelector(selector);
    if (targetSection) {
        const offsetTop = targetSection.offsetTop - 80;
        
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

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

/* ===============================================
   RESPONSIVE BEHAVIOR
   =============================================== */

/**
 * Handle window resize events
 */
function handleResize() {
    const mobileBreakpoint = 768;
    const windowWidth = window.innerWidth;
    
    // Close mobile menu on resize to desktop
    if (windowWidth > mobileBreakpoint) {
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        
        if (hamburger && navMenu) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    }
}

// Add resize event listener with debouncing
window.addEventListener('resize', debounce(handleResize, 250));

/* ===============================================
   PERFORMANCE OPTIMIZATIONS
   =============================================== */

/**
 * Initialize performance optimizations
 */
function initializePerformanceOptimizations() {
    // Lazy load images when they come into view
    const images = document.querySelectorAll('img');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                // Optimize image loading
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

/* ===============================================
   ACCESSIBILITY ENHANCEMENTS
   =============================================== */

/**
 * Enhance keyboard navigation and accessibility
 */
function enhanceAccessibility() {
    // Handle keyboard navigation for mobile menu
    document.addEventListener('keydown', function(e) {
        // Close mobile menu on Escape key
        if (e.key === 'Escape') {
            const hamburger = document.querySelector('.hamburger');
            const navMenu = document.querySelector('.nav-menu');
            
            if (hamburger && navMenu && navMenu.classList.contains('active')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                hamburger.focus(); // Return focus to hamburger button
            }
        }
    });
    
    // Improve focus management for interactive elements
    const focusableElements = document.querySelectorAll(
        'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #6366f1';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

/* ===============================================
   INITIALIZATION
   =============================================== */

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSmoothScrolling();
    initializeVideoPlayer();
    initializeAnimations();
    initializeButtons();
    initializePerformanceOptimizations();
    enhanceAccessibility();
    
    console.log('Enver website fully initialized!');
});

/* ===============================================
   ERROR HANDLING
   =============================================== */

/**
 * Global error handler
 */
window.addEventListener('error', function(e) {
    console.error('JavaScript error occurred:', e.error);
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    e.preventDefault();
});