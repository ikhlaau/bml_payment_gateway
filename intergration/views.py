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


def checkout(request):

    time.sleep(1)
    order_id = request.GET.get('order_id')
    order = ShopifyOrder.objects.filter(order_id=order_id).first()
    if order:
        pass
    else:
        if request.method == 'POST':
            body = request.body
            order_data = json.loads(body)
            shop_id = request.GET.get('shop_id')
            print(order_data)
            print(shop_id)
        else:
            return JsonResponse({'Error': 'Payment failed.'})

        

    if order.payment_status == 'pending_payment':
        return redirect(order.payment_url)
    elif order.payment_status in('pending_gateway_url','CANCELLED'):
        shop = Shopify.objects.filter(shop_name = order.shop_id).first()
        if order.presentment_currency == 'MVR':
            pg_amount = round(float(order.total_price) *100)
        else:
            pg_amount = round(float(order.total_price)*15.42*100)
        payment_details = {
            'amount': pg_amount,
            'currency': 'MVR',
            'customerReference':str(order.order_id),
            'localId':str(order.order_id),
            "redirectUrl":"https://bml-payment-gateway-zwkoz.ondigitalocean.app/payments/from_bml"
        }

        # Send request to your custom payment gatewa
        response = requests.post('https://api.merchants.bankofmaldives.com.mv/public/v2/transactions', json=payment_details, headers={"Authorization":shop.bml_key})
        payment_response = response.json()
        # print(payment_response)
        if response.status_code == 201:
            order.payment_url = payment_response['url']
            order.payment_status = 'pending_payment'
            order.gateway_id = payment_response['id']
            order.save()

        return redirect(order.payment_url)
    elif order.payment_status == 'CONFIRMED':
        return redirect(order.order_status_url)
    else:
        return JsonResponse({'Error': 'Payment failed.'})

def check_order_status(request):
    order_id = request.GET.get('order_id')
    order = ShopifyOrder.objects.filter(order_id=order_id).first()
    status = 'Not paid'
    if order:
        if order.payment_status == 'CONFIRMED':
            status  ='Paid'
    else:
        status  ='No order'
    return JsonResponse({'payment_status': status})


def from_bml(request):
    transactionId = request.GET.get('transactionId')
    state = request.GET.get('state')
    signature = request.GET.get('signature')
    if state == "CONFIRMED":
        order = ShopifyOrder.objects.filter(gateway_id=transactionId).first()
        shop =  Shopify.objects.filter(shop_name=order.shop_id).first()

        currency = 'MVR'

        if order.presentment_currency == 'MVR':
            mvr_amount = round(float(order.total_price) *100)
        else:
            mvr_amount = round(float(order.total_price)*15.42*100)

        check_signature_string = 'amount=' + str(mvr_amount) + '&currency=' + currency + '&apiKey='+shop.bml_key
        sha_1 = hashlib.sha1()
        sha_1.update(check_signature_string.encode('utf-8'))
        if signature ==sha_1.hexdigest():
            order.payment_status = state
            order.save()
            update_order_status(order)
            return redirect(order.order_status_url)
            
        else:
            return JsonResponse({'error':'Signature missmatch'})
    else:
        order = ShopifyOrder.objects.filter(gateway_id=transactionId).first()
        order.payment_status = state
        order.save()
        return redirect(order.order_status_url)

@csrf_exempt
def order_created(request):
    if request.method == 'POST':
        # Verify the webhook
        hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
        body = request.body
        # if not verify_webhook(hmac_header, body):
        #     return HttpResponse('Forbidden', status=403)

        order_data = json.loads(body)
        shop_id = request.GET.get('shop_id')
        order = ShopifyOrder.objects.filter(order_id=order_data['id']).first()

        if order:
            order.shop_id = shop_id
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
            order.save()
        else:            
            order = ShopifyOrder()
            order.order_id = order_data['id']
            order.shop_id = shop_id
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


def update_order_status(order):
    # status = 'paid' if payment_response.get('success') else 'failed'
    shop = Shopify.objects.filter(shop_name = order.shop_id).first()
    SHOPIFY_API_KEY = shop.api_key
    SHOP_NAME = shop.shop_name
    SHOPIFY_PASSWORD = shop.password
    order_id = order.order_id

    update_data = {
        'order': {
            'id': order.order_id,
            'financial_status':'paid',
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': SHOPIFY_PASSWORD
    }

    url = f'https://{SHOP_NAME}.myshopify.com/admin/api/2023-01/orders/{order_id}.json'
    # url = f'https://glamorgaze.shop/admin/api/2023-04/orders/{ORDER_ID}.json'

    print(url)
    response = requests.put(url, json=update_data,headers=headers)

    if response.status_code == 200:
        print('Order status updated:', response.json())
    else:
        print('Failed to update order status:', response.text)

def update_order_payment_url(order_id, payment_response):
    # status = 'paid' if payment_response.get('success') else 'failed'

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