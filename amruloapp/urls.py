from django.urls import path
from . import views
from payments.views import order_payments, order_complete, payments
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
    path('payments/', payments, name='payments'),
    path('order_payments/<int:order_num>/', order_payments, name='order_payments'),
    path('order_complete/', order_complete, name='order_complete'),


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
