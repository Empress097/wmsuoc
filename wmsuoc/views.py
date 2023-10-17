from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from wmsuoc.forms import *
from .models import *
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from xhtml2pdf import pisa
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User saved:", user)  # Add this line for debugging
            messages.success(request, "Registration Success!")
            return redirect('home')
        else:
            print("Form is not valid:", form.errors)  # Add this line for debugging
            messages.error(request, "Please check for errors indicated!")
    else:
        form = UsersCreationForm()
    return render(request, 'store/index.html', {'form': form})

def login_customer(request):
    form = AuthenticationForm(request)  # Define form outside the if block
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Update the form with POST data
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('customer_page')
            else:
                messages.error(request, "No user information found!")
        else:
            messages.error(request, "Invalid credentials. Please check your username and password.")
    return render(request, 'store/customer_login.html', {'form': form})

@login_required
def customer_page(request):
    products = Product.objects.filter(is_active=True)
    print(products)
    context = {
        'products':products,
    }
    return render(request, 'store/customer_page.html',context)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    messages.success(request, 'Added to Cart successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    messages.success(request, "Item quantity is now added!")
    return redirect('customer_orderlist')

@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            messages.success(request, 'Item is now deleted from cart!')
            cp.delete()
        else:
            cp.quantity -= 1
            messages.success(request, 'Item is removed by 1')
            cp.save()
    return redirect('customer_orderlist')

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Item removed from Cart.")
    return redirect('customer_orderlist')

@login_required
def customer_orderlist(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)
    amount = decimal.Decimal(0)
    delivery_fee = decimal.Decimal(50)
    one_radius = decimal.Decimal(0)
    one_total = delivery_fee + one_radius
    total_fee_1 = one_total
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
    context = {
        'cart_products':cart_products,
        'amount':amount,
        'delivery_fee': delivery_fee,
        'one_radius': one_radius,
        'total_fee_1': total_fee_1,
        'total_amount_1': amount+delivery_fee,
    }
    return render(request, 'store/customer_orderlist.html',context)

def customer_cart(request):
    return render(request, 'store/customer_cart.html')

def customer_track_order(request):
    return render(request, 'store/customer_track_order.html')

def vendor_dashboard(request):
    return render(request, 'store/vendor_dashboard.html')

def vendor_addfood(request):
    return render(request, 'store/vendor_addfood.html')

def vendor_pending_order(request):
    return render(request, 'store/vendor_pending_order.html')

def vendor_pending_order_details(request):
    return render(request, 'store/vendor_pending_order_details.html')

def vendor_remittance(request):
    return render(request, 'store/vendor_remittance.html')

def vendor_gcash(request):
    return render(request, 'store/vendor_gcash.html')

def errand_dashboard(request):
    return render(request, 'store/errand_dashboard.html')

def customer_profile(request):
    return render(request, 'store/customer_profile.html')

def admin_login(request):
    return render(request, 'store/admin_login.html')

def admin_dashboard(request):
    if request.method == 'POST':
        vendor_form = VendorCreationForm(request.POST)
        if vendor_form.is_valid():
            vendor_form.save()
            messages.success(request, "Registration Success!")
            return redirect('admin_dashboard')
        else:
            print("Form is not valid:", vendor_form.errors)  # Add this line for debugging
            messages.error(request, "Please check for errors indicated!")
    else:
        vendor_form = VendorCreationForm()
    return render(request, 'store/admin_dashboard.html', {'vendor_form': vendor_form})