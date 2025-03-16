document.addEventListener("DOMContentLoaded", () => {
    // Set current year in footer
    document.getElementById("currentYear").textContent = new Date().getFullYear()
  
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById("mobileMenuBtn")
    const mobileMenu = document.getElementById("mobileMenu")
  
    mobileMenuBtn.addEventListener("click", () => {
      mobileMenu.classList.toggle("active")
  
      // Toggle icon between bars and X
      const icon = mobileMenuBtn.querySelector("i")
      if (icon.classList.contains("fa-bars")) {
        icon.classList.remove("fa-bars")
        icon.classList.add("fa-times")
      } else {
        icon.classList.remove("fa-times")
        icon.classList.add("fa-bars")
      }
    })
  
    // Hide secondary navbar on scroll    
    const secondaryNavbar = document.getElementById("secondaryNavbar")
    let lastScrollTop = 0

    window.addEventListener("scroll", () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop

        if (scrollTop > 50) {
        secondaryNavbar.classList.add("hidden")
        } else {
        secondaryNavbar.classList.remove("hidden")
        }

        lastScrollTop = scrollTop
    })
    
    // Close mobile menu when clicking outside
    document.addEventListener("click", (event) => {
      if (
        mobileMenu.classList.contains("active") &&
        !mobileMenu.contains(event.target) &&
        !mobileMenuBtn.contains(event.target)
      ) {
        mobileMenu.classList.remove("active")
  
        const icon = mobileMenuBtn.querySelector("i")
        icon.classList.remove("fa-times")
        icon.classList.add("fa-bars")
      }
    })
  
    // Category hover for desktop
    const categoryItems = document.querySelectorAll(".category-item")
  
    categoryItems.forEach((item) => {
      // For touch devices
      if ("ontouchstart" in window) {
        item.addEventListener("click", function (e) {
          const link = this.querySelector(".category-link")
          const dropdown = this.querySelector(".dropdown-menu")
  
          // If clicking the main category link (not a subcategory)
          if (e.target === link || link.contains(e.target)) {
            e.preventDefault()
  
            // Close all other dropdowns
            categoryItems.forEach((otherItem) => {
              if (otherItem !== item) {
                otherItem.classList.remove("active")
              }
            })
  
            // Toggle current dropdown
            this.classList.toggle("active")
          }
        })
      }
    })
  
    // Close dropdowns when clicking outside
    document.addEventListener("click", (e) => {
      const isClickInsideCategory = Array.from(categoryItems).some((item) => item.contains(e.target))
  
      if (!isClickInsideCategory) {
        categoryItems.forEach((item) => {
          item.classList.remove("active")
        })
      }
    })
  
    // Product card hover animations
    const productCards = document.querySelectorAll(".product-card")
  
    productCards.forEach((card) => {
      card.addEventListener("mouseenter", function () {
        const image = this.querySelector(".product-image img")
        image.style.transform = "scale(1.1)"
      })
  
      card.addEventListener("mouseleave", function () {
        const image = this.querySelector(".product-image img")
        image.style.transform = "scale(1)"
      })
    })
  
    // Spotlight item hover animations
    const spotlightItems = document.querySelectorAll(".spotlight-item")
  
    spotlightItems.forEach((item) => {
      item.addEventListener("mouseenter", function () {
        const image = this.querySelector(".spotlight-image-container img")
        image.style.transform = "scale(1.1)"
      })
  
      item.addEventListener("mouseleave", function () {
        const image = this.querySelector(".spotlight-image-container img")
        image.style.transform = "scale(1)"
      })
    })
  
    // Newsletter form submission
    const newsletterForm = document.querySelector(".newsletter-form")
  
    if (newsletterForm) {
      newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault()
        const emailInput = this.querySelector('input[type="email"]')
  
        if (emailInput.value) {
          // Here you would typically send this to your backend
          alert("Thank you for subscribing to our newsletter!")
          emailInput.value = ""
        }
      })
    }
  })
  
  