from django.shortcuts import render, redirect
from .scripts import *
from .forms import *

from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

import stripe 
from .OTP import account_activation_token

from .models import Cart, products

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    if request.user.is_authenticated:
        data = {'blocksidebar' : True,
                'cart_item_no': total_cart_items(request),
                'cart_item': cart_items(request)}
        return render(request, 'core/index.html', data)
    else:
        data = {'blocksidebar': True}
        return render(request, 'core/index.html', data)

def browse_product(request):
    
    if 'query' in request.GET:
        search_text = request.GET['query']
        product = search_product(search_text)
    else:
        product = all_products()
    
    data = {'product': product, 
            'category': all_category(),
            'searchbar': True}
    
    return render(request, 'core/browse_product.html', data)

@login_required
def add_to_cart(request, product_id):
        product = products.objects.get(Product_id__icontains=product_id)
        cart_item = Cart.objects.filter(user=request.user, product=product)
        if cart_item.count() > 0:
                cart_item = cart_item.first()
                cart_item.quantity += 1
                cart_item.save()
        else:
                cart_item = Cart(
                        user=request.user,
                        product=product,
                        quantity=1
                )
                cart_item.save()
        return redirect('browse_product')

@login_required
def checkout_page(request):
    
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='INR',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return redirect('/')
    else:
        if request.user.address_1 == "":
            data = {'blocksidebar': True,
                    'cart_item_no': total_cart_items(request),
                    'cart_item': cart_items(request),
                    'form': ProfileForm(),
                    'error_box': True,
                    'error': "Please add your address first then make order"}    
            return render(request, 'core/user_profile.html', data)
            
        products = cart_items(request) 

        total_price = 0
        for items in products.all():
            total_price += items.product.Selling_price * items.quantity
        total_price = total_price*100

        data = {'blocksidebar': True,
                'blockfooter': True,
                'cart_item_no': total_cart_items(request),
                'cart_item': products,
                'products': products,
                'real_price': total_price/100,
                'quantity': total_cart_items(request),
                'total_price': total_price,
                'key': settings.STRIPE_PUBLISHABLE_KEY}

        return render(request, 'core/checkout.html', data)

@login_required
def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='INR',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')

def signup_view(request):
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}

        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():   
                        instance = form.save(commit=False)
                        instance.is_customer = True                        
                        instance.save()            

                        username = request.POST.get('username')
                        password = request.POST.get('password1')
                        user = authenticate(username=username, password=password)
                        login(request, user)  
                        send_verficationmail(request)      

                        return redirect('/')

                else:
                    data['form'] = form
                    return render(request, 'core/signup.html', data)
        else:
            form = SignUpForm()
            data['form'] = form
            return render(request, 'core/signup.html', data)

@login_required
def email_verification(request):
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    send_verficationmail(request)
    return render(request, 'core/email_sent.html', data)

def activate(request, uidb64, token):
    data = {'blocksidebar': True,
            'blockfooter': True,
            'blocknavbar': True}
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        login(request, user)
        data['message']="Your email is activated and verified"
        return render(request, 'core/verification_email.html', data)
    else:
        data['message']="Activation link is invalid and email is not verified"
        return render(request, 'core/verification_email.html', data)

def login_view(request):
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True}
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(username=username, password=password)
                    if user!=None:
                        sent_OTP(user.email) 
                        return redirect('buyer_otp_verification', user.email)
                    else:
                        data['form'] = form
                        data['error_box'] = True
                        data['error'] = "Invalid username or password"
                        return render(request, 'core/login.html', data)
                else:
                    data['form'] = form
                    return render(request, 'core/login.html', data)
        else:
                form = LoginForm()
                data['form'] = form
                return render(request, 'core/login.html', data)

def OTP_verification(request, email):
    if request.method == 'POST':
        form = SecondStepVerificationForm(request.POST)
        if form.is_valid():
            user = checkOTP(request.POST.get('OTP'), email)
            if user==False:
                data = {'blocksidebar': True,
                        'blockfooter': True,
                        'blocknavbar': True,
                        'form': form, 
                        'error_box': True,
                        'error': 'Invalid OTP'}
                return render(request, 'core/verification.html', data)                
            else:                
                login(request, user)
                return redirect('/')
                
    else:
        data = {'blocksidebar': True,
                'blockfooter': True,
                'blocknavbar': True,
                'form': SecondStepVerificationForm()}
        return render(request, 'core/verification.html', data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def user_profile(request):
    data = {'blocksidebar': True,
            'cart_item_no': total_cart_items(request),
            'cart_item': cart_items(request)}     
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            request.user.address_1 = request.POST.get('address_1')
            request.user.address_2 = request.POST.get('address_2')
            request.user.city = request.POST.get('city')
            request.user.state = request.POST.get('state')
            request.user.zip_code = request.POST.get('zip_code')
            request.user.save(update_fields=['address_1', 'address_2', 'city', 'state', 'zip_code'])           
            return redirect('/user_profile/')
    else:
        data['form'] = ProfileForm()   
    return render(request, 'core/user_profile.html', data)

def help_page(request):
    data = {'blocksidebar': True}
    return render(request, 'core/help.html', data)