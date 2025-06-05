/* ===============================================
   ENVER PORTFOLIO - JAVASCRIPT
   =============================================== */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initializeNavigation();
    initializeSmoothScrolling();
    initializeVideoPlayer();
    initializeAnimations();
    
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
 * Initialize video player interactions
 */
function initializeVideoPlayer() {
    const playButton = document.querySelector('.play-button');
    const videoContainer = document.querySelector('.video-container');
    
    if (playButton && videoContainer) {
        playButton.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'translate(-50%, -50%) scale(0.9)';
            
            setTimeout(() => {
                this.style.transform = 'translate(-50%, -50%) scale(1)';
            }, 150);
            
            // You can replace this with actual video functionality
            console.log('Video play button clicked');
            
            // Example: Show alert for demo purposes
            alert('Video would play here. You can replace this with actual video embed or modal.');
        });
        
        // Add hover effect for the entire video container
        videoContainer.addEventListener('mouseenter', function() {
            playButton.style.transform = 'translate(-50%, -50%) scale(1.1)';
        });
        
        videoContainer.addEventListener('mouseleave', function() {
            playButton.style.transform = 'translate(-50%, -50%) scale(1)';
        });
    }
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
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.why-content, .video-section');
    
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
    `;
    document.head.appendChild(style);
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