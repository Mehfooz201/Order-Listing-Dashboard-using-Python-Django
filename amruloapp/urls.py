from django.urls import path
from amruloapp import views
from payments.views import (
    additional_price_payment_request,
    additional_price_billing_page,
    additional_price_payment_complete,
    main_order_payment_request,
    main_order_billing_page,
    main_order_payment_complete)
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .forms import MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    # path('', TemplateView.as_view(template_name='baseapp/homepage.html')),
    path('', views.home, name='home'),
    path('login/', views.signin, name='login'),

    # path('login/', views.signin, name='login'),
    path('logout/', views.logoutUser, name="logout"),


#---------------------------------------------------------------------------
#Dashboard of Amrulo Web Application
#---------------------------------------------------------------------------

    #My Order
    path('create-order/', views.createOrder, name='create-order'),

    path('order-list/', views.orderList, name='order-list'),
    path('additional_price_payment_request/', additional_price_payment_request, name='additional_price_payment_request'),
    path('additional_price_billing_page/<int:order_num>/', additional_price_billing_page, name='additional_price_billing_page'),
    path('additional_price_payment_complete/', additional_price_payment_complete, name='additional_price_payment_complete'),
    path('main_order_payment_request/', main_order_payment_request, name='main_order_payment_request'),
    path('main_order_billing_page/<int:order_num>/', main_order_billing_page, name='main_order_billing_page'),
    path('main_order_payment_complete/', main_order_payment_complete, name='main_order_payment_complete'),


    path('framework-manage/', views.frameworkManagement, name='framework-manage'),
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),



    path('remake-order/', views.remakeOrder, name='remake-order'),

    path('monthly-statement/', views.monthlyStatement, name='monthly-statement'),

    path('cad-design/', views.cadResult, name='cad-result'),


    #UserProfile Details
    path('user-profile/<int:id>/', views.userProfile, name='user-profile'),

    path('change-password/', views.changePassword, name='change_password'),



    #Staff User
    path('staff-user', views.addStaffUser, name='staff-user'),


    #Dental statistics
    path('order-documents', views.orderDocuments, name='order-documents'),



    #Forget Password
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='amruloapp/password_reset_form.html', form_class=MyPasswordResetForm), name='password_reset'),
    
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='amruloapp/password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='amruloapp/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='amruloapp/password_reset_complete.html'), name='password_reset_complete'),

    


]
