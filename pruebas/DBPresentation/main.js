let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const progressBar = document.getElementById('progress-bar');
const currentSlideText = document.getElementById('current-slide');
const totalSlidesText = document.getElementById('total-slides');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

// Initialize
totalSlidesText.innerText = slides.length;
updateSlide(0);

// Functions
function updateSlide(index) {
    // Boundary check
    if (index < 0) index = 0;
    if (index >= slides.length) index = slides.length - 1;

    // Manage active classes
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) {
            slide.classList.add('active');
        }
    });

    currentSlide = index;
    
    // Update UI elements
    const progress = ((index + 1) / slides.length) * 100;
    progressBar.style.width = `${progress}%`;
    currentSlideText.innerText = index + 1;

    // Manage button states
    prevBtn.style.opacity = index === 0 ? '0.3' : '1';
    prevBtn.style.cursor = index === 0 ? 'default' : 'pointer';
    nextBtn.style.opacity = index === slides.length - 1 ? '0.3' : '1';
    nextBtn.style.cursor = index === slides.length - 1 ? 'default' : 'pointer';
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        updateSlide(currentSlide + 1);
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        updateSlide(currentSlide - 1);
    }
}

function goToSlide(slideNumber) {
    updateSlide(slideNumber - 1);
}

// Event Listeners
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        prevSlide();
    }
});

// Optional: Mouse wheel navigation
let wheelTimeout;
document.addEventListener('wheel', (e) => {
    clearTimeout(wheelTimeout);
    wheelTimeout = setTimeout(() => {
        if (e.deltaY > 50) nextSlide();
        if (e.deltaY < -50) prevSlide();
    }, 100);
});

// Touch support for mobile
let touchstartX = 0;
let touchendX = 0;

function checkDirection() {
    if (touchendX < touchstartX - 50) nextSlide();
    if (touchendX > touchstartX + 50) prevSlide();
}

document.addEventListener('touchstart', e => {
    touchstartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchendX = e.changedTouches[0].screenX;
    checkDirection();
});
