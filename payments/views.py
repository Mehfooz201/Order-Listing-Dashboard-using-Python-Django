from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from amruloapp.models import Order
from payments.models import Payment
from forex_python.converter import CurrencyRates, RatesNotAvailableError
import json
from django.http import JsonResponse
# Create your views here.


@login_required(login_url='login')
def main_order_payment_request(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, order_number=body['orderID'])

    # Order paid by customer, so is_ordered field will be true
    order.order_is_paid = True
    order.save()

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        order_id = body['orderID'],
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        payment_type = "main_order",
        amount_paid = body['amount_paid'],
        currency = body['currency'],
        status = body['status'],
    )
    payment.save()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

@login_required(login_url='login')
def main_order_billing_page(request ,order_num, price=0):
    current_user = request.user

    # Fetch the actual exchange rate for INR
    try:
        c = CurrencyRates()
        inr_rate = c.get_rate('USD', 'INR')
    except RatesNotAvailableError:
        pass
    inr_rate = 83.12
    
    order = Order.objects.get(user=request.user, order_number=order_num)
    price = order.price
    price_inr = order.price
    order_currency = order.currency

    if order.currency == 'INR':
        if price_inr > 0:
            price_inr = '%.2f'%float(float(price)/float(inr_rate))
    else:
        price_inr = order.price

    context = {
        'inr_rate': inr_rate,
        'order': order,
        'order_currency': order_currency,
        'price': float(price),
        'price_inr': float(price_inr),
    }

    return render(request, 'amruloapp/dashboard/main_order_billing_page.html', context)

@login_required(login_url='login')
def main_order_payment_complete(request):
    return render(request, 'amruloapp/dashboard/main_order_payment_complete.html')

@login_required(login_url='login')
def additional_price_payment_request(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, order_number=body['orderID'])

    # Order paid by customer, so is_ordered field will be true
    order.add_price_is_paid = True
    _remake_price = order.remake_price
    _price = order.price
    order.price = _remake_price + _price
    order.remake_price = 0
    order.order_status = 'review'
    order.save()

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        order_id = body['orderID'],
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        payment_type = "additional_price",
        amount_paid = body['amount_paid'],
        currency = body['currency'],
        status = body['status'],
    )
    payment.save()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

@login_required(login_url='login')
def additional_price_billing_page(request ,order_num, price=0):
    current_user = request.user

    # Fetch the actual exchange rate for INR
    try:
        c = CurrencyRates()
        inr_rate = c.get_rate('USD', 'INR')
    except RatesNotAvailableError:
        pass
    inr_rate = 83.12
    
    order = Order.objects.get(user=request.user, order_number=order_num)
    additional_price = order.remake_price
    additional_price_inr = order.remake_price
    order_currency = order.currency

    if order.currency == 'INR':
        if additional_price_inr > 0:
            additional_price_inr = '%.2f'%float(float(additional_price)/float(inr_rate))
    else:
        additional_price_inr = order.remake_price

    context = {
        'inr_rate': inr_rate,
        'order': order,
        'order_currency': order_currency,
        'additional_price': float(additional_price),
        'additional_price_inr': float(additional_price_inr),
    }

    return render(request, 'amruloapp/dashboard/additional_price_billing_page.html', context)

@login_required(login_url='login')
def additional_price_payment_complete(request):
    return render(request, 'amruloapp/dashboard/additional_price_payment_complete.html')