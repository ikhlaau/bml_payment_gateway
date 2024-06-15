from django.shortcuts import render
from intergration.models import *
import time
import hashlib

# Create your views here.
import hmac
import hashlib
import json
import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# Load your settings or environment variables
SHOPIFY_WEBHOOK_SECRET = 'b35fd35dabc267ac0b1e9f2a1c91b67a'
SHOPIFY_API_KEY = ' '
SHOPIFY_PASSWORD = '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'
SHOP_NAME = '2e3894-da'

def checkout(request):
    time.sleep(3)
    order_id = request.GET.get('order_id')
    order = ShopifyOrder.objects.filter(order_id=order_id).first()
    print(order)
    if order:
        pass
    else:
        time.sleep(5)
        order = ShopifyOrder.objects.filter(order_id=order_id).first()

    if order.payment_status == 'pending_payment':
        return redirect(order.payment_url)
    if order.payment_status == 'pending_gateway_url':
        payment_details = {
            'amount': round(float(order.total_price)*15.42*100),
            'currency': 'MVR',
            'customerReference':str(order.order_id),
            'localId':str(order.order_id),
            "redirectUrl":"https://bml-payment-gateway-zwkoz.ondigitalocean.app/payments/from_bml"
        }

        # Send request to your custom payment gatewa
        response = requests.post('https://api.merchants.bankofmaldives.com.mv/public/v2/transactions', json=payment_details, headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjM2ZTIwNzhlLWZhM2ItNGMyZi1iNDJlLWM5MDc4Njg5YWYyOSIsImNvbXBhbnlJZCI6IjYxMTgwNDA5ZmQ0NTRmMDAwODUyMmQ5MCIsImlhdCI6MTYyODk2Mzg0OSwiZXhwIjo0Nzg0NjM3NDQ5fQ.Y1Vvyf1BRrEjGSSfvkwPH0FUZtDvVFJ8vwoLmKVH7FU"})
        payment_response = response.json()
        # print(payment_response)
        if response.status_code == 201:
            order.payment_url = payment_response['url']
            order.payment_status = 'pending_payment'
            order.gateway_id = payment_response['id']
            order.save()
        return redirect(order.payment_url)

def check_order_status(request):
    order_id = request.GET.get('order_id')
    order = ShopifyOrder.objects.filter(order_id=order_id).first()

    return JsonResponse({'payment_status': order.payment_status})


def from_bml(request):

    transactionId = request.GET.get('transactionId')
    state = request.GET.get('state')
    signature = request.GET.get('signature')

    order = ShopifyOrder.objects.filter(gateway_id=transactionId).first()

    mvr_amount  =round(float(order.total_price)*15.42*100)
    currency = 'MVR'

    check_signature_string = 'amount=' + mvr_amount + '&currency=' + currency + '&apiKey=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjM2ZTIwNzhlLWZhM2ItNGMyZi1iNDJlLWM5MDc4Njg5YWYyOSIsImNvbXBhbnlJZCI6IjYxMTgwNDA5ZmQ0NTRmMDAwODUyMmQ5MCIsImlhdCI6MTYyODk2Mzg0OSwiZXhwIjo0Nzg0NjM3NDQ5fQ.Y1Vvyf1BRrEjGSSfvkwPH0FUZtDvVFJ8vwoLmKVH7FU'
    hash_object = hashlib.sha1(check_signature_string)
    pbHash = hash_object.hexdigest()
    return JsonResponse({'pbHash': pbHash,'transactionId':transactionId,'signature':signature})

@csrf_exempt
def order_created(request):
    if request.method == 'POST':
        # Verify the webhook
        hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
        body = request.body
        # if not verify_webhook(hmac_header, body):
        #     return HttpResponse('Forbidden', status=403)

        order_data = json.loads(body)

        order = ShopifyOrder()
        order.order_id = order_data['id']
        order.checkout_id = order_data['checkout_id']
        order.cart_token = order_data['cart_token']
        order.checkout_token = order_data['checkout_token']
        order.confirmation_number = order_data['confirmation_number']
        order.order_number = order_data['order_number']
        order.order_status_url = order_data['order_status_url']
        order.token = order_data['token']
        order.reference = order_data['reference']
        order.total_price = order_data['total_price']
        order.presentment_currency = order_data['presentment_currency']
        order.payment_status = 'pending_gateway_url'
        order.save()

        return HttpResponse('Webhook received', status=200)
    return HttpResponse('Method not allowed', status=405)

def verify_webhook(hmac_header, body):
    hash = hmac.new(SHOPIFY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    calculated_hmac = hash.hex()
    return hmac.compare_digest(calculated_hmac, hmac_header)

def process_payment(order_data):
    # Extract necessary details from order_data
    order = ShopifyOrder.objects.filter(order_id=order_data['id']).first()
    payment_details = {
        'amount': round(float(order.total_price)*15.42*100),
        'currency': 'MVR',
        'customerReference':str(order_data['id']),
        'localId':str(order_data['id']),
        "redirectUrl":"https://bml-payment-gateway-zwkoz.ondigitalocean.app/payments/from_bml"
    }

    # Send request to your custom payment gatewa
    response = requests.post('https://api.merchants.bankofmaldives.com.mv/public/v2/transactions', json=payment_details, headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjM2ZTIwNzhlLWZhM2ItNGMyZi1iNDJlLWM5MDc4Njg5YWYyOSIsImNvbXBhbnlJZCI6IjYxMTgwNDA5ZmQ0NTRmMDAwODUyMmQ5MCIsImlhdCI6MTYyODk2Mzg0OSwiZXhwIjo0Nzg0NjM3NDQ5fQ.Y1Vvyf1BRrEjGSSfvkwPH0FUZtDvVFJ8vwoLmKVH7FU"})
    payment_response = response.json()
    if response.status_code == 201:
        order.payment_url = payment_response['url']
        order.payment_status = 'pending_payment'
        order.save()
        print('Payment Success:')
    else:
        print('Payment failed:')
    # update_order_status(order_data['id'], payment_response['url'])


def update_order_status(order_id, payment_response):
    # status = 'paid' if payment_response.get('success') else 'failed'
    print(payment_response)
    update_data = {
        'order': {
            'id': order_id,
            'note_attributes': [
                    {
                        'name': "custom_redirect_url",
                        'value': payment_response
                    }
                ]
        }
    }

    url = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOP_NAME}.myshopify.com/admin/api/2023-01/orders/{order_id}.json'
    print(url)
    response = requests.put(url, json=update_data)

    if response.status_code == 200:
        print('Order status updated:', response.json())
    else:
        print('Failed to update order status:', response.text)
