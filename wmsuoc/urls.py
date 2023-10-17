from wmsuoc.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('login_customer/', views.login_customer, name="login_customer"),
    path('customer_page/', views.customer_page, name="customer_page"),
    path('customer_orderlist/', views.customer_orderlist, name="customer_orderlist"),
    path('customer_cart/', views.customer_cart, name="customer_cart"),
    path('customer_track_order/', views.customer_track_order, name="customer_track_order"),
    path('vendor_dashboard/', views.vendor_dashboard, name="vendor_dashboard"),
    path('vendor_addfood/', views.vendor_addfood, name="vendor_addfood"),
    path('vendor_pending_order/', views.vendor_pending_order, name="vendor_pending_order"),
    path('vendor_pending_order_details/', views.vendor_pending_order_details, name="vendor_pending_order_details"),
    path('vendor_remittance/', views.vendor_remittance, name="vendor_remittance"),
    path('vendor_gcash/', views.vendor_gcash, name="vendor_gcash"),
    path('errand_dashboard/', views.errand_dashboard, name="errand_dashboard"),
    path('customer_profile/', views.customer_profile, name="customer_profile"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),


    





]
