let slideIndex = 0;
let autoSlideInterval;

function updateCarousel() {
    let slides = document.querySelectorAll('.carousel-item');
    let indicatorsContainer = document.querySelector('.carousel-indicators');

    if (!indicatorsContainer) {
        console.error("Error: .carousel-indicators element not found!");
        return;
    }

    if (slides.length === 0) {
        console.error("Error: No slides found!");
        indicatorsContainer.textContent = "No items available.";
        return;
    }

    // Remove 'active' class from all items
    slides.forEach(slide => slide.classList.remove('active'));

    // Add 'active' class to the current slide
    slides[slideIndex].classList.add('active');

    // Update the indicator text to show "Album X of Y"
    indicatorsContainer.textContent = `Album ${slideIndex + 1} of ${slides.length}`;
    console.log(`Updated indicator: Album ${slideIndex + 1} of ${slides.length}`);
}

function moveSlide(n) {
    let slides = document.querySelectorAll('.carousel-item');
    if (slides.length === 0) return;

    slideIndex = (slideIndex + n + slides.length) % slides.length;
    updateCarousel();
    resetAutoSlide();
}

function startAutoSlide() {
    autoSlideInterval = setInterval(() => {
        moveSlide(1);
    }, 15000);
}

function resetAutoSlide() {
    clearInterval(autoSlideInterval);
    startAutoSlide();
}

// Initialize carousel
document.addEventListener("DOMContentLoaded", () => {
    let slides = document.querySelectorAll('.carousel-item');
    let indicatorsContainer = document.querySelector('.carousel-indicators');

    if (!indicatorsContainer) {
        console.error("Error: .carousel-indicators div not found in DOM!");
        return;
    }

    if (slides.length > 0) {
        indicatorsContainer.textContent = `Album 1 of ${slides.length}`;
        updateCarousel();
        startAutoSlide();
    } else {
        indicatorsContainer.textContent = "No items available.";
    }

    let carousel = document.querySelector('.carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
        carousel.addEventListener('mouseleave', startAutoSlide);
    }
});
