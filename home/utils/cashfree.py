import requests
from django.conf import settings

CASHFREE_BASE_URL = "https://sandbox.cashfree.com/pg/orders" if settings.CASHFREE_ENVIRONMENT == "TEST" else "https://api.cashfree.com/pg/orders"

def create_cashfree_order(order_id, amount, customer_email, customer_phone):
    headers = {
        "accept": "application/json",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY,
        "x-api-version": "2022-09-01",
        "content-type": "application/json"
    }

    data = {
        "order_id": order_id,
        "order_amount": amount,
        "order_currency": "INR",
        "customer_details": {
            "customer_id": "cust_" + str(order_id),
            "customer_email": customer_email,
            "customer_phone": customer_phone
        },
        "order_meta": {
            "return_url": "http://127.0.0.1:8000/payment-success/?order_id=" + order_id,
            "notify_url": "http://127.0.0.1:8000/payment-webhook/"
        }
    }

    response = requests.post(CASHFREE_BASE_URL, json=data, headers=headers)
    
    print("Cashfree API Response:", response.status_code, response.text)  # Debugging

    return response.json()
