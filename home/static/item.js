document.addEventListener("DOMContentLoaded", () => {
// Product Thumbnails
const thumbnails = document.querySelectorAll('.thumbnail');
const mainImage = document.getElementById('mainImage');

let firstThumbnail = document.querySelector(".thumbnail");
if (firstThumbnail) {
    firstThumbnail.classList.add("active");
}

thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', function() {
    // Remove active class from all thumbnails
    thumbnails.forEach(t => t.classList.remove('active'));
    
    // Add active class to clicked thumbnail
    this.classList.add('active');
    
    // Update main image
    const imageUrl = this.getAttribute('data-image');
    mainImage.src = imageUrl;
    });
});

// Color Selection
const colorOptions = document.querySelectorAll('.color-option');

colorOptions.forEach(option => {
    option.addEventListener('click', function() {
    // Remove active class from all color options
    colorOptions.forEach(o => o.classList.remove('active'));
    
    // Add active class to clicked option
    this.classList.add('active');
    });
});

// Size Selection
const sizeOptions = document.querySelectorAll('.size-option');

sizeOptions.forEach(option => {
    option.addEventListener('click', function() {
    // Remove active class from all size options
    sizeOptions.forEach(o => o.classList.remove('active'));
    
    // Add active class to clicked option
    this.classList.add('active');
    });
});

// Wishlist Button Toggle
const wishlistBtn = document.querySelector('.wishlist-action-btn');

if (wishlistBtn) {
    wishlistBtn.addEventListener('click', function() {
    this.classList.toggle('active');
    });
}

// Accordion Functionality
const accordionHeaders = document.querySelectorAll('.accordion-header');

accordionHeaders.forEach(header => {
    header.addEventListener('click', function() {
    const accordionItem = this.parentElement;
    accordionItem.classList.toggle('active');
    });
});

// Size Guide Modal
const sizeGuideLink = document.getElementById('sizeGuideLink');
const sizeGuideModal = document.getElementById('sizeGuideModal');
const modalClose = document.getElementById('modalClose');

if (sizeGuideLink && sizeGuideModal && modalClose) {
    sizeGuideLink.addEventListener('click', function() {
    sizeGuideModal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
    });
    
    modalClose.addEventListener('click', function() {
    sizeGuideModal.classList.remove('active');
    document.body.style.overflow = ''; // Re-enable scrolling
    });
    
    // Close modal when clicking outside
    sizeGuideModal.addEventListener('click', function(e) {
    if (e.target === sizeGuideModal) {
        sizeGuideModal.classList.remove('active');
        document.body.style.overflow = '';
    }
    });
}
});