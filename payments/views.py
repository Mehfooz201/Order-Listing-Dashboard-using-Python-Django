from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cdlapp.models import Order, OrderGallery
from payments.models import orderPayment, additionalPricePayment
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from cdlapp.forms import OrderForm, UserProfileUpdateForm, StaffUserCreationForm, RemakeRequestForm
import json
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import default_storage
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
                    delivery_timing_id = int(body['delivery_timing']),
                    currency = body['currency'],
                    quantity = body['quantity'],
                    price = body['amount'],
                    is_ordered = True)
    order.save()

    if int(body['length_input1']) > 1:
        images_files1 = body['design_requirement']
        images_files2 = images_files1.replace("&#x27;","\"")
        images_files3 = images_files2.replace(": "," : ")
        images_files4 = images_files3.replace("[","")
        images_files5 = images_files4.replace("]","")
        images_files6 = eval(images_files5)
        for upload in images_files6:
            photo = OrderGallery(order=order, title=upload["title"], image=upload["url"], extension=upload["extension"])
            photo.save()
    else:
        photo = OrderGallery(order=order, title=str(body['design_requirement']).split('/')[-1], image=str(body['design_requirement']), extension=str(body['design_requirement']).split('.')[-1])
        photo.save()

    if int(body['length_input2']) > 1:
        others_files1 = body['file_upload_required']
        others_files2 = others_files1.replace("&#x27;","\"")
        others_files3 = others_files2.replace(": "," : ")
        others_files4 = others_files3.replace("[","")
        others_files5 = others_files4.replace("]","")
        others_files6 = eval(others_files5)
        for file in others_files6:
            required_files = OrderGallery(order=order, title=file["title"], image=file["url"], extension=file["extension"])
            required_files.save()
    else:
        required_files = OrderGallery(order=order, title=str(body['file_upload_required']).split('/')[-1], image=str(body['file_upload_required']), extension=str(body['file_upload_required']).split('.')[-1])
        required_files.save()


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
            manufacturer=None, product_type=None, product_sub_type=None, product_type_=None, product_sub_type_=None,
             customer_name=None, purchaser=None,order_type=None, salesman=None,
             requirements_remarks=None, original_data=None,design_printing=None, product_material=None,
             delivery_timing=None,currency=None, quantity=None,
             design_requirement=None, file_upload_required=None,
             length_input1=0, length_input2=0):
    current_user = request.user

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

            delivery_timing = request.POST.get('delivery_timing')
            
            currency = form.cleaned_data['currency']
            quantity = form.cleaned_data['quantity']

            price = form.cleaned_data['price']
            price_usd = form.cleaned_data['price']

            length_input1 = len(request.FILES.getlist('design_requirement'))
            length_input2 = len(request.FILES.getlist('file_upload_required'))

            if length_input1 > 1:
                save_img_path=[]
                for i in request.FILES.getlist('design_requirement'):
                    path1 = os.path.join(settings.MEDIA_ROOT,'uploads/files/gallery',str(i))
                    path_img = default_storage.save(path1, i)
                    save_img_path.append({"title" : str(i), "url" : path_img, "extension" : str(i).split('.')[1]})
                design_requirement = str(save_img_path)
            else:
                path1 = os.path.join(settings.MEDIA_ROOT, 'uploads/files/gallery', str(request.FILES['design_requirement']))
                path_img = default_storage.save(path1, request.FILES['design_requirement'])
                design_requirement = str(path_img)

            if length_input2 > 1:
                save_file_path=[]
                for j in request.FILES.getlist('file_upload_required'):
                    path2 = os.path.join(settings.MEDIA_ROOT,'uploads/files/gallery',str(j))
                    path_file = default_storage.save(path2, j)
                    save_file_path.append({"title" : str(j), "url" : path_file, "extension" : str(j).split('.')[1]})
                file_upload_required = str(save_file_path)
            else:
                path2 = os.path.join(settings.MEDIA_ROOT, 'uploads/files/gallery', str(request.FILES['file_upload_required']))
                path_file = default_storage.save(path2, request.FILES['file_upload_required'])
                file_upload_required = str(path_file)
                
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

        'delivery_timing': delivery_timing,

        'currency': currency,
        'quantity': quantity,
        
        'price': float(price),

        'design_requirement': design_requirement,
        'file_upload_required': file_upload_required,
        'length_input1': length_input1,
        'length_input2': length_input2,
        
    }

    return render(request, 'cdlapp/dashboard/main_order_billing_page.html', context)

@login_required(login_url='login')
def main_order_payment_complete(request):
    return render(request, 'cdlapp/dashboard/main_order_payment_complete.html')

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

    return render(request, 'cdlapp/dashboard/additional_price_billing_page.html', context)

@login_required(login_url='login')
def additional_price_payment_complete(request):
    return render(request, 'cdlapp/dashboard/additional_price_payment_complete.html')

@login_required(login_url='login')
def later_payment_request(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, order_number=body['orderID'])

    # Order paid by customer, so is_ordered field will be true
    order.is_ordered = True
    order.save()

    # Store transaction details inside Payment model
    payment = orderPayment(
        user = request.user,
        order_number = body['orderID'],
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
def later_payment_billing_page(request ,order_num, price=0):
    current_user = request.user
    
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

    customer_name = order.customer_name
    manufacturer = order.manufacturer
    order_type = order.order_type
    purchaser = order.purchaser
    salesman = order.salesman
    requirements_remarks = order.requirements_remarks

    original_data = order.original_data
    design_printing = order.design_printing
    product_type = order.product_type
    product_sub_type = order.product_sub_type
    product_type_ = order.product_type
    product_sub_type_ = order.product_sub_type
    product_material = order.product_material

    delivery_timing = order.delivery_timing
    
    currency = order_currency
    quantity = order.quantity
    

    context = {
        'customer_name': customer_name,
        'order': order,
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

        'delivery_timing': delivery_timing,

        'currency': currency,
        'quantity': quantity,
        
        'price': float(price),
        'price_inr': float(price_inr),
    }

    return render(request, 'cdlapp/dashboard/later_payment_billing_page.html', context)

@login_required(login_url='login')
def later_payment_complete(request):
    return render(request, 'cdlapp/dashboard/later_payment_complete.html')


@login_required(login_url='login')
def create_order_request(request):

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
                    delivery_timing_id = int(body['delivery_timing']),
                    currency = body['currency'],
                    quantity = body['quantity'],
                    price = body['amount'],
                    is_ordered = False)
                    
    order.save()

    if int(body['length_input1']) > 1:
        images_files1 = body['design_requirement']
        images_files2 = images_files1.replace("&#x27;","\"")
        images_files3 = images_files2.replace(": "," : ")
        images_files4 = images_files3.replace("[","")
        images_files5 = images_files4.replace("]","")
        images_files6 = eval(images_files5)
        for upload in images_files6:
            photo = OrderGallery(order=order, title=upload["title"], image=upload["url"], extension=upload["extension"])
            photo.save()
    else:
        photo = OrderGallery(order=order, title=str(body['design_requirement']).split('/')[-1], image=str(body['design_requirement']), extension=str(body['design_requirement']).split('.')[-1])
        photo.save()

    if int(body['length_input2']) > 1:
        others_files1 = body['file_upload_required']
        others_files2 = others_files1.replace("&#x27;","\"")
        others_files3 = others_files2.replace(": "," : ")
        others_files4 = others_files3.replace("[","")
        others_files5 = others_files4.replace("]","")
        others_files6 = eval(others_files5)
        for file in others_files6:
            required_files = OrderGallery(order=order, title=file["title"], image=file["url"], extension=file["extension"])
            required_files.save()
    else:
        required_files = OrderGallery(order=order, title=str(body['file_upload_required']).split('/')[-1], image=str(body['file_upload_required']), extension=str(body['file_upload_required']).split('.')[-1])
        required_files.save()




    data = {
        'order_number': order.order_number,
    }
    return JsonResponse(data)
