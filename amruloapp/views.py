from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db.models import Q
from .models import  User, Order, FrameworkAgreement, CompanyInformation
from .forms import OrderForm, UserProfileUpdateForm, StaffUserCreationForm
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404



# Create your views here.

#--------------------- Home and Login Page ----------------------------
# def home(request):
#     return render(request, 'amruloapp/index.html')

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


@login_required
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
@login_required 
def createOrder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_status = form.fields['order_status'].initial  # Set the default value
            order.user = request.user  # Set the user field to the currently logged-in user
            order.price = order.calculate_price()
            order.save()
            return redirect('order-list')
        else:
            messages.error(request, "These fields are required")
            print('Form validation error:', form.errors)
    else:
        form = OrderForm()   
    
    # Fetch the actual exchange rate for INR
    try:
        c = CurrencyRates()
        inr_rate = c.get_rate('USD', 'INR')
    except RatesNotAvailableError:
        # Handle the error gracefully, e.g., use a default exchange rate
        inr_rate = 82.0  # You can use a default value here or handle the error as per your requirement
    
    company = CompanyInformation.objects.all()

    context = {'active_item': 'create-order', 'form': form, 
                'inr_rate': inr_rate, 'company': company}
    
    return render(request, 'amruloapp/dashboard/create-order.html', context)


@login_required 
def orderList(request):
    user = request.user
    order_number = request.GET.get('order_number')
    from_date = request.GET.get('fromdate')
    to_date = request.GET.get('todate')

    # order_data = Order.objects.filter(user=user)
    order_data = Order.objects.all()

    if order_number:
        # Filter orders based on the order_number if it's provided in the search form
        order_data = order_data.filter(order_number__icontains=order_number)
    
    if from_date and to_date:
        # Convert the date strings to datetime objects
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

        # Filter orders based on the date range
        order_data = order_data.filter(order_date__range=[from_date, to_date])
        
    context = {'active_item': 'order-list', 'order_data': order_data}
    return render(request, 'amruloapp/dashboard/order-list.html', context)

@login_required 
def confirmReceipt(request):
    user = request.user  # Get the logged-in user
    order_number = request.GET.get('order_number')
    order_data = Order.objects.filter(user=user, order_status='complete')

    if order_number:
        try:
            order_data = order_data.filter(order_number=int(order_number))
        except ValueError:
            # Handle invalid order number input
            pass

    context = {'active_item': 'confirm-order', 'order_data':order_data}
    return render(request, 'amruloapp/dashboard/confirm-reciept.html' ,context)




@login_required
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



@login_required 
def returnedOrder(request):
    context = {'active_item': 'return-order'}
    return render(request, 'amruloapp/dashboard/returned-orders.html', context)






@login_required 
def frameworkManagement(request):
    user = request.user
    agreements = FrameworkAgreement.objects.filter(customer=user)
    orders = Order.objects.filter(user=user, framework_agreement__in=agreements)
    company = CompanyInformation.objects.all()
    context = {'active_item': 'framemanage-order', 'agreements': agreements, 'orders': orders, 'company':company}
    return render(request, 'amruloapp/dashboard/framework-manage.html', context)





@login_required 
def remakeOrder(request):
    context = {'active_item': 'remake-order'}
    return render(request, 'amruloapp/dashboard/remake-order.html', context)

def monthlyStatement(request):
    context = {'active_item': 'monthly-order'}
    return render(request, 'amruloapp/dashboard/monthly-statement.html', context)

def cadResult(request):
    context = {'active_item': 'cad-order'}
    return render(request, 'amruloapp/dashboard/cad-result.html', context)


#----------------------- Staff Manege----------------------------------------#

def addStaffUser(request):
    users = User.objects.all()
    if request.method == 'POST':
        staff_user_form = StaffUserCreationForm(request.POST)
        if staff_user_form.is_valid():
            email = staff_user_form.cleaned_data['email']
            password1 = staff_user_form.cleaned_data['password1']
            password2 = staff_user_form.cleaned_data['password2']
            
            # Check if the email already exists in User model
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists. Please use a different email.')
            # Check if passwords match
            elif password1 != password2:
                messages.error(request, 'Passwords do not match. Please re-enter your password.')
            else:
                user = staff_user_form.save(commit=False)
                user.is_staff = True
                user.save()
                messages.success(request, 'Staff User added successfully.')
                return redirect('staff-user')
        else:
            # If there are errors, display them
            messages.error(request, 'There are errors in the form. Please correct them.')
    else:
        staff_user_form = StaffUserCreationForm()

    context = {'active_item': 'staff-user', 'staff_user_form': staff_user_form, 'users': users}
    return render(request, 'amruloapp/dashboard/staff-user.html', context)



#----------------------- Dental Statistics ------------------------------------#

def orderDocuments(request):
    context = {'active_item': 'order-docs'}
    return render(request, 'amruloapp/dashboard/order-documents.html', context)




