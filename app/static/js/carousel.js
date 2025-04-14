let slideIndex = 0;
let autoSlideInterval;
let isAnimating = false;
let startX = 0;
let endX = 0;

function updateCarousel() {
    const slides = document.querySelectorAll('.carousel-item');
    const track = document.querySelector('.carousel-track');
    const container = document.querySelector('.carousel');
    const indicatorsContainer = document.querySelector('.carousel-indicators');

    if (!indicatorsContainer) {
        console.error("Error: .carousel-indicators element not found!");
        return;
    }

    if (slides.length === 0) {
        console.error("Error: No slides found!");
        indicatorsContainer.textContent = "No items available.";
        return;
    }

    slideIndex = (slideIndex + slides.length) % slides.length;

    const containerWidth = container.offsetWidth;

    // Set each slide width to match container
    slides.forEach(slide => {
        slide.style.width = `${containerWidth}px`;
    });

    // Set track width to fit all slides
    track.style.width = `${containerWidth * slides.length}px`;

    // Move track to current slide
    track.style.transform = `translateX(-${containerWidth * slideIndex}px)`;

    indicatorsContainer.textContent = `Album ${slideIndex + 1} of ${slides.length}`;
}


function moveSlide(n) {
    if (isAnimating) return;
    const slides = document.querySelectorAll('.carousel-item');
    if (slides.length === 0) return;

    isAnimating = true;
    slideIndex = (slideIndex + n + slides.length) % slides.length;
    updateCarousel();
    resetAutoSlide();
    setTimeout(() => (isAnimating = false), 500);
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => moveSlide(1), 15000);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

function handleSwipeStart(e) {
    startX = e.touches ? e.touches[0].clientX : e.clientX;
}

function handleSwipeEnd(e) {
    endX = e.changedTouches ? e.changedTouches[0].clientX : e.clientX;
    const deltaX = endX - startX;
    if (Math.abs(deltaX) > 50) {
        moveSlide(deltaX > 0 ? -1 : 1);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll('.carousel-item');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    const track = document.querySelector('.carousel-track');

    if (!indicatorsContainer) {
        console.error("Error: .carousel-indicators div not found in DOM!");
        return;
    }

    if (slides.length > 0) {
        updateCarousel();
        startAutoSlide();
    } else {
        indicatorsContainer.textContent = "No items available.";
    }

    const carousel = document.querySelector('.carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
        carousel.addEventListener('mouseleave', startAutoSlide);

        // Swipe event listeners
        carousel.addEventListener('touchstart', handleSwipeStart);
        carousel.addEventListener('touchend', handleSwipeEnd);
    }
});
