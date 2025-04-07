document.addEventListener('DOMContentLoaded', () => {

    function generateRandomOrderID() {
        return 'ORD-' + Math.random().toString(36).substr(2, 9).toUpperCase();
    }

    let isSubmittingOrder = false;
    const cashfreeClientId = document.getElementById('cashfreeClientId').value; // Get Client ID from HTML

    function initiatePayment(orderToken) {
        if (typeof Cashfree !== "undefined" && typeof Cashfree.Element !== "undefined" && cashfreeClientId) {
            const cf = new Cashfree.Element({ clientId: cashfreeClientId });

            cf.element.init({
                paymentSessionId: orderToken,
            });

            const paymentFormContainer = document.getElementById('payment-form-container');
            if (paymentFormContainer) {
                cf.element.mount(paymentFormContainer, {
                    components: ['card', 'upi', 'netbanking', 'wallet'] // Adjust as needed
                });
            } else {
                console.error("Payment form container element not found.");
                alert('Error: Payment UI container not found.');
                return;
            }

            const placeOrderButton = document.getElementById('continue-to-payment');
            if (placeOrderButton) {
                placeOrderButton.addEventListener('click', async () => {
                    if (isSubmittingOrder) return; // Prevent double submission during payment
                    isSubmittingOrder = true;
                    document.getElementById('loader').style.display = 'block'; // Show loader during payment

                    try {
                        const result = await cf.element.submitPayment();
                        document.getElementById('loader').style.display = 'none'; // Hide loader after payment attempt
                        isSubmittingOrder = false;

                        if (result.paymentId) {
                            console.log("Payment Successful:", result);
                            // Redirect to success page or update UI
                            window.location.href = '/payment-success/'; // Adjust URL as needed
                        } else if (result.error) {
                            console.error("Payment Failed:", result.error);
                            alert(`Payment Failed: ${result.error.message}`);
                            // Handle payment failure (e.g., display error message to user)
                        }
                    } catch (error) {
                        document.getElementById('loader').style.display = 'none'; // Ensure loader is hidden on error
                        isSubmittingOrder = false;
                        console.error("Error submitting payment:", error);
                        alert("An unexpected error occurred during payment.");
                    }
                });
            } else {
                console.error("Place order button not found.");
            }

        } else {
            console.error("Cashfree Element SDK is not initialized or Client ID is missing.");
            alert('Payment initiation failed due to SDK or configuration issue.');
        }
    }

    async function submitOrder() {
        if (isSubmittingOrder) return; // Prevent double submission
        isSubmittingOrder = true;

        console.log("Submit Order Clicked");

        const selectedRadio = document.querySelector('.address-radio:checked');
        if (!selectedRadio) {
            alert('Please select a delivery address before continuing.');
            isSubmittingOrder = false;
            return;
        }
        console.log("Selected Address ID:", selectedRadio.id);

        const customerID = document.getElementById('customerID').value;
        if (!customerID) {
            alert("Customer ID missing.");
            isSubmittingOrder = false;
            return;
        }

        const orderAmount = parseFloat(document.getElementById('totalAmount').value);
        if (isNaN(orderAmount) || orderAmount <= 0) {
            alert("Please enter a valid amount.");
            isSubmittingOrder = false;
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

        try {
            const response = await fetch(createOrderApiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(orderData)
            });

            const data = await response.json();
            document.getElementById('loader').style.display = 'none';
            console.log("Response from backend:", data);

            if (data.payment_session_id) {
                initiatePayment(data.payment_session_id); // Call Element initiation
            } else {
                alert('Order creation failed.');
                isSubmittingOrder = false;
            }

        } catch (error) {
            document.getElementById('loader').style.display = 'none';
            console.error('Error:', error);
            alert("Something went wrong.");
            isSubmittingOrder = false;
        }
    }

    window.submitOrder = submitOrder;

});