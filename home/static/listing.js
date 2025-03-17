document.addEventListener('DOMContentLoaded', function() {
      
    // Toggle between secondary navbar and filter bar
    const secondaryNavbar = document.getElementById('secondaryNavbar');
    const filterBar = document.getElementById('filterBar');
    const filterToggleBtn = document.createElement('button');
    
    filterToggleBtn.classList.add('btn', 'secondary-btn');
    filterToggleBtn.style.position = 'fixed';
    filterToggleBtn.style.top = '90px';
    filterToggleBtn.style.left = '20px';
    filterToggleBtn.style.zIndex = '999';
    filterToggleBtn.textContent = 'Show Filters';
    
    document.body.appendChild(filterToggleBtn);
    
    filterToggleBtn.addEventListener('click', function() {
      if (filterBar.classList.contains('active')) {
        filterBar.classList.remove('active');
        secondaryNavbar.classList.remove('hidden');
        this.textContent = 'Show Filters';
      } else {
        filterBar.classList.add('active');
        secondaryNavbar.classList.add('hidden');
        this.textContent = 'Hide Filters';
      }
    });
    
    // Sort options
    const sortOptions = document.querySelectorAll('.sort-option');
    const currentSortText = document.getElementById('currentSort');
    
    sortOptions.forEach(option => {
      option.addEventListener('click', function() {
        // Remove active class from all options
        sortOptions.forEach(o => o.classList.remove('active'));
        
        // Add active class to clicked option
        this.classList.add('active');
        
        // Update current sort text
        currentSortText.textContent = this.textContent;
        
        // Here you would typically sort the products
        // For demo purposes, we'll just log the sort type
        console.log('Sorting by:', this.getAttribute('data-sort'));
      });
    });
    
    // Hide secondary navbar on scroll
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      if (scrollTop > 50 && !filterBar.classList.contains('active')) {
        secondaryNavbar.classList.add('hidden');
      } else if (scrollTop <= 50 && !filterBar.classList.contains('active')) {
        secondaryNavbar.classList.remove('hidden');
      }
      
      lastScrollTop = scrollTop;
    });
    
    // Pagination
    const pageItems = document.querySelectorAll('.page-item:not(.disabled)');
    
    pageItems.forEach(item => {
      item.addEventListener('click', function() {
        // Remove active class from all page items
        pageItems.forEach(p => p.classList.remove('active'));
        
        // Add active class to clicked page item
        this.classList.add('active');
        
        // Here you would typically load the products for the selected page
        // For demo purposes, we'll just log the page number
        console.log('Loading page:', this.textContent);
      });
    });
  });