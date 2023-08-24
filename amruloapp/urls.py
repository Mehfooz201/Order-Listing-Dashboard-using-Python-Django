from django.urls import path
from . import views
from django.views.generic import TemplateView


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



]
