from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db.models import Q
from .models import  User, Order, FrameworkAgreement, CompanyInformation, FrameworkInformation
from products.models import (
    OriginalData,DesignPrinting,ProductType,ProductSubType,
    ProductMaterial,UnitOfMeasurement,DeliveryTiming,
    Product12HrsPrice,Product6HrsPrice,Product2HrsPrice,Product
    )
from .forms import OrderForm, UserProfileUpdateForm, StaffUserCreationForm, RemakeRequestForm
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, date, timedelta

from .decorators import allowed_users

from django.core.mail import send_mail

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

from django.contrib.auth.models import Group
from datetime import datetime
from dateutil.parser import parse
from notifications.models import Notification
from notifications.signals import notify
from django.core import serializers
import json

# Create your views here.


def notifications(request, notification_pk):
    notifcation = Notification.objects.get(id = notification_pk, recipient = request.user)
    notifcation.mark_as_read()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# --------------------- Home and Login Page ----------------------------
def home(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Compose and send the email
        subject = f"New Contact Form Submission from {name}"
        from_email = 'cdllabs38@gmail.com'  # Replace with your email
        recipient_list = ['cdllabs38@gmail.com']  # Replace with recipient email(s)
        message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Optionally, you can add a success message here
        return render(request, 'amruloapp/index.html')
    
    return render(request, 'amruloapp/index.html')




#----------------------- Staff Manage----------------------------------------#


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def addStaffUser(request):
    users = User.objects.all()
    groups = Group.objects.filter(name__in=['Vendor', 'User'])
    
    if request.method == 'POST':
        staff_user_form = StaffUserCreationForm(request.POST)
        if staff_user_form.is_valid():
            email = staff_user_form.cleaned_data['email']
            password1 = staff_user_form.cleaned_data['password1']
            password2 = staff_user_form.cleaned_data['password2']
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email.')
            elif password1 != password2:
                messages.error(request, 'Passwords do not match. Please re-enter your password.')
            else:
                user = staff_user_form.save(commit=False)
                user.is_staff = True
                user.save()
                
                # Get the selected group ID from the form data
                group_id = request.POST.get('groups')
                group = Group.objects.get(id=group_id)
                user.groups.add(group)  # Add user to the selected group
                
                messages.success(request, 'Staff User added successfully.')
                return redirect('staff-user')
            print(staff_user_form.errors)

            print('errors', user)
        else:
            print("Direct jumping here !")
            print(staff_user_form.errors)
            messages.error(request, 'There are errors in the form. Please correct them.')
    else:
        staff_user_form = StaffUserCreationForm()
        print(staff_user_form.errors)

    context = {'active_item': 'staff-user', 'staff_user_form': staff_user_form, 'users': users, 'groups': groups}
    return render(request, 'amruloapp/dashboard/staff-user.html', context)





login_required(login_url='login') 
def frameworkManagement(request):
    user = request.user
    agreements = FrameworkAgreement.objects.filter(customer=user)
    frameinfo = FrameworkInformation.objects.all()

    orders = Order.objects.filter(user=user, framework_agreement__in=agreements)

    product_sub_type = ProductSubType.objects.all()
    product_material = ProductMaterial.objects.all()
    delivery_timing = DeliveryTiming.objects.all()
    products = Product.objects.all()

    company = CompanyInformation.objects.all()
    context = {'active_item': 'framemanage-order',
     'agreements': agreements, 
     'orders': orders, 
     'company':company, 
     'frameinfo':frameinfo, 
     'current_date': date.today(),
     'product_sub_type':product_sub_type,
     'product_material':product_material,
     'delivery_timing':delivery_timing,
     'products':products,}

    return render(request, 'amruloapp/dashboard/framework-manage.html', context)


login_required(login_url='login')
def generate_pdf(request):
    user = request.user
    agreements = FrameworkAgreement.objects.filter(customer=user)
    orders = Order.objects.filter(user=user, framework_agreement__in=agreements)
    company = CompanyInformation.objects.all()
    current_date = date.today()
    context = {
        'agreements': agreements,
        'orders': orders,
        'company': company,
        'current_date': current_date,
    }

    template = get_template('amruloapp/dashboard/framework-agreement-pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="framework_agreement.pdf"'

    buffer = BytesIO()
    pisa.CreatePDF(html, dest=buffer, encoding='utf-8')

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
    
    

def signin(request):
    if request.user.is_authenticated:
        return redirect('create-order')
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doest not exist.")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('create-order')
        else:
            messages.error(request, "Email & Password doest not exist.")
    return render(request, 'amruloapp/login.html', )

#Logout
def logoutUser(request):
    logout(request)
    return redirect('login')


login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('user-profile', id=request.user.id)
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('user-profile', id=request.user.id)
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('user-profile', id=request.user.id)  # Redirect to profile page

    return render(request, 'amruloapp/dashboard/user_profile.html')





#---------------------------------------------------------------------#
#                           Dashboard 
#---------------------------------------------------------------------#


@login_required(login_url='login')
def createOrder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_status = form.fields['order_status'].initial  # Set the default value
            order.user = request.user  # Set the user field to the currently logged-in user
            order.price = order.calculate_price()
            order.save()
            notify.send(request.user, recipient=request.user, verb='order created successfully !')
            return redirect('order-list')
        else:
            messages.error(request, "These fields are required")
            print('Form validation error:', form.errors)
    else:
        form = OrderForm()   
    
    # Fetch the actual exchange rate for INR
    #try:
        #c = CurrencyRates()
        #inr_rate = c.get_rate('USD', 'INR')
    #except RatesNotAvailableError:
        # Handle the error gracefully, e.g., use a default exchange rate
    #    pass
    inr_rate = 82.0  # You can use a default value here or handle the error as per your requirement
    
    company = CompanyInformation.objects.all()
    original_data = OriginalData.objects.all()
    design_printing = DesignPrinting.objects.all()
    product_type = ProductType.objects.all()
    product_sub_type = ProductSubType.objects.all()

    product_material = ProductMaterial.objects.all()
    data_material = []
    for i in product_material:
        data_material.append({'name':i.name})
    data_filtered = [dict(value) for value in {tuple(material.items()) for material in data_material}]

    unit_of_measurement = UnitOfMeasurement.objects.all()

    product_12hrs_price = Product12HrsPrice.objects.all()
    product_6hrs_price = Product6HrsPrice.objects.all()
    product_2hrs_price = Product2HrsPrice.objects.all()

    delivery_timing = DeliveryTiming.objects.all()
    products = Product.objects.all()
    data_product_price = []
    for j in delivery_timing:
        data_product_price.append({str(j.name):{str(i.product_sub_type.name).replace("\xa0"," "):i.product_12hrs_price.delivery_timing.name == j.name and float(i.product_12hrs_price.price) or i.product_6hrs_price.delivery_timing.name == j.name and float(i.product_6hrs_price.price) or i.product_2hrs_price.delivery_timing.name == j.name and float(i.product_2hrs_price.price) for i in products }})

    format_data1 = str(data_product_price).replace('[','')
    format_data2 = format_data1.replace(']','')
    format_data3 = format_data2.replace("}}, {","}, ")
    format_data4 = format_data3.replace("}}, {","}, ")
    format_data5 = format_data4.replace("'","\"")
    format_data6 = str(format_data5).replace("\'"," ")

    context = {
        'active_item': 'create-order',
        'form': form,
        'inr_rate': inr_rate,
        'company': company,
        'company' : company,
        'original_data' : original_data,
        'design_printing' : design_printing,
        'product_type' : product_type,
        'product_sub_type' : product_sub_type,
        'product_material' : data_filtered,
        'unit_of_measurement' : unit_of_measurement,
        'delivery_timing' : delivery_timing,
        'product_12hrs_price' : product_12hrs_price,
        'product_6hrs_price' : product_6hrs_price,
        'product_2hrs_price' : product_2hrs_price,
        'product_price' : format_data6,
        }
    
    return render(request, 'amruloapp/dashboard/create-order.html', context)


@login_required(login_url='login')
def orderList(request):
    user = request.user
    order_number = request.GET.get('order_number')
    date_range = request.GET.get('date_range')

    # order_data = Order.objects.filter(user=user)
    order_data = Order.objects.all().order_by('-order_number')

    

    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            # Handle invalid order number input
            pass

    if request.method == 'POST':
        revoke_order_number = request.POST.get('revoke_order_number')
        if revoke_order_number:
            try:
                order_to_revoke = Order.objects.get(order_number=int(revoke_order_number))
                order_to_revoke.delete()
                messages.success(request, 'Order Record has been deleted successfully.')
                return redirect('order-list')
            except Order.DoesNotExist:
                pass


    if request.method == 'POST':
        order_number = request.POST.get('order_number')  # Get the order number from the submitted form
        order = get_object_or_404(Order, order_number=order_number)  # Get the order
        remake_form = RemakeRequestForm(request.POST, instance=order)

        if remake_form.is_valid():
            order_number = remake_form.instance.order_number  # Get the order number
            order = Order.objects.get(order_number=order_number)  # Get the order

            # Update the fields from the form
            order.remake_notes = remake_form.cleaned_data['remake_notes']
            order.num_crowns = remake_form.cleaned_data['num_crowns']
            order.num_brackets = remake_form.cleaned_data['num_brackets']
            order.order_status = 'pending'  # Set the order status to pending

            order.save()  # Save the order with updated fields
            messages.success(request, 'Remake request submitted successfully.')
            return redirect('remake-order')
                    
    if date_range:
        start_date, end_date = date_range.split(' - ')
        start_date = parse(start_date).date()
        end_date = parse(end_date).date() + timedelta(days=1)  # Include the end date itself
        order_data = order_data.filter(order_date__range=(start_date, end_date))

    
    context = {'active_item': 'order-list', 'order_data': order_data}
    return render(request, 'amruloapp/dashboard/order-list.html', context)



@login_required(login_url='login')
def remakeOrder(request):
    user = request.user  # Get the logged-in user
    order_number = request.GET.get('order_number')
    order_data = Order.objects.filter(user=user, order_status='pending')

    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            # Handle invalid order number input
            pass

    if request.method == 'POST':
        revoke_order_number = request.POST.get('revoke_order_number')
        if revoke_order_number:
            try:
                order_to_revoke = Order.objects.get(order_number=int(revoke_order_number))
                order_to_revoke.delete()
                messages.success(request, 'Order Record has been deleted successfully.')
                return redirect('remake-order')
            except Order.DoesNotExist:
                pass

    context = {'active_item': 'remake-order', 'order_data':order_data}
    return render(request, 'amruloapp/dashboard/remake-order.html', context)






@login_required(login_url='login')
def userProfile(request, id):
    user = get_object_or_404(User, id=id)
    form = UserProfileUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user-profile', id=id)

    context = {'user': user, 'form': form}
    return render(request, 'amruloapp/dashboard/user_profile.html', context)











@login_required(login_url='login')
def monthlyStatement(request):
    user = request.user
    order_number = request.GET.get('order_number')
    date_range = request.GET.get('date_range')

    order_data = Order.objects.filter(user=user)

    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            pass

    if date_range:
        start_date, end_date = date_range.split(' - ')
        start_date = parse(start_date).date()
        end_date = parse(end_date).date() + timedelta(days=1)  # Include the end date itself
        order_data = order_data.filter(order_date__range=(start_date, end_date))

    context = {'active_item': 'monthly-order', 'order_data': order_data}
    return render(request, 'amruloapp/dashboard/monthly-statement.html', context)



@login_required(login_url='login')
def cadResult(request):
    user = request.user  # Get the logged-in user
    order_number = request.GET.get('order_number')

    #Single Status of Order
    # order_data = Order.objects.filter(user=user, order_status='completed')

    #Multi order Status query
    # Get orders with 'completed' or 'approved' status
    order_data = Order.objects.filter(
        Q(user=user, order_status='completed') | Q(user=user, order_status='approved')
    )
    
    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            # Handle invalid order number input
            pass
    
    if request.method == 'POST':
        order_number = request.POST.get('order_number')  # Get the order number from the submitted form
        order = get_object_or_404(Order, order_number=order_number)  # Get the order
        remake_form = RemakeRequestForm(request.POST, instance=order)

        if remake_form.is_valid():
            order_number = remake_form.instance.order_number  # Get the order number
            order = Order.objects.get(order_number=order_number)  # Get the order

            # Update the fields from the form
            order.remake_notes = remake_form.cleaned_data['remake_notes']
            order.num_crowns = remake_form.cleaned_data['num_crowns']
            order.num_brackets = remake_form.cleaned_data['num_brackets']
            order.order_status = 'pending'  # Set the order status to pending

            order.save()  # Save the order with updated fields
            messages.success(request, 'Remake request submitted successfully.')
            return redirect('remake-order')

    context = {'active_item': 'cad-order', 'order_data':order_data}
    return render(request, 'amruloapp/dashboard/cad-result.html', context)


#----------------------- Dental Statistics ------------------------------------#
@login_required(login_url='login')
def orderDocuments(request):
    user = request.user  # Get the logged-in user
    order_number = request.GET.get('order_number')
    order_data = Order.objects.filter(user=user)
    date_range = request.GET.get('date_range')

    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            # Handle invalid order number input
            pass
    
    if date_range:
        start_date, end_date = date_range.split(' - ')
        start_date = parse(start_date).date()
        end_date = parse(end_date).date() + timedelta(days=1)  # Include the end date itself
        order_data = order_data.filter(order_date__range=(start_date, end_date))

    context = {'active_item': 'order-docs', 'order_data':order_data}
    return render(request, 'amruloapp/dashboard/order-documents.html', context)




