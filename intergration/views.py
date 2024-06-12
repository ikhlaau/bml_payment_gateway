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
SHOPIFY_WEBHOOK_SECRET = 'b35fd35dabc267ac0b1e9f2a1c91b67a'
SHOPIFY_API_KEY = '6e6e4347ad0221e2fb799d32ba4a7e25'
SHOPIFY_PASSWORD = 'your-shopify-password'
SHOP_NAME = '2e3894-da'

def hello(requests):
    return HttpResponse("return this string")

@csrf_exempt
def order_created(request):
    if request.method == 'POST':
        # Verify the webhook
        hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
        body = request.body
        print(body)
        # if not verify_webhook(hmac_header, body):
        #     return HttpResponse('Forbidden', status=403)

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
        'amount': (float(order_data['total_price'])*100),
        'currency': order_data['currency'],
        # 'customer_info': order_data['customer'],
        'customerReference':order_data['id'],
        'localId':order_data['id'],
        "redirectUrl":"https://google.com/test/1"
        # Additional details as required by your payment gateway
    }
    print(payment_details)

    # Send request to your custom payment gatewa
    response = requests.post('https://api.merchants.bankofmaldives.com.mv/public/v2/transactions', json=payment_details, headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjM2ZTIwNzhlLWZhM2ItNGMyZi1iNDJlLWM5MDc4Njg5YWYyOSIsImNvbXBhbnlJZCI6IjYxMTgwNDA5ZmQ0NTRmMDAwODUyMmQ5MCIsImlhdCI6MTYyODk2Mzg0OSwiZXhwIjo0Nzg0NjM3NDQ5fQ.Y1Vvyf1BRrEjGSSfvkwPH0FUZtDvVFJ8vwoLmKVH7FU"})
    if response.status_code == 200:
        payment_response = response.json()
        print(payment_response)
        return redirect(payment_response['url'])
        # update_order_status(order_data['id'], payment_response)
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
