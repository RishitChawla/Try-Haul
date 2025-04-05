function generateRandomOrderID() {
    return 'ORD-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}

let isSubmittingOrder = false;

function submitOrder() {
    if (isSubmittingOrder) return; // Prevent double submission
    isSubmittingOrder = true;

    console.log("Submit Order Clicked");
    const submitBtn = document.getElementById('continue-to-payment');
    submitBtn.disabled = true;

    // Select Address
    const selectedRadio = document.querySelector('.address-radio:checked');
    if (!selectedRadio) {
        alert('Please select a delivery address before continuing.');
        isSubmittingOrder = false;
        submitBtn.disabled = false;
        return;
    }

    // Collect customer details and order info
    const customerID = document.getElementById('customerID').value;
    if (!customerID) {
        alert("Customer ID missing.");
        isSubmittingOrder = false;
        submitBtn.disabled = false;
        return;
    }

    const orderAmount = parseFloat(document.getElementById('totalAmount').value);
    if (orderAmount <= 0 || isNaN(orderAmount)) {
        alert("Amount must be a valid number greater than 0.");
        isSubmittingOrder = false;
        submitBtn.disabled = false;
        return;
    }

    const discount = parseFloat(document.getElementById('discount').value || 0);
    const couponDiscount = parseFloat(document.getElementById('couponDiscount').value || 0);
    const orderId = generateRandomOrderID();
    sessionStorage.setItem("latestOrderId", orderId);

    const createOrderApiUrl = document.getElementById("createOrderApiUrl").value;
    if (!createOrderApiUrl) {
        alert("Create Order API URL not found.");
        isSubmittingOrder = false;
        submitBtn.disabled = false;
        return;
    }

    const orderData = {
        customer_details: {
            customer_id: customerID,
        },
        order_id: orderId,
        order_amount: orderAmount,
        selected_address: selectedRadio.id,
        discount: discount + couponDiscount,
        order_currency: "INR"
    };

    document.getElementById('loader').style.display = 'block';
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(createOrderApiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loader').style.display = 'none';
        isSubmittingOrder = false;
        submitBtn.disabled = false;

        console.log("Response from backend:", data);

        if (data.payment_session_id) {
            cashfree.checkout({
                paymentSessionId: data.payment_session_id,
                redirectTarget: "_self"
            });
        } else {
            alert('Order creation failed');
        }
    })
    .catch(error => {
        document.getElementById('loader').style.display = 'none';
        isSubmittingOrder = false;
        submitBtn.disabled = false;
        console.error('Error:', error);
    });
}
