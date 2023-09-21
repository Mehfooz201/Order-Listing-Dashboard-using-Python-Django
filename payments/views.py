from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from amruloapp.models import Order
from payments.models import Payment
from forex_python.converter import CurrencyRates, RatesNotAvailableError
import json
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='login')
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        order_id = body['orderID'],
        payment_id = body['transID'],
        payment_method = body['payment_method'],
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
def order_payments(request ,order_num, price=0):
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

    return render(request, 'amruloapp/dashboard/payment.html', context)

@login_required(login_url='login')
def order_complete(request):
    return render(request, 'amruloapp/dashboard/payment_complete.html')