from django.shortcuts import render

# Create your views here.
import hmac
import hashlib
import json
import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Load your settings or environment variables
SHOPIFY_WEBHOOK_SECRET = 'your-shopify-webhook-secret'
SHOPIFY_API_KEY = 'your-shopify-api-key'
SHOPIFY_PASSWORD = 'your-shopify-password'
SHOP_NAME = 'your-shop-name'

def hello(requests):
    return HttpResponse("return this string")

@csrf_exempt
def order_created(request):
    if request.method == 'POST':
        # Verify the webhook
        hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
        body = request.body
        print(body)
        if not verify_webhook(hmac_header, body):
            return HttpResponse('Forbidden', status=403)

        # Process the order data and initiate payment
        order_data = json.loads(body)
        process_payment(order_data)

        return HttpResponse('Webhook received', status=200)

    return HttpResponse('Method not allowed', status=405)

def verify_webhook(hmac_header, body):
    hash = hmac.new(SHOPIFY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    calculated_hmac = hash.hex()
    return hmac.compare_digest(calculated_hmac, hmac_header)

def process_payment(order_data):
    # Extract necessary details from order_data
    payment_details = {
        'amount': order_data['total_price'],
        'currency': order_data['currency'],
        'customer_info': order_data['customer'],
        # Additional details as required by your payment gateway
    }
    print(order_data)

    # Send request to your custom payment gateway
    response = requests.post('https://your-payment-gateway.com/api/payments', json=payment_details)
    
    if response.status_code == 200:
        payment_response = response.json()
        update_order_status(order_data['id'], payment_response)
    else:
        print('Payment failed:', response.text)

def update_order_status(order_id, payment_response):
    status = 'paid' if payment_response.get('success') else 'failed'

    update_data = {
        'order': {
            'id': order_id,
            'financial_status': status
        }
    }

    url = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2023-01/orders/{order_id}.json'
    response = requests.put(url, json=update_data)

    if response.status_code == 200:
        print('Order status updated:', response.json())
    else:
        print('Failed to update order status:', response.text)
