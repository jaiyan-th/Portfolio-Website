/**
 * Animation Controller for Portfolio Website
 * Handles scroll-based animations, hero animations, and interactive effects
 */

class AnimationController {
    constructor() {
        this.init();
    }

    init() {
        this.initializeHeroAnimations();
        this.initializeScrollAnimations();
        this.initializeInteractiveAnimations();
    }

    // Hero Section Animations
    initializeHeroAnimations() {
        // Staggered animation for hero elements
        const heroElements = [
            { selector: '#hero h1', delay: 0 },
            { selector: '#hero p:first-of-type', delay: 200 },
            { selector: '#hero p:last-of-type', delay: 400 },
            { selector: '#explore-work-btn', delay: 600 }
        ];

        heroElements.forEach(({ selector, delay }) => {
            const element = document.querySelector(selector);
            if (element) {
                // Set initial state
                element.style.opacity = '0';
                element.style.transform = 'translateY(30px)';
                element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';

                // Animate in with delay
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, delay);
            }
        });

        // Animate scroll indicator
        const scrollIndicator = document.querySelector('#hero .animate-bounce');
        if (scrollIndicator) {
            setTimeout(() => {
                scrollIndicator.style.opacity = '1';
                scrollIndicator.style.animation = 'bounce 2s infinite';
            }, 1000);
        }
    }

    // Scroll-based Animations
    initializeScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, observerOptions);

        // Observe sections and cards
        const animatedElements = document.querySelectorAll(
            'section:not(#hero), .card, .skill-badge, .project-card'
        );

        animatedElements.forEach(element => {
            observer.observe(element);
        });

        // Special handling for section titles
        const sectionTitles = document.querySelectorAll('section h2');
        sectionTitles.forEach(title => {
            observer.observe(title);
        });
    }

    // Animate individual elements
    animateElement(element) {
        if (element.classList.contains('animated')) return;

        element.classList.add('animated');
        
        // Different animations based on element type
        if (element.tagName === 'SECTION') {
            this.animateSection(element);
        } else if (element.tagName === 'H2') {
            this.animateSectionTitle(element);
        } else {
            this.animateCard(element);
        }
    }

    // Section animation
    animateSection(section) {
        const children = section.querySelectorAll('> *');
        children.forEach((child, index) => {
            child.style.opacity = '0';
            child.style.transform = 'translateY(20px)';
            child.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                child.style.opacity = '1';
                child.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Section title animation
    animateSectionTitle(title) {
        title.style.opacity = '0';
        title.style.transform = 'translateY(-20px)';
        title.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            title.style.opacity = '1';
            title.style.transform = 'translateY(0)';
        }, 100);
    }

    // Card animation
    animateCard(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px) scale(0.95)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
        }, Math.random() * 200);
    }

    // Interactive Animations
    initializeInteractiveAnimations() {
        // Button hover effects
        this.initializeButtonAnimations();
        
        // Card hover effects
        this.initializeCardAnimations();
        
        // Navigation animations
        this.initializeNavAnimations();
        
        // Theme toggle animation
        this.initializeThemeToggleAnimation();
    }

    // Button Animations
    initializeButtonAnimations() {
        const buttons = document.querySelectorAll('button, .btn-primary, a[class*="btn"]');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'scale(1.02) translateY(-2px)';
                button.style.boxShadow = '0 10px 25px rgba(255, 107, 53, 0.3)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'scale(1) translateY(0)';
                button.style.boxShadow = 'none';
            });
            
            button.addEventListener('mousedown', () => {
                button.style.transform = 'scale(0.98) translateY(0)';
            });
            
            button.addEventListener('mouseup', () => {
                button.style.transform = 'scale(1.02) translateY(-2px)';
            });
        });
    }

    // Card Animations
    initializeCardAnimations() {
        const cards = document.querySelectorAll('.card, [class*="card"]');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px) scale(1.01)';
                card.style.boxShadow = '0 20px 40px rgba(255, 107, 53, 0.1)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = 'none';
            });
        });
    }

    // Navigation Animations
    initializeNavAnimations() {
        const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
        
        navLinks.forEach(link => {
            link.addEventListener('mouseenter', () => {
                link.style.transform = 'translateY(-2px)';
            });
            
            link.addEventListener('mouseleave', () => {
                link.style.transform = 'translateY(0)';
            });
        });
    }

    // Theme Toggle Animation
    initializeThemeToggleAnimation() {
        const themeToggle = document.getElementById('theme-toggle');
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                // Add rotation animation
                const icon = themeToggle.querySelector('i');
                if (icon) {
                    icon.style.transform = 'rotate(360deg)';
                    icon.style.transition = 'transform 0.5s ease';
                    
                    setTimeout(() => {
                        icon.style.transform = 'rotate(0deg)';
                    }, 500);
                }
                
                // Add pulse effect to button
                themeToggle.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    themeToggle.style.transform = 'scale(1)';
                }, 200);
            });
        }
    }

    // Parallax Effect for Hero Background
    initializeParallax() {
        const hero = document.getElementById('hero');
        if (!hero) return;

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallaxSpeed = 0.5;
            
            hero.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        });
    }

    // Typing Animation for Hero Text
    initializeTypingAnimation(element, text, speed = 100) {
        if (!element) return;
        
        element.textContent = '';
        let i = 0;
        
        const typeWriter = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            }
        };
        
        typeWriter();
    }

    // Progress Bar Animation
    animateProgressBar(element, percentage, duration = 1000) {
        if (!element) return;
        
        element.style.width = '0%';
        element.style.transition = `width ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.width = `${percentage}%`;
        }, 100);
    }

    // Stagger Animation for Multiple Elements
    staggerAnimation(elements, delay = 100) {
        elements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * delay);
        });
    }
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.animationController = new AnimationController();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnimationController;
}