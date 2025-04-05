document.addEventListener('DOMContentLoaded', function() {
    
    // Select the button properly
    const continueToPaymentBtn = document.getElementById('continue-to-payment');
    
    if (!continueToPaymentBtn) {
        console.error('Error: #continue-to-payment button not found.');
        return;  // Exit script if the button is not found
    }
    
    // Ensure the selected address input field exists
    const selectedAddressInput = document.getElementById('selectedAddress');
    if (!selectedAddressInput) {
      console.error('Error: #selectedAddress input field not found.');
      return;
    }else{
      console.log("selected Address: ",selectedAddressInput)
    }
    
    
    // Address selection functionality
    const addressRadios = document.querySelectorAll('.address-radio');
    addressRadios.forEach(radio => {
      radio.addEventListener('change', function() {
        document.querySelectorAll('.address-card').forEach(card => {
          card.classList.remove('selected');
        });
        this.closest('.address-card').classList.add('selected');
      });
    });

    // Add new address toggle
    const addAddressBtn = document.getElementById('add-address-btn');
    if (addAddressBtn) {
      const addressForm = document.getElementById('address-form-container');
      
      addAddressBtn.addEventListener('click', function(e) {
        e.preventDefault();
        addressForm.classList.toggle('ishidden');
        this.textContent = addressForm.classList.contains('ishidden') ? 'Add New Address' : 'Cancel';
      });
    }

    window.onload = function () {
        const orderButton = document.getElementById("continue-to-payment");
        if (orderButton) {
            orderButton.addEventListener("click", function() {
                if (typeof submitOrder === "function") {
                    submitOrder();
                } else {
                    console.error("submitOrder function is not defined!");
                }
            });
        } else {
            console.error("Order button not found!");
        }
    };

  });