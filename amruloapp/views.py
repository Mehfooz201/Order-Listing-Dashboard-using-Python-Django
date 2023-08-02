from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db.models import Q
from .models import  User, Order
from .forms import OrderForm
from forex_python.converter import CurrencyRates, RatesNotAvailableError


# Create your views here.



#--------------------- Home and Login Page ----------------------------
def home(request):
    return render(request, 'amruloapp/index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
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





#---------------------------------------------------------------------#
#                           Dashboard 
#---------------------------------------------------------------------#
def createOrder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_status = form.fields['order_status'].initial  # Set the default value
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
 

    context = {'active_item': 'create-order', 'form': form, 
                'inr_rate': inr_rate,}
    
    return render(request, 'amruloapp/dashboard/create-order.html', context)


def orderList(request):
    order_data = Order.objects.all()
    
    context = {'active_item': 'order-list', 'order_data':order_data}
    return render(request, 'amruloapp/dashboard/order-list.html', context)

def returnedOrder(request):
    context = {'active_item': 'return-order'}
    return render(request, 'amruloapp/dashboard/returned-orders.html', context)

def addressManagement(request):
    context = {'active_item': 'address-order'}
    return render(request, 'amruloapp/dashboard/add-manage.html', context)

def confirmReceipt(request):
    context = {'active_item': 'confirm-order'}
    return render(request, 'amruloapp/dashboard/confirm-reciept.html' ,context)

def archiveOrders(request):
    context = {'active_item': 'archive-order'}
    return render(request, 'amruloapp/dashboard/archieved-orders.html', context)

def frameworkManagement(request):
    context = {'active_item': 'framemanage-order'}
    return render(request, 'amruloapp/dashboard/framework-manage.html', context)

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
    context = {'active_item': 'staff-user'}
    return render(request, 'amruloapp/dashboard/staff-user.html', context)


#----------------------- Dental Statistics ------------------------------------#

def orderDocuments(request):
    context = {'active_item': 'order-docs'}
    return render(request, 'amruloapp/dashboard/order-documents.html', context)

