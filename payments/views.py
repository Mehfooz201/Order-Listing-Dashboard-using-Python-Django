from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from amruloapp.models import Order
from payments.models import orderPayment, additionalPricePayment
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from amruloapp.forms import OrderForm, UserProfileUpdateForm, StaffUserCreationForm, RemakeRequestForm
import json
from django.http import JsonResponse
# Create your views here.


@login_required(login_url='login')
def main_order_payment_request(request):
    body = json.loads(request.body)

    order = Order.objects.create(user=request.user,
                    customer_name = body['customer_name'],
                    manufacturer = body['manufacturer'],
                    order_type = body['order_type'],
                    purchaser = body['purchaser'],
                    salesman = body['salesman'],
                    requirements_remarks = body['requirements_remarks'],
                    original_data_id = int(body['original_data']),
                    design_printing_id = int(body['design_printing']),
                    product_type_id = int(body['product_type']),
                    product_sub_type_id = int(body['product_sub_type']),
                    product_material_id = int(body['product_material']),
                    unit_of_measurement_id = int(body['unit_of_measurement']),
                    delivery_timing_id = int(body['delivery_timing']),
                    currency = body['currency'],
                    quantity = body['quantity'],
                    price = body['amount'],
                    design_requirement = "uploads/files/otherfiles/"+body['design_requirement'],
                    file_upload_required = "uploads/files/stl-dcm-html/"+body['file_upload_required'])
    order.save()


    # Store transaction details inside Payment model
    payment = orderPayment(
        user = request.user,
        order_number = order.order_number,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = body['amount'],
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
def main_order_billing_page(request , price=0, price_inr=0,
            manufacturer=None, product_type=None, product_sub_type=None,
             customer_name=None, purchaser=None,order_type=None, salesman=None,
             requirements_remarks=None, original_data=None,design_printing=None, product_material=None,
             unit_of_measurement=None, delivery_timing=None,currency=None, quantity=None,
             design_requirement=None, file_upload_required=None,):
    current_user = request.user
    inr_rate = 0

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            manufacturer = form.cleaned_data['manufacturer']
            order_type = form.cleaned_data['order_type']
            purchaser = form.cleaned_data['purchaser']
            salesman = form.cleaned_data['salesman']
            requirements_remarks = form.cleaned_data['requirements_remarks']

            original_data = request.POST.get('original_data')
            design_printing = request.POST.get('design_printing')
            product_type = request.POST.get('product_type')
            product_sub_type = request.POST.get('product_sub_type')
            product_type_ = form.cleaned_data['product_type']
            product_sub_type_ = form.cleaned_data['product_sub_type']
            product_material = request.POST.get('product_material')

            unit_of_measurement = request.POST.get('unit_of_measurement')
            delivery_timing = request.POST.get('delivery_timing')
            
            currency = form.cleaned_data['currency']
            quantity = form.cleaned_data['quantity']

            price = form.cleaned_data['price']
            price_usd = form.cleaned_data['price']

            design_requirement = form.cleaned_data['design_requirement']
            file_upload_required = form.cleaned_data['file_upload_required']

            #order_price = form.save(commit=False)
            #order.order_status = form.fields['order_status'].initial  # Set the default value
            #order.user = request.user  # Set the user field to the currently logged-in user
            #order.price = order.calculate_price
            #order.save()

    # Fetch the actual exchange rate for INR
    try:
        c = CurrencyRates()
        inr_rate = c.get_rate('USD', 'INR')
    except RatesNotAvailableError:
        inr_rate = 83.12

    if currency == 'INR':
        if price_usd > 0:
            price_usd = '%.2f'%float(float(price)/float(inr_rate))
    else:
        price_usd = price

    context = {
        'inr_rate': inr_rate,
        'price_usd': float(price_usd),

        'customer_name': customer_name,
        'manufacturer': manufacturer,
        'order_type': order_type,
        'purchaser': purchaser,
        'salesman': salesman,
        'requirements_remarks': requirements_remarks,

        'original_data': original_data,
        'design_printing': design_printing,
        'product_type': product_type,
        'product_sub_type': product_sub_type,
        'product_type_': product_type_,
        'product_sub_type_': product_sub_type_,
        'product_material': product_material,

        'unit_of_measurement': unit_of_measurement,
        'delivery_timing': delivery_timing,

        'currency': currency,
        'quantity': quantity,
        
        'price': float(price),

        'design_requirement': design_requirement,
        'file_upload_required': file_upload_required,
        
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
    order.remake_price = 0
    order.order_status = 'review'
    order.save()

    # Store transaction details inside Payment model
    payment = additionalPricePayment(
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